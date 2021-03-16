## Overview
This is an AWS Lambda function that can help you check the EC2 fault tolerance state in your AWS account. The check counts EC2 instances that are configured with CloudWatch auto recovery alarms and EC2 instances associated with Auto Scaling Groups. It reports the EC2 recovery ratio across all EC2 instances in running status hosted in the same AWS account where the the lambda function is deployed.

## Amazon EC2 Auto Scaling Groups 
Auto Scaling Groups can help you automatically manage your scalability and resilency needs across Availability Zones in a single Region. Follow the link below to know more about why and how to associate your EC2 instances with Auto Scaling Groups
https://docs.aws.amazon.com/autoscaling/ec2/userguide/AutoScalingGroup.html

## Automatic Recovery using CloudWatch Alarms
Alternatively to Auto Scaling Groups, CloudWatch alarms can help you recover from a failed status check in a single Availability Zone. Follow the link below to know more about how to configure your EC2 instances with CloudWatch automatic recovery alarms
https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/UsingAlarmActions.html
