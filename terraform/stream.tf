provider "aws" {
  region = "eu-west-2" 
}

resource "aws_kinesis_stream" "guardian_content" {
  name             = "guardian_content"
  shard_count      = 1
  retention_period = 72  # Retention period in hours (3 days)
}