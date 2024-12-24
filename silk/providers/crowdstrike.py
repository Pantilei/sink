from typing import Any

from silk.core.configs import settings
from silk.providers.base import BaseDataProvider


class CrowdStrikeProvider(BaseDataProvider):
    def authorize(self) -> None:
        self.headers |= {"token": settings.crowdstrike_token}

    def _get_hosts(self, params: dict[str, Any]) -> list[dict[str, Any]]:
        result = self.session.post(f"{self.base_url}/crowdstrike/hosts/get", params=params, headers=self.headers)
        if not result.ok:
            return []
        return result.json()
