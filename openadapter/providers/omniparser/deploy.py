# openadapter/providers/omniparser/deploy.py

import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings
from loguru import logger
import boto3
from cdktf import App, TerraformStack
from constructs import Construct
from cdktf_aws_provider import AwsProvider, ecr, ecs

class Config(BaseSettings):
    """Configuration for OmniParser deployment."""
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION: str = "us-east-1"
    PROJECT_NAME: str = "omniparser"
    
    # ECR Settings
    ECR_REPOSITORY_NAME: str = "omniparser"
    
    # ECS Settings
    ECS_CLUSTER_NAME: str = "omniparser-cluster"
    ECS_SERVICE_NAME: str = "omniparser-service"
    ECS_TASK_FAMILY: str = "omniparser-task"
    ECS_CONTAINER_NAME: str = "omniparser"
    
    # Container Settings
    CONTAINER_PORT: int = 8000
    HOST_PORT: int = 8000
    CPU: int = 2048  # 2 vCPU
    MEMORY: int = 16384  # 16GB
    GPU_COUNT: int = 1
    
    # Model Settings
    SOM_MODEL_PATH: str = "/app/weights/icon_detect/model.pt"
    CAPTION_MODEL_NAME: str = "florence2"
    CAPTION_MODEL_PATH: str = "/app/weights/icon_caption_florence"
    DEVICE: str = "cuda"
    BOX_THRESHOLD: float = 0.05

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

class OmniParserStack(TerraformStack):
    def __init__(self, scope: Construct, id: str, config: Config):
        super().__init__(scope, id)
        
        # AWS Provider
        AwsProvider(self, "AWS",
            region=config.AWS_REGION,
            access_key=config.AWS_ACCESS_KEY_ID,
            secret_key=config.AWS_SECRET_ACCESS_KEY
        )
        
        # ECR Repository
        repository = ecr.EcrRepository(self, "Repository",
            name=config.ECR_REPOSITORY_NAME,
            image_tag_mutability="MUTABLE",
            force_delete=True
        )
        
        # ECS Cluster
        cluster = ecs.EcsCluster(self, "Cluster",
            name=config.ECS_CLUSTER_NAME,
            capacity_providers=["FARGATE_SPOT"],
            default_capacity_provider_strategies=[{
                "capacity_provider": "FARGATE_SPOT",
                "weight": 1
            }]
        )
        
        # ECS Task Definition
        task_definition = ecs.EcsTaskDefinition(self, "TaskDefinition",
            family=config.ECS_TASK_FAMILY,
            requires_compatibilities=["FARGATE"],
            network_mode="awsvpc",
            cpu=str(config.CPU),
            memory=str(config.MEMORY),
            container_definitions=json.dumps([{
                "name": config.ECS_CONTAINER_NAME,
                "image": f"{repository.repository_url}:latest",
                "cpu": config.CPU,
                "memory": config.MEMORY,
                "essential": True,
                "portMappings": [{
                    "containerPort": config.CONTAINER_PORT,
                    "hostPort": config.HOST_PORT,
                    "protocol": "tcp"
                }],
                "environment": [
                    {"name": "SOM_MODEL_PATH", "value": config.SOM_MODEL_PATH},
                    {"name": "CAPTION_MODEL_NAME", "value": config.CAPTION_MODEL_NAME},
                    {"name": "CAPTION_MODEL_PATH", "value": config.CAPTION_MODEL_PATH},
                    {"name": "DEVICE", "value": config.DEVICE},
                    {"name": "BOX_THRESHOLD", "value": str(config.BOX_THRESHOLD)}
                ],
                "resourceRequirements": [{
                    "type": "GPU",
                    "value": str(config.GPU_COUNT)
                }],
                "logConfiguration": {
                    "logDriver": "awslogs",
                    "options": {
                        "awslogs-group": f"/ecs/{config.PROJECT_NAME}",
                        "awslogs-region": config.AWS_REGION,
                        "awslogs-stream-prefix": "ecs"
                    }
                }
            }])
        )

def build_and_push_image(config: Config):
    """Build and push Docker image to ECR."""
    ecr_client = boto3.client('ecr', 
        region_name=config.AWS_REGION,
        aws_access_key_id=config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY
    )
    
    # Create ECR repository if it doesn't exist
    try:
        ecr_client.create_repository(repositoryName=config.ECR_REPOSITORY_NAME)
    except ecr_client.exceptions.RepositoryAlreadyExistsException:
        pass
    
    # Get ECR login token
    auth = ecr_client.get_authorization_token()
    token = auth['authorizationData'][0]['authorizationToken']
    endpoint = auth['authorizationData'][0]['proxyEndpoint']
    
    # Build Docker image
    logger.info("Building Docker image...")
    os.system(f"docker build -t {config.ECR_REPOSITORY_NAME} .")
    
    # Tag and push image
    repository_uri = f"{endpoint.replace('https://', '')}/{config.ECR_REPOSITORY_NAME}"
    os.system(f"docker tag {config.ECR_REPOSITORY_NAME}:latest {repository_uri}:latest")
    os.system(f"docker push {repository_uri}:latest")
    
    logger.info(f"Image pushed to {repository_uri}")
    return repository_uri

def deploy(config: Config = Config()):
    """Deploy OmniParser to AWS ECS."""
    # Initialize CDK app
    app = App()
    
    # Build and push Docker image
    repository_uri = build_and_push_image(config)
    
    # Create stack
    OmniParserStack(app, "omniparser", config)
    
    # Synthesize and deploy
    app.synth()
    os.system("cdktf deploy --auto-approve")
    
    logger.info("OmniParser deployed successfully")

if __name__ == "__main__":
    deploy()

