from typing import List, Optional
from abc import ABC, abstractmethod
from botocore.exceptions import ClientError
from fastapi import HTTPException

from app.models import EC2InstanceRequest, EC2Instance
from app.config import get_ec2_client


class InstanceService(ABC):
    """Abstract base class for EC2 instance management"""

    @abstractmethod
    def create_instance(self, instance_request: EC2InstanceRequest) -> EC2Instance:
        """Create a new EC2 instance"""
        pass

    @abstractmethod
    def get_instance(self, instance_id: str) -> EC2Instance:
        """Get information about a specific EC2 instance"""
        pass

    @abstractmethod
    def list_instances(self) -> List[EC2Instance]:
        """List all EC2 instances"""
        pass

    @abstractmethod
    def start_instance(self, instance_id: str) -> EC2Instance:
        """Start an EC2 instance"""
        pass

    @abstractmethod
    def stop_instance(self, instance_id: str) -> EC2Instance:
        """Stop an EC2 instance"""
        pass

    @abstractmethod
    def terminate_instance(self, instance_id: str) -> EC2Instance:
        """Terminate an EC2 instance"""
        pass


class EC2Service(InstanceService):
    """Concrete implementation of InstanceService for AWS"""

    def __init__(self):
        self.ec2_client = get_ec2_client()

    def create_instance(self, instance_request: EC2InstanceRequest) -> EC2Instance:
        try:
            response = self.ec2_client.run_instances(
                ImageId=instance_request.ami_id,
                InstanceType=instance_request.instance_type,
                KeyName=instance_request.key_pair_name,
                SecurityGroupIds=[instance_request.security_group_id],
                MinCount=1,
                MaxCount=1,
                TagSpecifications=[{
                    'ResourceType': 'instance',
                    'Tags': [
                        {'Key': 'Name', 'Value': instance_request.name},
                        {'Key': 'Environment', 'Value': instance_request.environment}
                    ]
                }]
            )

            instance_id = response['Instances'][0]['InstanceId']
            return self.get_instance(instance_id)

        except ClientError as e:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to create instance: {str(e)}"
            )

    def get_instance(self, instance_id: str) -> EC2Instance:
        try:
            response = self.ec2_client.describe_instances(
                InstanceIds=[instance_id]
            )

            if not response['Reservations']:
                raise HTTPException(
                    status_code=404,
                    detail=f"Instance {instance_id} not found"
                )

            instance = response['Reservations'][0]['Instances'][0]
            return self._convert_to_ec2_instance(instance)

        except ClientError as e:
            raise HTTPException(
                status_code=404,
                detail=f"Failed to get instance {instance_id}: {str(e)}"
            )

    def list_instances(self) -> List[EC2Instance]:
        try:
            response = self.ec2_client.describe_instances()
            instances = []

            for reservation in response['Reservations']:
                for instance in reservation['Instances']:
                    instances.append(self._convert_to_ec2_instance(instance))

            return instances

        except ClientError as e:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to list instances: {str(e)}"
            )

    def start_instance(self, instance_id: str) -> EC2Instance:
        try:
            self.ec2_client.start_instances(InstanceIds=[instance_id])
            return self.get_instance(instance_id)

        except ClientError as e:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to start instance {instance_id}: {str(e)}"
            )

    def stop_instance(self, instance_id: str) -> EC2Instance:
        try:
            self.ec2_client.stop_instances(InstanceIds=[instance_id])
            return self.get_instance(instance_id)

        except ClientError as e:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to stop instance {instance_id}: {str(e)}"
            )

    def terminate_instance(self, instance_id: str) -> EC2Instance:
        try:
            self.ec2_client.terminate_instances(InstanceIds=[instance_id])
            return self.get_instance(instance_id)

        except ClientError as e:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to terminate instance {instance_id}: {str(e)}"
            )

    def _convert_to_ec2_instance(self, aws_instance: dict) -> EC2Instance:
        """Helper method to convert AWS instance response to EC2Instance model"""
        tags = {tag['Key']: tag['Value'] for tag in aws_instance.get('Tags', [])}

        return EC2Instance(
            instance_id=aws_instance['InstanceId'],
            instance_type=aws_instance['InstanceType'],
            state=aws_instance['State']['Name'],
            public_ip=aws_instance.get('PublicIpAddress', ''),
            private_ip=aws_instance.get('PrivateIpAddress', ''),
            name=tags.get('Name', ''),
            environment=tags.get('Environment', ''),
            launch_time=aws_instance['LaunchTime']
        )
