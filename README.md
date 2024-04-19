# AWS IoT
This repository contains the code for a live IoT streaming and analysis application.


<img src="https://github.com/juandavidlozano/AWS_IoT/blob/main/pics/Flow.jpg" alt="Answer 1" width="1000" height="500">


## Detailed AWS Data Pipeline Overview

This pipeline integrates various AWS services to handle real-time sensor data processing with subsequent batch analysis capabilities. The architecture is designed to facilitate the ingestion, processing, visualization, and storage of data with high reliability and scalability.

### Components of the Pipeline

#### 1. **AWS S3 Bucket**
- **Purpose**: Stores sensor data files in a structured time-based format.
- **Data Format**: Files are stored in Parquet format within time-partitioned directories.
- **Benefits**: Provides durable, scalable, and secure storage for massive datasets.

#### 2. **AWS IoT Core**
- **Purpose**: Acts as the entry point for data transmitted by IoT sensors.
- **Benefits**: Securely connects devices to the cloud, facilitating reliable and efficient data transfer.

#### 3. **Amazon Kinesis Data Streams**
- **Purpose**: Streams sensor data in real-time, enabling immediate processing and analysis.
- **Benefits**: Supports high-throughput, real-time data streaming, and seamless data intake without bottlenecks.

#### 4. **Real-time Data Visualization Webpage**
- **Purpose**: Visualizes streaming data in real-time to provide instant insights from sensor outputs.
- **Benefits**: Enhances operational awareness and decision-making through immediate data visibility.

#### 5. **Amazon Kinesis Data Firehose**
- **Purpose**: Transfers streaming data into AWS S3, converting data from JSON to Parquet.
- **Benefits**: Automates data loading to S3, optimizing for cost-efficiency and query performance.

#### 6. **AWS Lambda**
- **Purpose**: Triggered by new data arrival in S3, it initiates a Glue crawler to update data schemas in the Glue Catalog.
- **Benefits**: Offers a serverless execution model to run code in response to events, reducing operational overhead and costs.

#### 7. **AWS Glue Crawler**
- **Purpose**: Updates the AWS Glue Data Catalog with new data schemas and partitions.
- **Benefits**: Automates the management of metadata, facilitating organized data analysis and accessibility.

#### 8. **AWS Glue Data Catalog**
- **Purpose**: Maintains a central repository of metadata for managed data assets.
- **Benefits**: Simplifies data management, enhances discoverability, and supports seamless integration with analytical tools.

#### 9. **API for On-demand Athena Query**
- **Purpose**: Provides an interface for executing SQL queries against stored data via Amazon Athena.
- **Benefits**: Allows flexible, ad-hoc querying of data through a simple API endpoint, enhancing data accessibility for applications.

#### 10. **Amazon Athena**
- **Purpose**: Executes SQL queries against the data stored in S3 using the Glue Data Catalog.
- **Benefits**: Provides serverless querying, reducing the need for complex ETL setups and lowering query costs.

### Pipeline Benefits
- **Scalability**: Handles large-scale data processing without degradation in performance.
- **Cost Efficiency**: Minimizes costs through serverless architectures and managed services, paying only for what is used.
- **Real-time and Batch Processing**: Combines real-time data processing with comprehensive batch analytics for deep insights.
- **Data Accessibility**: Enhances data-driven decision-making through flexible access to processed data.
