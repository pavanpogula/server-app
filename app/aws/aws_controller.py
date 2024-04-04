import sys
sys.path.append(sys.path[0] + "/app/aws")
import os
from boto3 import resource
from botocore.exceptions import NoRegionError, NoCredentialsError
from dotenv import load_dotenv

load_dotenv()
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY_ID = os.getenv('AWS_SECRET_ACCESS_KEY_ID')
REGION_NAME = os.getenv('REGION_NAME')



try:
  
    
    table_resource = resource(
        'dynamodb',
        aws_access_key_id=AWS_SECRET_ACCESS_KEY,
      aws_secret_access_key =AWS_SECRET_ACCESS_KEY_ID,
        
        region_name=REGION_NAME
    )
    
    # To access or modify the table's entries, we have to get the table using the resource
    user_table = table_resource.Table('user_table')

except NoRegionError:
    print("No AWS region specified. Please provide a valid AWS region.")
    # Handle the exception appropriately, e.g., logging, raising a custom exception, etc.

except NoCredentialsError:
    print("AWS credentials not found. Please provide valid AWS credentials.")
    # Handle the exception appropriately, e.g., logging, raising a custom exception, etc.

# This function should be defined outside the try-except block to handle exceptions gracefully.
def get_items_all():
    try:
        response = user_table.scan()
        return response
    except Exception as e:
        print("An error occurred while scanning the DynamoDB table:", e)
        # Handle the exception appropriately, e.g., logging, returning a custom error response, etc.
        return None
