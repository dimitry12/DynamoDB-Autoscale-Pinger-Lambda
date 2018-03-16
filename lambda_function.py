import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
import boto3
import uuid
from boto3.dynamodb.conditions import Key

def ping_table_key(table_name, key_field, gsi_name=None):
    random_value = str(uuid.uuid4())
    
    table = boto3.resource('dynamodb').Table(table_name)
    # generating read
    if gsi_name is None:
        table.query(
            KeyConditionExpression=Key(key_field).eq(random_value)
        )
    else:
        table.query(
            IndexName=gsi_name,
            KeyConditionExpression=Key(key_field).eq(random_value)
        )
    logging.info('Performed read on table `%s` using key `%s`.' % (table_name, key_field))
    
    # generating write
    if gsi_name is None:
        table.delete_item(
            Key={
                key_field: random_value
            }
        )
        logging.info('Performed write on table `%s` using key `%s`.' % (table_name, key_field))
    else:
        pass

def lambda_handler(event, context):
    client = boto3.client('dynamodb')
    
    for table_name in client.list_tables()['TableNames']:
        logging.info('Pinging table `%s`..' % table_name)
        
        table_description = client.describe_table(TableName=table_name)       
        key_field = table_description['Table']['KeySchema'][0]['AttributeName']
        logging.info('Found key `%s` in table `%s`.' % (key_field,table_name))
        
        ping_table_key(table_name, key_field)
        
        for gsi in table_description['Table'].get('GlobalSecondaryIndexes',[]):
            gsi_name = gsi['IndexName']
            gsi_field = gsi['KeySchema'][0]['AttributeName']
            logging.info('Found GSI `%s` on field `%s` in table `%s`.' % (gsi_name,gsi_field,table_name))
            ping_table_key(table_name, gsi_field, gsi_name)
        
    return True
