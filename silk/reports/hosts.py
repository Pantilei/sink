from datetime import datetime
from typing import Any

from matplotlib import pyplot as plt

from silk.reports.base import BaseReporting


class HostsReporting(BaseReporting):
    def report_distribution_by_operating_system(self) -> None:
        pipeline = _get_distribution_by_operating_system_pipeline()
        data = self._coll.aggregate(pipeline).to_list(None)
        total_count = [row["total_count"] for row in data]
        os = [row["os"][:25] for row in data]
        fig, ax = plt.subplots()
        ax.bar(x=os, height=total_count)
        ax.set_ylabel("OS")
        title = "OS Distribution"
        ax.set_title(title)
        fig.savefig(self._reports_folder / f"{title.lower().replace(' ', '-')}-{self._report_date.date()}")

    def report_old_new_hosts_distribution(self) -> None:
        pipeline = _get_old_new_hosts_distribution_pipeline(old_date=self._report_date)
        data = self._coll.aggregate(pipeline).to_list(None)
        total_count = [row["total_count"] for row in data]
        host_age = [row["host_age"] for row in data]
        fig, ax = plt.subplots()
        ax.bar(x=host_age, height=total_count)
        ax.set_ylabel("Host count")
        title = "Old vs New Hosts"
        ax.set_title(title)
        fig.savefig(self._reports_folder / f"{title.lower().replace(' ', '-')}-{self._report_date.date()}")


def _get_distribution_by_operating_system_pipeline() -> list[dict[str, Any]]:
    return [
        {"$group": {"_id": "$os", "total_count": {"$sum": 1}}},
        {"$project": {"_id": 0, "os": "$_id", "total_count": 1}},
    ]


def _get_old_new_hosts_distribution_pipeline(old_date: datetime) -> list[dict[str, Any]]:
    return [
        {"$addFields": {"host_age": {"$cond": [{"$lte": ["$last_seen_at", old_date]}, "Old", "New"]}}},
        {"$group": {"_id": "$host_age", "total_count": {"$sum": 1}}},
        {"$project": {"_id": 0, "host_age": "$_id", "total_count": 1}},
    ]
