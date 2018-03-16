# DynamoDB Autoscale Pinger Lambda

AWS DynamoDB autoscaler fails to scale read/write capacity down if **no** activity is present. In other words, if a burst of activity is followed by an abrupt end of any reads and writes - then AWS DynamoDB will remain forever with lots of read- and write-capacity, and it gets expensive.

I trigger this Lambda every minute using CW Event.

It requires the following IAM policy:
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "dynamodb:ListTables",
                "dynamodb:DescribeTable",
                "dynamodb:DeleteItem",
                "dynamodb:Query"
            ],
            "Resource": "*"
        }
    ]
}
```
