# OpenAdapter
Effortless Deployment and Integration for Advanced UI Action Models

OpenAdapter is a deployment tool designed for model builders and users who need
efficient, high-performance deployment of state-of-the-art screenshot parsing
models. With OpenAdapter, you can quickly and easily set up these models on
trusted hardware that you control, enabling automation with action and
screenshot data on local or securely managed systems.

This repository supports multiple cloud backends, initially with AWS, Hugging
Face Inference API, and compatibility with frontier model APIs (e.g.,
Anthropic, OpenAI), making it ideal for flexible, scalable deployment in
diverse automation use cases and
[OpenAdapt](https://github.com/OpenAdaptAI/OpenAdapt)-agnostic implementations.

## Features
- **Automated Cloud Deployment**: Rapidly deploy models on AWS EC2, Hugging
  Face Inference API, or connect with Anthropic/OpenAI APIs for remote
  inference.
- **Configurable via `.env`**: Simplify setup with a customizable environment file.
- **Cost-Efficient**: Deploy high-performance instances on demand; easily pause
  or stop resources to minimize costs.
- **Compatibility with Any Dockerized Model or Frontier Model API**: While
  OpenAdapter supports models like OmniParser and Set-of-Mark (SoM) as
  examples, it is designed to plug into any project with a Dockerfile and can
  even autogenerate a Dockerfile if necessary. Additionally, it enables seamless
  integration with non-containerized APIs like Anthropic's and OpenAI's.

For additional details on the pattern used, see:
- [OmniParser PR #52](https://github.com/microsoft/OmniParser/pull/52)
- [SoM PR #19](https://github.com/microsoft/SoM/pull/19)

## Setup

### Prerequisites
- Python 3.10+
- [AWS account](https://aws.amazon.com/) with necessary permissions for deploying on EC2  
  _(Support for [Hugging Face](https://huggingface.co/), Anthropic, and OpenAI
  APIs is planned but not yet available)_
- `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and `GITHUB_TOKEN` with repository access

### Installation
1. Clone this repository:
    ```bash
    git clone https://github.com/OpenAdaptAI/OpenAdapter.git
    cd OpenAdapter
    ```

2. Create a `.env` file in the project root with your cloud and GitHub credentials:
    ```plaintext
    AWS_ACCESS_KEY_ID=<your aws access key id>
    AWS_SECRET_ACCESS_KEY=<your aws secret access key (required)>
    AWS_REGION=<your aws region (required)>
    GITHUB_OWNER=<your github owner (required)>  # e.g., OpenAdaptAI
    GITHUB_REPO=<your github repo (required)>    # e.g., OmniParser
    GITHUB_TOKEN=<your github token (required)>
    ```

3. Install dependencies:
    ```bash
    python3 -m venv venv && source venv/bin/activate
    pip install -r deploy_requirements.txt
    ```

## Usage Examples
This tool provides a set of straightforward commands for deploying and managing model instances.

### Start the Deployment
To deploy a model (such as OmniParser or Set-of-Mark) on an AWS EC2 instance with GPU and 100GB storage (default), run:
```bash
python deploy.py start
```

### Interact with the Deployed Model
After deployment, you can interact with the model server:
```bash
python client.py "http://<server_ip>:7861"
```

### Pause or Stop the Instance
Pause the instance (shutdown without deleting resources):
```bash
python deploy.py pause
```

Stop the instance entirely, freeing all associated resources:
```bash
python deploy.py stop
```

### Check Server Status
To check the status of the EC2 instance and retrieve its public IP:
```bash
python deploy.py status
```

### SSH Access
SSH into the deployed instance for direct access:
```bash
python deploy.py ssh
```

## Costs
- **Approximate Cost**: Running a model on the default `AWS g4dn.xlarge`
instance with 100GB storage costs around $10/day ($0.526/hr) in most AWS
regions.  _(Configuration uses `g4dn.xlarge` with T4 16GB GPU and Deep Learning
AMI GPU PyTorch 2.0.1 on Ubuntu 20.04, as defined in
`deploy.config.AWS_EC2_INSTANCE_TYPE`)_

## Modular Cloud Backends
OpenAdapter is designed with a modular backend structure to support multiple
cloud providers and frontier model APIs. Current backends include:
- **AWS**: For deploying on EC2, with options for instance types, storage, and
security settings.
- **Hugging Face Inference API**: For deploying models directly on Hugging
Face’s infrastructure, suitable for lighter workloads and models.
- **Anthropic/OpenAI APIs**: Seamless integration with remote model inference
on Anthropic and OpenAI’s systems, extending capabilities to hosted large
language models.

## Integrations
This project is intended for openadapt-agnostic deployments but also serves as
a complementary tool for OpenAdaptAI's
[OpenAdapt](https://github.com/OpenAdaptAI/OpenAdapt) project. It can be
customized to suit various automation, data processing, or model inference
applications beyond OpenAdapt, providing a standalone, scalable solution for
deploying SOTA models.

## Contributing
Coming soon.

## License
OpenAdapter is licensed under the MIT License. See [LICENSE](./LICENSE) for more details.
