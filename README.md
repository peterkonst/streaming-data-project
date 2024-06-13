# Streaming Data Project

## Overview

This project is a proof of concept for a streaming data application that retrieves articles from the Guardian API and publishes them to an AWS Kinesis stream. The articles can then be consumed and analyzed by other applications.

## Requirements

- Python 3.7+
- AWS Account
- Guardian API Key

## Installation and Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/streaming-data-project.git
   cd streaming-data-project
   ```

2. Createand activate your vritual environemnt:
    ```bash
   python -m venv venv
   source venv/bin/activate
    ```

3. Install the dependencies:

    ``` bash
    pip install -r requirements.txt
    ```
4. Set up your environemnt variables by creating a `.env` file in the root directory

    ``` bash
    GUARDIAN_API_KEY=your_guardian_api_key
    AWS_ACCESS_KEY_ID=your_aws_access_key_id
    AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
    AWS_DEFAULT_REGION=your_aws_region
    ```
5. Download and set up terraform:
    ``` bash
    terraform init
    terraform plan
    terraform apply
## Usage

1. Producer:

    The producer script retrieves articles from the Guardian API and published them to an AWS Kinesis Stream
    ``` bash
    python producer_consumer/producer.py
    ```
2. Consumer

    The consumer script reads records from the AWS Kinesis streama and prints them
    ``` bash
    python producer_consumer/consumer.py
    ```
## Testing

1. Make sure to set your PYTHONPATH
    ``` bash
    export PYTHONPATH=$(pwd)
    ```
2. Run the tests using `pytest`
    ``` bash
    pytest
    ```
