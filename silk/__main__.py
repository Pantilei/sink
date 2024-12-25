from datetime import datetime
from pathlib import Path

from pymongo import MongoClient

from silk.core.configs import settings
from silk.parsers.adapters.crowdstrike import CrowdStrikeAdapter
from silk.parsers.adapters.qualys import QualysAdapter
from silk.parsers.parser import HostsParser
from silk.providers.crowdstrike import CrowdStrikeProvider
from silk.providers.qualys import QualysProvider
from silk.reports.hosts import HostsReporting
from silk.schemas import Host


def main() -> None:
    mongo_client: MongoClient = MongoClient(host=str(settings.mongo_db_service))
    hosts_coll = mongo_client["hosts"]["hosts"]
    parser = HostsParser[Host](hosts_coll=hosts_coll, db_write_buffer_size=3)
    parser.add_provider(CrowdStrikeProvider(base_url=settings.crowdstrike_base_url), CrowdStrikeAdapter())
    parser.add_provider(QualysProvider(base_url=settings.qualys_base_url), QualysAdapter())
    parser.run()

    # NOTE: Random date from past since there is not new data
    report_date = datetime(year=2023, month=6, day=26)
    HostsReporting(hosts_coll, reports_folder=Path("./visualizations"), report_date=report_date).generate()


if __name__ == "__main__":
    main()
