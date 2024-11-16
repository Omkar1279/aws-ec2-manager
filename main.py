from fastapi import FastAPI
from app.routers import ec2

app = FastAPI(
    title="EC2 Instance Manager",
    description="API for managing AWS EC2 instances",
    version="1.0.0"
)

app.include_router(ec2.router)
