import json, boto3, uuid

sqs = boto3.resource('sqs', region_name="eu-central-1")

tweets = sqs.get_queue_by_name(QueueName='JUSTYNAsQUEUE')
response = tweets.send_message(MessageBody='Hello World', MessageAttributes={
    'Author': {
        'StringValue': 'Justyna',
        'DataType': 'String'
    }
})
