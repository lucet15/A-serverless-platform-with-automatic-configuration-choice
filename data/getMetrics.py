import boto3
import pandas as pd
import sys
import datetime


def getMetrics(faasFunction, instante, memory, cpu, input):

    # Create a CloudWatch client
    cloudwatch = boto3.client('cloudwatch')

    print(cloudwatch)

    # Define the metric parameters
    namespace = 'AWS/LoadBalancer'
    dimensions = [
        {
            'Name': 'ApiName',
            'Value': 'gateway-external'
        },
        {
            'Name': 'FunctionName',
            'Value': faasFunction
        }
    ]
    statistics = ['Average']
    period = 3600 * 5
    start_time = datetime.datetime.now() - datetime.timedelta(seconds=period)
    end_time = datetime.datetime.now()

    # Define the metrics to retrieve
    metrics = [
        'response-time',
        'DNS+dialup',
        'DNS',
        'Request-write',
        'Response-delay',
        'Response-read',
        'status-code',
        'offset'
    ]

    # Get the CloudWatch metrics
    response = cloudwatch.get_metric_data(
        MetricDataQueries=[
            {
                'Id': 'metric1',
                'MetricStat': {
                    'Metric': {
                        'Namespace': namespace,
                        'MetricName': metrics[0],
                        'Dimensions': dimensions
                    },
                    'Period': period,
                    'Stat': statistics[0]
                }
            },
            # Repeat the above block for each metric in the 'metrics' list
            # with a unique 'Id' and 'MetricStat' configuration
        ],
        StartTime=start_time,
        EndTime=end_time
    )

    # Extract the metric data points
    datapoints = response['MetricDataResults'][0]['Timestamps']
    metric_values = response['MetricDataResults'][0]['Values']

    print(datapoints)
    print(metric_values)

    # Create a list of dictionaries containing the metric data
    metrics_data = []
    for i in range(len(datapoints)):
        metric = {
            'Timestamp': datapoints[i],
            'MetricValue': metric_values[i]
        }
        metrics_data.append(metric)

    # Create a pandas DataFrame from the metrics data
    df = pd.DataFrame(metrics_data)

    # Save the DataFrame to a CSV file
    df.to_csv("metrics/" + faasFunction + "_" + input + "_" + memory + "_" + cpu + ".csv", index=False)


def main():

    # Parse the information
    faasFunction = sys.argv[1]
    instance = sys.argv[2]
    memory = sys.argv[3]
    cpu = sys.argv[4]
    input = sys.argv[5]

    getMetrics(faasFunction, instance, memory, cpu, input)



if __name__ == "__main__":
    main()