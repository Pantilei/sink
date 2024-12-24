from concurrent.futures import CancelledError, Future, ThreadPoolExecutor
from contextlib import suppress
from threading import Lock
from typing import TYPE_CHECKING, Annotated, Generic, Iterator, Type, TypeVar

from loguru import logger
from pydantic import TypeAdapter
from pymongo.collection import Collection as MongoCollection
from pymongo.errors import BulkWriteError
from pymongo.operations import UpdateOne
from pymongo.results import BulkWriteResult

from silk.parsers.adapters.base import HostsAdapter
from silk.providers.base import BaseDataProvider
from silk.schemas import HostIdentifier

T_MODEL = TypeVar("T_MODEL", bound=HostIdentifier)
SuccessStoredCount = Annotated[int, "SuccessStoredCount"]
_MAX_LIMIT = 2


class HostsParser(Generic[T_MODEL]):
    if TYPE_CHECKING:
        __model__: Type[T_MODEL]

    def __init__(self, hosts_coll: MongoCollection, db_write_buffer_size: int = 1000) -> None:
        self._provider_to_adapter: dict[BaseDataProvider, HostsAdapter] = {}
        self._hosts_coll = hosts_coll
        self._db_write_buffer_size = db_write_buffer_size
        self._buffer: list[T_MODEL] = []
        self._buffer_lock = Lock()
        self._log_success_to_db: int = 0
        self._log_fail_to_db: int = 0
        self._log_fail_validation: int = 0

    def __class_getitem__(cls, model: Type[T_MODEL]) -> "Type[HostsParser]":
        return type(f"{cls.__name__}[{model.__name__}]", (cls,), {"__model__": model})

    def add_provider(self, provider: BaseDataProvider, adapter: HostsAdapter) -> None:
        self._provider_to_adapter[provider] = adapter

    def run(self, *, max_workers: int | None = None) -> None:
        if not self._provider_to_adapter:
            logger.info("No providers added. Skipping parsing...")
            return
        for data_provider in self._provider_to_adapter:
            data_provider.authorize()
        max_workers = max_workers or len(self._provider_to_adapter)
        logger.info(f"Start parsing with {max_workers} workers.")
        with ThreadPoolExecutor(max_workers=max_workers) as pool:
            for provider, adapter in self._provider_to_adapter.items():
                future = pool.submit(self._pipeline_exec, provider=provider, adapter=adapter)
                future.add_done_callback(self._check_future_result)
        self._try_to_store(force=True)
        logger.info(self._log_summary())

    def _parse(self, provider: BaseDataProvider, adapter: HostsAdapter) -> Iterator[T_MODEL]:
        """Perform parsing of the data."""
        skip, limit = 0, _MAX_LIMIT
        while raw_hosts := provider.get_hosts(params=dict(skip=skip, limit=limit)):
            for raw_host in raw_hosts:
                adapter.set_payload(raw_host)
                yield adapter.as_hosts_doc()  # type: ignore
            skip += _MAX_LIMIT

    def _validate(self, item: T_MODEL) -> T_MODEL:
        """Validate data coming from parse"""
        TypeAdapter(self.__model__).validate_python(item)
        return item

    def _store(self, hosts: list[T_MODEL]) -> SuccessStoredCount:
        """Store validated data"""
        write_requests = []
        for host in hosts:
            query = {"instance_id": host["instance_id"]}
            write_requests.append(UpdateOne(query, {"$set": host}, upsert=True))

        if not write_requests:
            return 0
        try:
            bulk_result: BulkWriteResult = self._hosts_coll.bulk_write(write_requests, ordered=False)
        except BulkWriteError as bwe:
            logger.error("BulkWriteError: %s", str(bwe)[:250])
            bulk_result = BulkWriteResult(bulk_api_result=bwe.details, acknowledged=True)  # type: ignore

        return bulk_result.matched_count or bulk_result.upserted_count or 0

    def _pipeline_exec(self, provider: BaseDataProvider, adapter: HostsAdapter) -> None:
        for raw_parser_item in self._parse(provider=provider, adapter=adapter):
            try:
                validated_item = self._validate(raw_parser_item)
            except Exception as validation_exc:
                logger.error(f"[Validation] {validation_exc}.")
                self._log_fail_validation += 1
                continue
            self._buffer.append(validated_item)
            self._try_to_store()

    def _try_to_store(self, force: bool = False) -> None:
        if not self._buffer or (not force and len(self._buffer) < self._db_write_buffer_size):
            return

        with self._buffer_lock:
            to_store, self._buffer = self._buffer, []

        stored_count: int = self._store(to_store) if to_store else 0
        self._log_success_to_db += stored_count
        self._log_fail_to_db += len(to_store) - stored_count

    def _check_future_result(self, future: Future) -> None:
        with suppress(CancelledError):
            if exc := future.exception():
                logger.error("Unhandled error in worker: %s", exc)

    def _log_summary(self) -> str:
        return f"""
            Parsed: {self._log_fail_validation + self._log_success_to_db + self._log_fail_to_db}            
            ------------------------            
            Validation =>            
            FAIL: {self._log_fail_validation}            
            ------------------------           
            DB writes =>            
            SUCCESS: {self._log_success_to_db}            
            FAIL: {self._log_fail_to_db}   
        """
