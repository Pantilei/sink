from abc import ABC, abstractmethod
from typing import Any

from loguru import logger
from pydantic import HttpUrl
from requests import RequestException, Session


class BaseDataProvider(ABC):
    def __init__(self, base_url: HttpUrl) -> None:
        self.base_url = base_url
        self.headers = {"accept": "application/json"}
        self.session = Session()

    @abstractmethod
    def authorize(self) -> None:
        """Perform Authorization"""

    def get_hosts(self, params: dict[str, Any]) -> list[dict[str, Any]] | None:
        try:
            return self._get_hosts(params=params)
        except RequestException:
            logger.error(f"Exception on host request. Params: {params}.")
            return None

    @abstractmethod
    def _get_hosts(self, params: dict[str, Any]) -> list[dict[str, Any]]: ...
