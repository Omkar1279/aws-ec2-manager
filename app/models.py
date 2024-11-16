from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class EC2Instance(BaseModel):
    """Data Model for instance information"""
    instance_id: str
    instance_type: str
    state: str
    public_ip: Optional[str] = ""
    private_ip: Optional[str] = ""
    name: Optional[str] = ""
    environment: Optional[str] = ""
    launch_time: datetime


class EC2InstanceRequest(BaseModel):
    """Data Model for instance request"""
    name: str
    instance_type: str
    ami_id: str
    key_pair_name: str
    security_group_id: str
    environment: str = "development"