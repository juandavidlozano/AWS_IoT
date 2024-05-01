#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import sys
import time
import random
import json
import argparse
from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder

# Function to parse command-line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description="Simulator Arguments")
    parser.add_argument('--endpoint', required=True, help="Your AWS IoT custom endpoint")
    parser.add_argument('--ca_file', required=True, help="CA file path")
    parser.add_argument('--cert', required=True, help="Certificate file path")
    parser.add_argument('--key', required=True, help="Private key file path")
    parser.add_argument('--client_id', required=True, help="MQTT client ID")
    parser.add_argument('--topic', required=True, help="MQTT topic")
    
    return parser.parse_args()

# Establish an MQTT connection
def establish_connection(args):
    event_loop_group = io.EventLoopGroup(1)
    host_resolver = io.DefaultHostResolver(event_loop_group)
    client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)
    
    mqtt_connection = mqtt_connection_builder.mtls_from_path(
        endpoint=args.endpoint,
        cert_filepath=args.cert,
        pri_key_filepath=args.key,
        client_bootstrap=client_bootstrap,
        ca_filepath=args.ca_file,
        client_id=args.client_id,
        clean_session=False,
        keep_alive_secs=6
    )
    
    print("Connecting to {} with client ID '{}'...".format(
        args.endpoint, args.client_id))
    
    connected_future = mqtt_connection.connect()
    
    # Wait for connection to be fully established.
    connected_future.result()
    return mqtt_connection

OUTLIER_PROBABILITY = 0.05  # 5% chance to generate an outlier
OUTLIER_MULTIPLIER = 10  # Outliers will be 10 times the normal value

def generate_barrels_per_second():
    if random.random() < OUTLIER_PROBABILITY:
        # Generate an outlier
        return random.uniform(500, 1000) * OUTLIER_MULTIPLIER
    else:
        # Simulating normal barrels per second between 500 and 1000
        return random.uniform(500, 1000)

def generate_reservoir_pressure_per_second():
    if random.random() < OUTLIER_PROBABILITY:
        # Generate an outlier
        return random.uniform(1000, 2000) * OUTLIER_MULTIPLIER
    else:
        # Simulating normal reservoir pressure per second between 1000 and 2000 psi
        return random.uniform(1000, 2000)



# Main function to generate and publish dummy data
def main():
    args = parse_arguments()
    mqtt_connection = establish_connection(args)
    
    print("Connected!")

    while True:
        # Generate dummy data for barrels per second and reservoir pressure per second
        barrels_per_second = generate_barrels_per_second()
        reservoir_pressure_per_second = generate_reservoir_pressure_per_second()
        
        # Create a dictionary to store the generated data with metadata
        data = {
            "timestamp": int(time.time()),  # Current timestamp in seconds
            "barrels_per_second": barrels_per_second,  # Flattened structure
            "reservoir_pressure_per_second": reservoir_pressure_per_second  # Flattened structure
        }

        json_data = json.dumps(data)
        print("Publishing: {}".format(json_data))
        mqtt_connection.publish(
            topic=args.topic,
            payload=json_data,
            qos=mqtt.QoS.AT_LEAST_ONCE)
        time.sleep(1)

    # Disconnect from AWS IoT
    print("Disconnecting...")
    disconnect_future = mqtt_connection.disconnect()
    disconnect_future.result()

if __name__ == "__main__":
    main()

