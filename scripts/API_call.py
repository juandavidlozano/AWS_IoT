import boto3
import json
import time
from datetime import datetime, timezone

athena_client = boto3.client('athena')
s3_client = boto3.client('s3')

def find_latest_result_file(bucket):
    # List objects in the root folder of the bucket
    response = s3_client.list_objects_v2(
        Bucket=bucket
    )

    # Find the most recent CSV file based on LastModified attribute
    csv_files = [obj for obj in response.get('Contents', []) if obj['Key'].endswith('.csv')]
    if not csv_files:
        raise ValueError("No CSV files found in the specified bucket.")
    
    latest_file = max(csv_files, key=lambda obj: obj['LastModified'])

    return latest_file['Key']

def lambda_handler(event, context):
    # Your Athena query
    query = """
    SELECT
      timestamp,
      barrels_per_second AS barrels_per_second,
      reservoir_pressure_per_second AS reservoir_pressure_per_second
    FROM
      "s3_crawler_database"."sensor_data_jdl"
    ORDER BY
      timestamp DESC
    LIMIT 10;
    """

    # Start the Athena query execution
    response = athena_client.start_query_execution(
        QueryString=query,
        QueryExecutionContext={
            'Database': 's3_crawler_database'
        },
        ResultConfiguration={
            'OutputLocation': 's3://athena-query-result-jdl/'
        }
    )
    
    query_execution_id = response['QueryExecutionId']
    
    # Athena is asynchronous, so wait for the query to complete
    while True:
        query_status = athena_client.get_query_execution(QueryExecutionId=query_execution_id)
        query_execution_status = query_status['QueryExecution']['Status']['State']
        if query_execution_status == 'SUCCEEDED':
            break
        if query_execution_status in ['FAILED', 'CANCELLED']:
            return {'statusCode': 500, 'body': 'Query Failed'}
        time.sleep(1)  # Simple sleep; use exponential backoff in production
    
    # Athena query has succeeded, now fetch the latest results file
    result_file_key = find_latest_result_file('athena-query-result-jdl')

    # Fetch the results from the latest result file
    result_object = s3_client.get_object(Bucket='athena-query-result-jdl', Key=result_file_key)
    result_content = result_object['Body'].read().decode('utf-8')

    # Convert the CSV result to JSON
    # Assumes first line is headers
    lines = result_content.split('\n')
    headers = lines[0].split(',')
    data = [dict(zip(headers, line.split(','))) for line in lines[1:] if line]

    return {
        'statusCode': 200,
        'body': json.dumps(data),
        'headers': {
            'Content-Type': 'application/json'
        }
    }
