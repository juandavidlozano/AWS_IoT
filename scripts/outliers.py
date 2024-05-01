import boto3
import pandas as pd
from io import BytesIO
from sklearn.ensemble import IsolationForest
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import base64

plt.ioff()

# Replace 'your-data-bucket' with the actual name of your data bucket
data_bucket = 'sensor-data-jdl'
# This is the bucket name where the HTML file will be saved, as per your screenshot
output_bucket = 'htlm-outliers'

def find_latest_file():
    """ Function to find the latest file in the specified bucket """
    s3 = boto3.client('s3')
    paginator = s3.get_paginator('list_objects_v2')
    page_iterator = paginator.paginate(Bucket=data_bucket)

    latest = None
    for page in page_iterator:
        if 'Contents' in page:
            latest = max(page['Contents'], key=lambda x: x['LastModified'])
    if latest:
        return latest['Key']
    return None

def detect_outliers_s3():
    # Find the latest file in the data bucket
    key = find_latest_file()
    if not key:
        return "No files found in bucket."

    # Create an S3 client
    s3 = boto3.client('s3')
    
    # Fetch the file from S3
    response = s3.get_object(Bucket=data_bucket, Key=key)
    data_bytes = response['Body'].read()
    
    # Load the data into a pandas DataFrame
    data = pd.read_parquet(BytesIO(data_bytes))
    
    # Assuming 'data' is a column with a struct type with nested fields
    if 'data' in data.columns:
        data = pd.concat([data.drop(['data'], axis=1), data['data'].apply(pd.Series)], axis=1)

    if 'reservoir_pressure_per_second' in data.columns:
        iso = IsolationForest(contamination=0.1)
        data['outlier'] = iso.fit_predict(data[['reservoir_pressure_per_second']].values.reshape(-1, 1))

    # Plotting
    plt.figure(figsize=(10, 6))
    sns.lineplot(x=data.index, y='reservoir_pressure_per_second', data=data, marker='o', label='Pressure', color='blue')
    outliers = data[data['outlier'] == -1]
    plt.scatter(outliers.index, outliers['reservoir_pressure_per_second'], color='red', label='Outliers', s=100, edgecolor='black')
    plt.title('Reservoir Pressure Over Time with Outliers Highlighted')
    plt.xlabel('Index')
    plt.ylabel('Reservoir Pressure per Second')
    plt.legend()
    plt.grid(True)

    img_data = BytesIO()
    plt.savefig(img_data, format='png')
    img_data.seek(0)
    image_base64 = base64.b64encode(img_data.read()).decode('utf-8')
    image_html = f'<img src="data:image/png;base64,{image_base64}" />'

    # Convert HTML to bytes
    html_bytes = image_html.encode('utf-8')
    html_key = f'outlier-visualization-{datetime.utcnow().isoformat()}.html'

    # Save HTML to the 'htlm-outliers' bucket
    s3.put_object(Bucket=output_bucket, Key=html_key, Body=html_bytes, ContentType='text/html')
    
    print(f"HTML visualization saved to s3://{output_bucket}/{html_key}")


if __name__ == "__main__":
    detect_outliers_s3()
