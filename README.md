# 🚀 OpenAdapter

**Deploy & Integrate Screenshot Parsing and Action Models**

OpenAdapter simplifies deploying advanced screenshot parsing and action models on local or managed systems, supporting secure automation. Initial deployment options include AWS, with future support for Anthropic and OpenAI APIs.

## ✨ Key Features
- **Automated Cloud Deployment**: Deploy models on AWS EC2, with planned Anthropic/OpenAI API support and PII/PHI scrubbing.
- **Configurable with .env**: Simplifies setup with environment variables.
- **Cost-Efficiency**: Deploy high-performance instances on demand, with intelligent caching and resource pause/stop features to reduce costs.
- **Container & API Compatibility**: Supports Dockerized models like OmniParser and Set-of-Mark, with future support for Anthropic and OpenAI APIs.
- **CI/CD with GitHub Actions**: Automated integration and deployment ensure consistent updates.

### Prerequisites
- **Python 3.10+**
- **AWS Account** (support for Hugging Face, Anthropic, and OpenAI APIs planned)
- **Environment Variables**: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `GITHUB_TOKEN`

## ⚙️ Setup

1. **Clone and Enter Repository**:
   ```bash
   git clone https://github.com/OpenAdaptAI/OpenAdapter.git && cd OpenAdapter
   ```

2. **Configure Environment**:
   ```plaintext
   AWS_ACCESS_KEY_ID=<your aws access key>
   AWS_SECRET_ACCESS_KEY=<your aws secret access key>
   AWS_REGION=us-east-1
   GITHUB_OWNER=OpenAdaptAI
   GITHUB_REPO=<your repo>
   GITHUB_TOKEN=<your github token>
   ```

3. **Install Requirements Using `uv`**:
   ```bash
   pip install uv
   uv venv  # Create and activate virtual environment
   uv pip sync  # Install dependencies
   ```

## 💡 Usage
Straightforward commands to deploy and manage model instances.

### Example Deployment Script (OmniParser)
```python
from openadapter.server import OpenAdapterConfig, Deploy
import fire

class OmniParserDeploy(Deploy):
    def __init__(self):
        super().__init__(config=OpenAdapterConfig())

if __name__ == "__main__":
    fire.Fire(OmniParserDeploy)
```

### Commands
Deploy OmniParser on an AWS GPU instance:
```bash
python oa.deploy start
```

Interact with the model server:
```bash
python oa.client "http://<server_ip>:7861"
```

Pause or stop the instance:
```bash
python oa.deploy pause
python oa.deploy stop
```

Get server status and IP:
```bash
python oa.deploy status
```

### SSH Access and Logs
SSH into the server, list Docker containers, and monitor logs:
```bash
python -m oa.deploy ssh
% docker ps -a
...<container_id>...
% docker logs -f <container_id>
```

### Cost
- **Estimate**: Approx. $10/day on AWS g4dn.xlarge (100GB storage). Intelligent caching helps reduce costs by reusing data across runs.

## Modular Cloud Backends
- **AWS EC2**: Current backend, with flexible instance options and security.
- **Planned**: Hugging Face, Anthropic, OpenAI; future support for GCP and Azure.

## Integrations
Works with OpenAdapt or as a standalone solution for automated model deployment.

## 🛠️ Roadmap
- **AWS CDK Automation**: Streamline Infrastructure as Code.
- **Container Optimization**: Scale with ECS and ECR.
- **GPU & Intelligent Caching**: Optimize cost and performance.
- **Secure Data Handling**: Data encryption and VPC configurations.
- **Logging & Monitoring**: Integrate with CloudWatch.
- **Serverless Options**: AWS Lambda and Google Cloud Functions.
- **Cross-Cloud Flexibility**: Extend to GCP, Azure, and additional model APIs.

## License
MIT License.
