from abc import abstractmethod
from datetime import datetime
from typing import Any

from silk.schemas import Host, HostIdentifier


class HostsAdapter:
    payload: dict[str, Any]

    def set_payload(self, payload: dict[str, Any]) -> None:
        self.payload = payload

    @property
    @abstractmethod
    def agent_version(self) -> str: ...

    @property
    @abstractmethod
    def mac_address(self) -> str: ...

    @property
    @abstractmethod
    def hostname(self) -> str: ...

    @property
    @abstractmethod
    def os(self) -> str: ...

    @property
    @abstractmethod
    def cloud_provider(self) -> str: ...

    @property
    @abstractmethod
    def instance_id(self) -> str: ...

    @property
    @abstractmethod
    def local_ip(self) -> str: ...

    @property
    @abstractmethod
    def manufacturer(self) -> str: ...

    @property
    @abstractmethod
    def model(self) -> str: ...

    @property
    @abstractmethod
    def account_id(self) -> str: ...

    @property
    @abstractmethod
    def updated_at(self) -> datetime: ...

    @property
    @abstractmethod
    def created_at(self) -> datetime: ...

    @property
    @abstractmethod
    def last_seen_at(self) -> datetime: ...

    @property
    @abstractmethod
    def first_seen_at(self) -> datetime: ...

    def as_hosts_doc(self) -> HostIdentifier:
        return Host(
            instance_id=self.instance_id,
            agent_version=self.agent_version,
            mac_address=self.mac_address,
            hostname=self.hostname,
            os=self.os,
            cloud_provider=self.cloud_provider,
            local_ip=self.local_ip,
            manufacturer=self.manufacturer,
            model=self.model,
            account_id=self.account_id,
            updated_at=self.updated_at,
            created_at=self.created_at,
            last_seen_at=self.last_seen_at,
            first_seen_at=self.first_seen_at,
        )
