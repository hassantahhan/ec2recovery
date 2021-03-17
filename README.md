## Overview
This is an AWS Lambda function written in Python that can help you check the EC2 fault tolerance state in your AWS account. The check counts EC2 instances that are configured with CloudWatch auto recovery alarms and EC2 instances associated with Auto Scaling Groups. It reports the EC2 recovery ratio across all EC2 instances in running status hosted in the same AWS account where the the Lambda function is deployed

## Deployment
I developed and deployed this function using https://www.serverless.com/. But you can choose to deployed using any other preferred options such as AWS CodeDeploy or AWS CloudFormation. Alternatively, you can follow the link below to deploy the Lambda function as a .zip file archive
https://docs.aws.amazon.com/lambda/latest/dg/python-package.html

## Output
Find below a sample of data resturned by the Lambda function
```
{
   "check_account_id": "111111111111", 
   "check_last_update": "2021-03-17T00:28:00.219935", 
   "check_status_code": 200, 
   "ec2_instance_counts": {
      "Auto_Scaling_group_instance_count": 5, 
      "cloud_watch_alarm_instance_count": 1, 
      "running_instance_count": 7
   }, 
   "ec2_recovery_ratios": {
      "auto_scaling_group_recovery_ratio": 0.71, 
      "cloud_watch_alarm_recovery_ratio": 0.14, 
      "overall_recovery_ratio": 0.86
   }
}
```
## Regional Scalability using Auto Scaling Groups 
Auto Scaling Groups can help you automatically manage your scalability and resilency needs across Availability Zones in a single Region. Follow the link below to know more about why and how to associate your EC2 instances with Auto Scaling Groups
https://docs.aws.amazon.com/autoscaling/ec2/userguide/AutoScalingGroup.html

## Zonal Recovery using CloudWatch Alarms
Alternatively to Auto Scaling Groups, CloudWatch alarms can help you recover from a failed status check in a single Availability Zone. Follow the link below to know more about how to configure your EC2 instances with CloudWatch automatic recovery alarms
https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/UsingAlarmActions.html
