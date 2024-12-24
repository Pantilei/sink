from datetime import datetime

from typing_extensions import TypedDict


class HostIdentifier(TypedDict):
    instance_id: str


class Host(HostIdentifier):
    agent_version: str
    mac_address: str
    hostname: str
    os: str
    cloud_provider: str
    local_ip: str
    manufacturer: str
    model: str
    account_id: str
    updated_at: datetime
    created_at: datetime
    first_seen_at: datetime
    last_seen_at: datetime
