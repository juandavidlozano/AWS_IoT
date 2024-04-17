# Provider configuration for AWS
provider "aws" {
  region = "us-east-1" # Change this to your desired region
}

# Create SNS topics
resource "aws_sns_topic" "temperature_sensor_topic" {
  name = "temperature_sensor_topic"
}

resource "aws_sns_topic" "humidity_sensor_topic" {
  name = "humidity_sensor_topic"
}

resource "aws_sns_topic" "pressure_sensor_topic" {
  name = "pressure_sensor_topic"
}

# Create SQS queues
resource "aws_sqs_queue" "temperature_sensor_queue" {
  name = "temperature_sensor_queue"
}

resource "aws_sqs_queue" "humidity_sensor_queue" {
  name = "humidity_sensor_queue"
}

resource "aws_sqs_queue" "pressure_sensor_queue" {
  name = "pressure_sensor_queue"
}

# Output SNS topic ARNs and SQS queue URLs
output "sns_topic_arns" {
  value = [
    aws_sns_topic.temperature_sensor_topic.arn,
    aws_sns_topic.humidity_sensor_topic.arn,
    aws_sns_topic.pressure_sensor_topic.arn
  ]
}

output "sqs_queue_urls" {
  value = [
    aws_sqs_queue.temperature_sensor_queue.id,
    aws_sqs_queue.humidity_sensor_queue.id,
    aws_sqs_queue.pressure_sensor_queue.id
  ]
}
