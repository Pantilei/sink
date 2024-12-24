from datetime import datetime

from silk.parsers.adapters.base import HostsAdapter

_DATE_FORMAT_MICRO = "%Y-%m-%dT%H:%M:%S.%fZ"
_DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


class CrowdStrikeAdapter(HostsAdapter):
    @property
    def agent_version(self) -> str:
        return self.payload["agent_version"]

    @property
    def mac_address(self) -> str:
        return self.payload["mac_address"]

    @property
    def hostname(self) -> str:
        return self.payload["hostname"]

    @property
    def os(self) -> str:
        return self.payload["os_version"]

    @property
    def cloud_provider(self) -> str:
        return self.payload["service_provider"]

    @property
    def instance_id(self) -> str:
        return self.payload["instance_id"]

    @property
    def local_ip(self) -> str:
        return self.payload["local_ip"]

    @property
    def manufacturer(self) -> str:
        return self.payload["bios_manufacturer"]

    @property
    def model(self) -> str:
        return self.payload["system_product_name"]

    @property
    def account_id(self) -> str:
        return self.payload["service_provider_account_id"]

    @property
    def updated_at(self) -> datetime:
        return datetime.strptime(self.payload["modified_timestamp"]["$date"], _DATE_FORMAT_MICRO)

    @property
    def created_at(self) -> datetime:
        assigned_date = self.payload["device_policies"]["prevention"]["assigned_date"]
        return datetime.strptime(assigned_date[:26] + "Z", _DATE_FORMAT_MICRO)

    @property
    def last_seen_at(self) -> datetime:
        return datetime.strptime(self.payload["last_seen"], _DATE_FORMAT)

    @property
    def first_seen_at(self) -> datetime:
        return datetime.strptime(self.payload["first_seen"], _DATE_FORMAT)
