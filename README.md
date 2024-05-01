# AWS IoT
This repository contains the code for a live IoT streaming and analysis application.


<img src="https://github.com/juandavidlozano/AWS_IoT/blob/main/pics/Flow1.jpg" alt="Answer 1" width="1000" height="500">


## Detailed Pipeline Overview

This pipeline integrates various AWS services to handle real-time sensor data processing with subsequent batch analysis capabilities. The architecture is designed to facilitate the ingestion, processing, visualization, and storage of data with high reliability and scalability.

1. **Sensor Data Simulation**
   - **Tool**: Custom Python Script.
   - **Purpose**: Simulates real-time sensor data, including timestamps, barrels per second, and reservoir pressure per second. This simulates real-world IoT devices transmitting data.

2. **AWS IoT Core**
   - **Tool**: AWS IoT Core.
   - **Purpose**: Receives data transmitted by sensors (simulated by your Python script). It acts as a managed cloud platform that lets connected devices easily and securely interact with cloud applications and other devices.
   - **Benefits**: Provides secure data ingestion from millions of devices, scales automatically, and routes data to AWS services like Kinesis for further processing.

3. **Amazon Kinesis Data Streams**
   - **Tool**: Amazon Kinesis Data Streams.
   - **Purpose**: Consumes the streamed data from IoT Core, enabling real-time data processing and analysis.
   - **Benefits**: Capable of handling a high throughput of data, ensuring that data ingestion is not a bottleneck. Facilitates real-time data analytics.

4. **Real-time Data Visualization Webpage**
   - **Tool**: Custom Web Application.
   - **Purpose**: Subscribes to the Kinesis stream to display data in real-time, giving stakeholders immediate insight into sensor outputs.
   - **Benefits**: Provides instant visualization and monitoring, which can be crucial for operational adjustments and immediate decision-making.
   - **Security and Access Control**:
     - **Tool**: Amazon Cognito.
     - **Purpose**: Manages user authentication and access control for the real-time data visualization webpage.
     - **Benefits**: Ensures that only authenticated users can access the real-time data. Cognito integrates seamlessly with other AWS services, providing a secure and scalable way to handle user authentication and access rights. Users can authenticate using their existing corporate credentials or through social identities, managed in a unified system that adheres to security best practices.

5. **Amazon Kinesis Data Firehose**
   - **Tool**: Amazon Kinesis Data Firehose.
   - **Purpose**: Automatically loads streaming data from Kinesis Data Streams into S3, converting JSON format to Parquet, and organizing data into partitions by year, month, day, and hour.
   - **Benefits**: Seamless integration with S3 and automatic data transformation enhances query performance while reducing storage costs due to the columnar storage format (Parquet).

6. **AWS S3**
   - **Tool**: Amazon S3.
   - **Purpose**: Acts as a data lake to store processed data in Parquet format, organized in a time-partitioned structure.
   - **Benefits**: Provides durable, highly available, and scalable storage. Partitioning enhances data organization and speeds up query performance.

7. **AWS Lambda**
   - **Tool**: AWS Lambda.
   - **Purpose**: Triggered by S3 put events (when new files are saved by Firehose), it starts an AWS Glue crawler to update the metadata of the new data in the Glue Catalog.
   - **Benefits**: Provides serverless execution of backend processes, reducing management overhead and cost by running code in response to events.

8. **AWS Glue Crawler**
   - **Tool**: AWS Glue Crawler.
   - **Purpose**: Updates the AWS Glue Data Catalog with the latest data schema and partitions based on the new data files stored in S3.
   - **Benefits**: Automates the process of cataloging and organizing data, making it readily available for querying and analysis without manual intervention.

9. **AWS Glue Data Catalog**
   - **Tool**: AWS Glue Data Catalog.
   - **Purpose**: Serves as a central metadata repository for all the data assets stored in S3, with updated schema and partition information.
   - **Benefits**: Enables a unified metadata repository that simplifies management and enhances data discovery for analytics across multiple services like Athena.

10. **API for On-demand Athena Query**
    - **Tool**: Amazon API Gateway + AWS Lambda.
    - **Purpose**: The API, upon being called, triggers a Lambda function that executes an SQL query using Amazon Athena against the data cataloged in Glue.
    - **Benefits**: Provides a way to perform ad-hoc, complex querying through a simple API endpoint, making data accessible programmatically for applications or end-users.

11. **Amazon Athena**
    - **Tool**: Amazon Athena.
    - **Purpose**: Runs serverless queries against the data stored in S3 using standard SQL, leveraging the catalog maintained by AWS Glue.
    - **Benefits**: Offers fast, cost-effective, and serverless querying capabilities without the need to set up complex ETL jobs for analytical queries.

12. **AWS Elastic Container Registry (ECR)**
    - **Tool**: Amazon Elastic Container Registry (ECR).
    - **Purpose**: Provides a Docker container registry for storing, managing, and deploying Docker container images.
    - **Benefits**: Enables reliable and secure storage for container images, simplifying the development to production workflow by integrating seamlessly with ECS for easy deployment of containerized applications.

13. **AWS Elastic Container Service (ECS)**
    - **Tool**: Amazon Elastic Container Service (ECS).
    - **Purpose**: Manages the deployment and scaling of containerized applications using Docker containers.
    - **Benefits**: Automates the management of containerized applications, supports both ECS and Fargate to run containers without having to manage servers or clusters, and integrates with AWS infrastructure services like load balancing and security.

14. **Kinesis Analytics with Apache Flink**
    - **Tool**: Amazon Kinesis Analytics (with Apache Flink).
    - **Purpose**: Allows for complex real-time data processing and analytics using Apache Flink on the data streamed through Amazon Kinesis.
    - **Benefits**: Supports sophisticated stream processing capabilities such as event time processing, window functions, and state management. Enables users to deploy custom Flink applications directly into a managed Kinesis environment for real-time analytics.

15. **Integration of ECS with S3 Events**
    - **Tool**: AWS Lambda (trigger), Amazon ECS.
    - **Purpose**: Triggers ECS tasks based on events in S3 (e.g., file uploads to specific S3 buckets).
    - **Benefits**: Automates the processing of data stored in S3 by deploying Docker containers that can react to events, allowing for flexible and scalable data processing workflows.

   


### Pipeline Benefits

- **Scalability**: Each component is designed to scale with increased load, suitable for handling massive amounts of data without performance degradation.
- **Cost Efficiency**: Serverless and managed services reduce the overhead of infrastructure management and minimize cost by charging only for the resources used.
- **Real-time Processing and Batch Analysis**: Combines the benefits of real-time data stream processing with the deep insights provided by batch analytics.
- **Flexibility and Accessibility**: Data is accessible through various tools and interfaces, enhancing the ability to make data-driven decisions quickly.
