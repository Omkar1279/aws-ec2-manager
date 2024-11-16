from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional, Generator
from datetime import datetime

from app.services import EC2Service
from app.models import EC2InstanceRequest, EC2Instance


def get_instance_service() -> Generator[EC2Service, None, None]:
    """
    Dependency provider for EC2Service.
    Creates a new instance of EC2EC2Service for each request.
    """
    service = EC2Service()

    try:
        yield service
    finally:
        pass


# Create router instance
router = APIRouter(
    prefix="/api/v1/instances",
    tags=["instances"],
    responses={
        404: {"description": "Instance not found"},
        400: {"description": "Bad request"},
        500: {"description": "Internal server error"}
    }
)


@router.post("/",
             response_model=EC2Instance,
             status_code=201,
             summary="Create a new EC2 instance",
             response_description="The created EC2 instance"
             )
async def create_instance(
        request: EC2InstanceRequest,
        service: EC2Service = Depends(get_instance_service)
) -> EC2Instance:
    """
    Create a new EC2 instance with the following parameters:

    - **name**: Name tag for the instance
    - **instance_type**: AWS instance type (e.g., t2.micro)
    - **ami_id**: ID of the Amazon Machine Image
    - **key_pair_name**: Name of the key pair for SSH access
    - **security_group_id**: ID of the security group to attach
    - **environment**: Deployment environment (default: development)
    """
    try:
        return service.create_instance(request)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to create instance: {str(e)}"
        )


@router.get("/",
            response_model=List[EC2Instance],
            summary="List all EC2 instances",
            response_description="List of EC2 instances"
            )
async def list_instances(
        environment: Optional[str] = Query(None, description="Filter by environment"),
        instance_type: Optional[str] = Query(None, description="Filter by instance type"),
        service: EC2Service = Depends(get_instance_service)
) -> List[EC2Instance]:
    """
    Retrieve a list of all EC2 instances.

    Optional query parameters:
    - **environment**: Filter instances by environment tag
    - **instance_type**: Filter instances by instance type
    """
    instances = service.list_instances()

    # Apply filters if provided
    if environment:
        instances = [i for i in instances if i.environment == environment]
    if instance_type:
        instances = [i for i in instances if i.instance_type == instance_type]

    return instances


@router.get("/{instance_id}",
            response_model=EC2Instance,
            summary="Get a specific EC2 instance",
            response_description="The requested EC2 instance"
            )
async def get_instance(
        instance_id: str,
        service: EC2Service = Depends(get_instance_service)
) -> EC2Instance:
    """
    Retrieve details for a specific EC2 instance by its ID.

    - **instance_id**: The ID of the EC2 instance to retrieve
    """
    return service.get_instance(instance_id)


@router.post("/{instance_id}/start",
             response_model=EC2Instance,
             summary="Start an EC2 instance",
             response_description="The started EC2 instance"
             )
async def start_instance(
        instance_id: str,
        service: EC2Service = Depends(get_instance_service)
) -> EC2Instance:
    """
    Start a stopped EC2 instance.

    - **instance_id**: The ID of the EC2 instance to start
    """
    return service.start_instance(instance_id)


@router.post("/{instance_id}/stop",
             response_model=EC2Instance,
             summary="Stop an EC2 instance",
             response_description="The stopped EC2 instance"
             )
async def stop_instance(
        instance_id: str,
        service: EC2Service = Depends(get_instance_service)
) -> EC2Instance:
    """
    Stop a running EC2 instance.

    - **instance_id**: The ID of the EC2 instance to stop
    """
    return service.stop_instance(instance_id)


@router.delete("/{instance_id}",
               response_model=EC2Instance,
               summary="Terminate an EC2 instance",
               response_description="The terminated EC2 instance"
               )
async def terminate_instance(
        instance_id: str,
        service: EC2Service = Depends(get_instance_service)
) -> EC2Instance:
    """
    Terminate an EC2 instance.

    - **instance_id**: The ID of the EC2 instance to terminate
    """
    return service.terminate_instance(instance_id)


# Additional endpoints for enhanced functionality

@router.get("/status/summary",
            summary="Get instance status summary",
            response_description="Summary of instance statuses"
            )
async def get_status_summary(
        service: EC2Service = Depends(get_instance_service)
) -> dict:
    """
    Get a summary of instance statuses across all instances.
    """
    instances = service.list_instances()
    status_count = {}

    for instance in instances:
        status_count[instance.state] = status_count.get(instance.state, 0) + 1

    return {
        "total_instances": len(instances),
        "status_breakdown": status_count,
        "timestamp": datetime.utcnow()
    }


@router.post("/{instance_id}/tags",
             response_model=EC2Instance,
             summary="Update instance tags",
             response_description="The updated EC2 instance"
             )
async def update_instance_tags(
        instance_id: str,
        tags: dict,
        service: EC2Service = Depends(get_instance_service)
) -> EC2Instance:
    """
    Update the tags of an EC2 instance.

    - **instance_id**: The ID of the EC2 instance to update
    - **tags**: Dictionary of tag key-value pairs to update
    """
    # Note: This would require adding an update_tags method to the EC2Service
    raise HTTPException(
        status_code=501,
        detail="Tag update functionality not implemented yet"
    )
