## Overview
Do you know how much EC2 resiliency you have built in your AWS account? Do you know how many EC2 instances in your environment can recover from an underlying host issue or corrupted file system?<br/>

This is an AWS Lambda function written in Python that can help you gauge the EC2 fault tolerance in your AWS account. The check counts EC2 instances that are configured with CloudWatch auto recovery alarms and EC2 instances associated with Auto Scaling Groups. It reports the EC2 recovery ratio across all EC2 instances in running status hosted in the same AWS account and AWS region where the the Lambda function is deployed.<br/>

EC2 Auto Scaling Groups are a better option to use than CloudWatch automatic recovery alarms, because the former can offer resiliency across Availability Zones. In all cases, the two recovery mechanisms should not be used together. Hence, if the Lambda function finds an EC2 instance to be associated with an Auto Scaling Group, then it ignores the state of its CloudWatch alarm configuration.

## Deployment
I deployed the Lambda function in my AWS test account using https://www.serverless.com/ and provided the serverless.yml for your reference. However, you can choose to deployed using any other preferred option such as AWS CodeDeploy or AWS CloudFormation.<br/>
Alternatively, you can follow the link below to deploy the Lambda function as a .zip file archive.<br/>
Reference link: https://docs.aws.amazon.com/lambda/latest/dg/python-package.html

## Environment
The Lambda function has no external dependencies other than Python 3.8. The suggested access level is the AmazonEC2ReadOnlyAccess managed policy. The suggested timeout limit is 10 seconds. The function can be configured with an optional environment variable (CHECK_REFRESH_SECONDS) to control the cache refresh rate, which is set to 5 minutes by default. 

## Testing
The core logic (other than the handler method) can be tested locally without the need for Lambda deployment. I provided two files (test.py and requirements.txt) to help you install and run the EC2 resiliency check locally. You still need to have your AWS access credentials in .aws\credentials for the test script to work. 

## Cost
The total cost of the Lambda function is estimated to be $0.01 USD/month, when the Lambda free usage tier is not included. 

## Output
Find below a sample of the Lambda function output
```
{
   "check_account_id": "111111111111",
   "check_last_update": "2021-03-17T00:28:00.219935",
   "check_region_code": "ap-southeast-2",
   "check_status_code": 200,
   "ec2_instance_counts": {
      "auto_scaling_group_instance_count": 5,
      "cloud_watch_alarm_instance_count": 1,
      "running_instance_count": 7
   },
   "ec2_recovery_ratios": {
      "auto_scaling_group_recovery_ratio": 0.714,
      "cloud_watch_alarm_recovery_ratio": 0.143,
      "overall_recovery_ratio": 0.857
   }
}
```
## Regional Resiliency using Auto Scaling Groups 
Auto Scaling Groups can help you automatically manage your scalability and resiliency across multiple Availability Zones in a single Region. Follow the link below to know more about why and how to associate your EC2 instances with Auto Scaling Groups.<br/>
Reference link: https://docs.aws.amazon.com/autoscaling/ec2/userguide/AutoScalingGroup.html

## Zonal Recovery using CloudWatch Alarms
Alternatively to Auto Scaling Groups, CloudWatch alarms can help you recover from a failed status check in a single Availability Zone. Follow the link below to know more about how to configure your EC2 instances with CloudWatch automatic recovery alarms.<br/>
Reference link: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/UsingAlarmActions.html
