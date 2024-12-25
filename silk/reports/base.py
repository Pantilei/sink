import inspect
from datetime import datetime, timedelta
from pathlib import Path
from time import monotonic
from typing import ClassVar

from loguru import logger
from pymongo.collection import Collection


class BaseReporting:
    """Methods starting with report_ will be called to generate the reports."""

    __reporting_method_name__: ClassVar[str] = "report_"

    def __init__(
        self, coll: Collection, reports_folder: Path = Path("./"), report_date: datetime | None = None
    ) -> None:
        self._coll = coll
        reports_folder.mkdir(exist_ok=True)
        self._reports_folder = reports_folder
        self._report_date = report_date or datetime.now()

    def generate(self) -> None:
        logger.info("Generating the report...")
        t_start = monotonic()
        for member_name, member in inspect.getmembers(self):
            if not member_name.startswith(self.__reporting_method_name__):
                continue
            member()
        logger.info(f"Reports generated in {timedelta(seconds=monotonic()-t_start)}s.")
