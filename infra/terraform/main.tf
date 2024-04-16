provider "aws" {
  region = "us-east-1"  # Replace with your preferred AWS region
}

module "lambda_function" {
  source = "./lambda"
  # Pass any required variables if needed
}
