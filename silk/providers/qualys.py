from typing import Any

from silk.core.configs import settings
from silk.providers.base import BaseDataProvider


class QualysProvider(BaseDataProvider):
    def authorize(self) -> None:
        self.headers |= {"token": settings.qualys_token}

    def _get_hosts(self, params: dict[str, Any]) -> list[dict[str, Any]]:
        result = self.session.post(f"{self.base_url}/qualys/hosts/get", params=params, headers=self.headers)
        if not result.ok:
            return []
        raw_hosts = []
        for row in result.json():
            for source_info in row["sourceInfo"]["list"]:
                for source_info_value in source_info.values():
                    if not source_info_value.get("instanceId"):
                        continue
                    raw_hosts.append({**row, **source_info_value})
        return raw_hosts
