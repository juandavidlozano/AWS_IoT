import boto3
import logging

# Initialize the logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Define the client outside of the handler function so it can be reused
glue_client = boto3.client('glue')

def lambda_handler(event, context):
    # name of your Glue crawler
    crawler_name = 's3_crawler'
    
    try:
        # Start the Glue crawler
        response = glue_client.start_crawler(Name=crawler_name)
        logger.info(f"Started Glue crawler: {crawler_name}")
    except glue_client.exceptions.EntityNotFoundException:
        logger.error(f"Glue crawler {crawler_name} not found.")
        raise
    except glue_client.exceptions.CrawlerRunningException:
        logger.info(f"Glue crawler {crawler_name} is already running.")
    except Exception as e:
        logger.error(f"Error starting Glue crawler {crawler_name}: {str(e)}")
        raise
    
    return {
        'statusCode': 200,
        'body': f"Triggered Glue crawler: {crawler_name}"
    }
