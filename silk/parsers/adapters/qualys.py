from datetime import datetime

from silk.parsers.adapters.base import HostsAdapter

_DATE_FORMAT_MICRO = "%Y-%m-%dT%H:%M:%S.%fZ"
_DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


class QualysAdapter(HostsAdapter):
    @property
    def agent_version(self) -> str:
        return self.payload["agentInfo"]["agentVersion"]

    @property
    def mac_address(self) -> str:
        return self.payload["macAddress"]

    @property
    def hostname(self) -> str:
        return self.payload["dnsHostName"]

    @property
    def os(self) -> str:
        return self.payload["os"]

    @property
    def cloud_provider(self) -> str:
        return self.payload["cloudProvider"]

    @property
    def instance_id(self) -> str:
        return self.payload["instanceId"]

    @property
    def local_ip(self) -> str:
        return self.payload["privateIpAddress"]

    @property
    def manufacturer(self) -> str:
        return self.payload["manufacturer"]

    @property
    def model(self) -> str:
        return self.payload["model"]

    @property
    def account_id(self) -> str:
        return self.payload["accountId"]

    @property
    def updated_at(self) -> datetime:
        return datetime.strptime(self.payload["lastUpdated"], _DATE_FORMAT)

    @property
    def created_at(self) -> datetime:
        return datetime.strptime(self.payload["created"], _DATE_FORMAT)

    @property
    def last_seen_at(self) -> datetime:
        return datetime.strptime(self.payload["lastVulnScan"]["$date"], _DATE_FORMAT_MICRO)

    @property
    def first_seen_at(self) -> datetime:
        return datetime.strptime(self.payload["firstDiscovered"], _DATE_FORMAT)
