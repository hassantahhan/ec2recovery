import os
import json
import boto3
import decimal
import datetime

check_last_result = {}
check_refresh_seconds = 300  # 5 minutes
check_last_update = datetime.datetime.now()

def handler_name(event, context):
    return get_ec2_recovery_stats(context.invoked_function_arn.split(':')[4])

def get_ec2_recovery_stats(check_account_id):
    global check_last_result
    global check_refresh_seconds
    global check_last_update

    if os.environ.get('CHECK_REFRESH_SECONDS'):
        check_refresh_seconds = os.environ.get('CHECK_REFRESH_SECONDS')

    elapsed_seconds = (datetime.datetime.now() - check_last_update).total_seconds()

    if len(check_last_result) == 0 or elapsed_seconds > check_refresh_seconds:
        check_last_update = datetime.datetime.now()
        check_last_result = refresh_ec2_recovery_stats(check_account_id, check_last_update)
            
    return check_last_result

def refresh_ec2_recovery_stats(check_account_id, check_last_update):
    running_instances = list_running_instances()
    auto_scaling_instances = list_auto_scaling_instances()
    alarm_instances = list_alarm_instances(auto_scaling_instances)

    instance_counts = {
        'running_instance_count': len(running_instances),
        'auto_scaling_group_instance_count': len(auto_scaling_instances),
        'cloud_watch_alarm_instance_count': len(alarm_instances)
    }

    try:
        decimal.getcontext().prec = 3
        overall_recovery_ratio = decimal.Decimal(len(alarm_instances) + len(auto_scaling_instances)) / decimal.Decimal(len(running_instances))
        auto_scaling_ratio = decimal.Decimal(len(auto_scaling_instances)) / decimal.Decimal(len(running_instances))
        alarm_recovery_ratio = decimal.Decimal(len(alarm_instances)) / decimal.Decimal(len(running_instances))
    except:
        overall_recovery_ratio = 0.0
        auto_scaling_ratio = 0.0
        alarm_recovery_ratio = 0.0

    recovery_ratios = {
        'overall_recovery_ratio': overall_recovery_ratio,
        'auto_scaling_group_recovery_ratio': auto_scaling_ratio,
        'cloud_watch_alarm_recovery_ratio': alarm_recovery_ratio
    }

    body = {
        'check_status_code': 200,
        'check_account_id': check_account_id,
        'check_last_update': check_last_update,
        'ec2_instance_counts': instance_counts,
        'ec2_recovery_ratios': recovery_ratios
    }

    return json.dumps(body, indent=3, sort_keys=True, default=default_formatter)

def list_running_instances():
    client = boto3.client('ec2')
    result = client.describe_instances(
        Filters=[{
            'Name': 'instance-state-name',
            'Values': ['running']}],
        MaxResults=1000
    )

    while 'NextToken' in result:
        next_result = client.describe_instances(
            Filters=[{
                'Name': 'instance-state-name',
                'Values': ['running']}],
            MaxResults=1000,
            NextToken=result['NextToken']
        )
        next_result['Reservations'].extend(result['Reservations'])
        result = next_result

    instance_list = []
    for reservation in (result['Reservations']):
        for instance in reservation['Instances']:
            instance_list.append(instance['InstanceId'])

    return instance_list

def list_auto_scaling_instances():
    client = boto3.client('autoscaling')
    result = client.describe_auto_scaling_groups()

    while 'NextToken' in result:
        next_result = client.describe_auto_scaling_groups(NextToken=result['NextToken'])
        next_result['AutoScalingGroups'].extend(result['AutoScalingGroups'])
        result = next_result

    instance_list = []
    for group in (result['AutoScalingGroups']):
        for instance in group['Instances']:
            if instance['InstanceId'] not in instance_list:
                instance_list.append(instance['InstanceId'])

    return instance_list

def list_alarm_instances(ignore_list):
    client = boto3.client('cloudwatch')
    result = client.describe_alarms()

    while 'NextToken' in result:
        next_result = client.describe_alarms(NextToken=result['NextToken'])
        next_result['MetricAlarms'].extend(result['MetricAlarms'])
        result = next_result

    instance_list = []
    for alarm in (result['MetricAlarms']):
        if 'StatusCheckFailed' in alarm['MetricName']:
            for dimension in alarm['Dimensions']:
                if dimension['Value'] not in instance_list and dimension['Value'] not in ignore_list:
                    instance_list.append(dimension['Value'])

    return instance_list

def default_formatter(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    elif isinstance(obj, datetime.datetime):
        return obj.isoformat()
    raise TypeError