import boto3
from datetime import datetime, timedelta

client = boto3.client('ce')

# staring time: current day minus 90 days, i.e. 90 days ago is the start time
start_Date = (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')
print(start_Date)

# end time
end_date = datetime.now().strftime('%Y-%m-%d')
print(end_date)

# calculating costs:
response = client.get_cost_and_usage(
    TimePeriod={
        'Start': start_Date, 
        'End': end_date
    },
    Granularity= 'MONTHLY',
    Metrics=['UnblendedCost', 'UsageQuantity']
)

for item in response['ResultsByTime']:
    print(item['TimePeriod'], "\n", item['Total']['UnblendedCost'], "\n")

# get all services used in the start and end time period
response_service = client.get_dimension_values(
    TimePeriod={
        'Start': start_Date, 
        'End': end_date
    },
    Dimension='SERVICE'
)

for service in response_service['DimensionValues']:
    print(service['Value'])

# get cost per service
response_services = client.get_cost_and_usage(
    TimePeriod={
        'Start': start_Date,
        'End': end_date
    },
    Granularity='MONTHLY',
    Metrics=['UnblendedCost'],
    GroupBy=[
        {
            'Type': 'DIMENSION',
            'Key': 'SERVICE'
        }
    ]
)

for item in response_services['ResultsByTime']:
    print(item['TimePeriod'])
    print('\n')
    for group in item['Groups']:
        service_name = group['Keys'][0]
        cost = group['Metrics']['UnblendedCost']['Amount']
        print(f"{service_name}: ${cost}")
        print('\n')

# forecast costs
start_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
end_date =  (datetime.now() + timedelta(days=31)).strftime('%Y-%m-%d')

response_forecast = client.get_cost_forecast(
    TimePeriod={
        'Start': start_date,
        'End': end_date
    },
    Metric='UNBLENDED_COST',
    Granularity='MONTHLY'
)

print(f"Start date: {start_date} | End date: {end_date}")
print(response_forecast)