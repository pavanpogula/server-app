import sys,os
sys.path.append(sys.path[0]+"/app/aws")
from boto3 import resource
import os

AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY_ID= os.environ.get('AWS_SECRET_ACCESS_KEY_ID')
REGION_NAME = 'us-east-2'
 
table_resource = resource(
   'dynamodb',
   aws_access_key_id     = AWS_SECRET_ACCESS_KEY_ID,
   aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
   region_name           = REGION_NAME
)
#To access or modify the table’s entries, we have to get the table using the resource
user_table = table_resource.Table('user_table')

def get_items_all():
    response = user_table.scan()
    return response