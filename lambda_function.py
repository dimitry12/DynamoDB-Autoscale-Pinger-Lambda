import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
import boto3
import uuid

def lambda_handler(event, context):
    client = boto3.client('dynamodb')
    
    for table_name in client.list_tables()['TableNames']:
        logging.info('Pinging table `%s`..' % table_name)
        
        key_field = client.describe_table(TableName=table_name)['Table']['KeySchema'][0]['AttributeName']
        logging.info('Found key `%s` in table `%s`.' % (key_field,table_name))
        
        random_value = str(uuid.uuid4())
        
        table = boto3.resource('dynamodb').Table(table_name)
        # generating read
        table.get_item(
            Key={
                key_field: random_value
            }
        )
        logging.info('Performed read on table `%s`.' % table_name)
        # generating write
        table.delete_item(
            Key={
                key_field: random_value
            }
        )
        logging.info('Performed write on table `%s`.' % table_name)
        
    return 'Hello from Lambda'
