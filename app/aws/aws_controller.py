import sys
sys.path.append(sys.path[0] + "/app/aws")
import os
from boto3 import resource
from botocore.exceptions import NoRegionError, NoCredentialsError
from app.model import  UserRegisterSchema
from app.aws.utils import generate_random_data ,adjusted_data,generate_object_id
from dotenv import load_dotenv
import time
import random
import hashlib
from decimal import Decimal
load_dotenv()
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY_ID = os.getenv('AWS_SECRET_ACCESS_KEY_ID')
REGION_NAME = 'us-east-2'
from boto3.dynamodb.conditions import Key, Attr


try:
  
    
    table_resource = resource(
        'dynamodb',
        aws_access_key_id=AWS_SECRET_ACCESS_KEY,
      aws_secret_access_key =AWS_SECRET_ACCESS_KEY_ID,
        
        region_name=REGION_NAME
    )
    
    # To access or modify the table's entries, we have to get the table using the resource
    user_table = table_resource.Table('user_table')
    multi_axes_chart_table = table_resource.Table('multi_axes_chart')
    energy_analysis_state = table_resource.Table('energy_analysis_state')

except NoRegionError:
    print("No AWS region specified. Please provide a valid AWS region.")
    # Handle the exception appropriately, e.g., logging, raising a custom exception, etc.

except NoCredentialsError:
    print("AWS credentials not found. Please provide valid AWS credentials.")
    # Handle the exception appropriately, e.g., logging, raising a custom exception, etc.


    
def get_user_by_email(email):
    try:
        # Query DynamoDB table based on the email attribute
        response = user_table.query(
            IndexName='email-index', 
            KeyConditionExpression='email = :email',
            ExpressionAttributeValues={':email': email}
            )
    
        # Check if any items are returned
        if response.get('Items'):
            # Return the first item (assuming there's only one item per email)
            id =response['Items'][0]['id']
            firstname = response['Items'][0]['firstname']
            lastname = response['Items'][0]['lastname']
            email:response['Items'][0]['email']
            password = response['Items'][0]['password']
            return {'id':id,'password':password,'firstname':firstname,'lastname':lastname,'email':email}
        else:
            # If no items found for the email, return None
            return  {'id':'none'}
    except Exception as e:
        print("An error occurred while querying the DynamoDB table:", e)
        # Handle the exception appropriately, e.g., logging, returning a custom error response, etc.
        return  {'id':None}
   
def insert_user(user:UserRegisterSchema):
    try:
        id = generate_object_id()
        user_table.put_item(
            Item = {
                'id':id,
                'firstname':user.firstname,
                'lastname':user.lastname,
                'email':user.email,
               'password': user.password,
               'street':'',
               'city':'',
               'country':'',
               'state':'',
               '_token':''
            }
        )
        return True
    except Exception as e:
        print("An error occurred while scanning the DynamoDB table:", e)
        # Handle the exception appropriately, e.g., logging, returning a custom error response, etc.
        return False  
   




def get_token_by_id(user_id):
    try:
        # Query DynamoDB table based on the id attribute
        response = user_table.query(
            KeyConditionExpression='id = :id',
            ExpressionAttributeValues={':id': user_id}
        )
    
        # Check if any items are returned
        if response.get('Items'):
            # Extract the token field from the first item
            token = response['Items'][0].get('_token')
            return token
        else:
            # If no items found for the id, return None
            return None
    except Exception as e:
        print("An error occurred while querying the DynamoDB table:", e)
        # Handle the exception appropriately, e.g., logging, returning a custom error response, etc.
        return None
 

# def get_user_by_id(user_id):
#     try:
#         # Query DynamoDB table based on the id attribute
#         response = user_table.query(
#             KeyConditionExpression='id = :id',
#             ExpressionAttributeValues={':id': user_id}
#         )
    
#         # Check if any items are returned
#         if response.get('Items'):
#             # Extract the token field from the first item
#             return {response['Items'][0]
#         else:
#             # If no items found for the id, return None
#             return None
#     except Exception as e:
#         print("An error occurred while querying the DynamoDB table:", e)
#         # Handle the exception appropriately, e.g., logging, returning a custom error response, etc.
#         return None
   
    
    
    
def update_token(user_id, access_token):
    
    try:
        # Update the token field for the specified user ID
        response = user_table.update_item(
            Key={'id': user_id},
            UpdateExpression='SET #token = :token',
            ExpressionAttributeValues={':token': access_token['access_token']},
            ExpressionAttributeNames={'#token': '_token'}
        )
        print("Token updated successfully:", response)
        return True
    except Exception as e:
        print("An error occurred while updating the token:", e)
        # Handle the exception appropriately, e.g., logging, returning a custom error response, etc.
        return False
   
    
    
def create_table():
    try:
        table_schema = [
        {
            'AttributeName': 'State',
            'KeyType': 'HASH'  # Partition key
        },
        {
            'AttributeName': 'Year',
            'KeyType': 'RANGE'  # Sort key
        }
        ]
    
    # Define the provisioned throughput
        provisioned_throughput = {
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    
    # Create the DynamoDB table
        table = table_resource.create_table(
            TableName='energy_analysis_state',
            KeySchema=table_schema,
            AttributeDefinitions=[
                {
                    'AttributeName': 'State',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'Year',
                    'AttributeType': 'N'
                }
            ],
            ProvisionedThroughput=provisioned_throughput
        )
    
    # Wait until the table exists
        table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
    
        print(f"Table '{table_name}' created successfully.")

        return ("Table created successfully.")
    except Exception as e:
        print("An error occurred while creating the DynamoDB table:", e)
        return " error"
        # Handle the exception appropriately, e.g., logging, returning a custom error response, etc.

# Call the create_table function to create the DynamoDB table

def get_multi_axes_by_year(year:int):
    try:
        response = multi_axes_chart_table.query(
             KeyConditionExpression='#yr = :year',
        ExpressionAttributeNames={'#yr': 'year'},
            ExpressionAttributeValues={':year': year}
        )
       
        if response.get('Items'):
            # If item already exists, return the existing data
            
            return response['Items'][0]
        else:
            # If item does not exist, insert the data into the database
            insert_data = generate_random_data(year)
            multi_axes_chart_table.put_item(Item=insert_data)
            print("Data inserted successfully.")
            # Return the inserted data
            return insert_data
    except Exception as e:
        print("An error occurred while inserting data into the DynamoDB table:", e)
        return e
        # Handle the exception appropriately, e.g., logging, returning a custom error response, etc.




def insert_energy_analysis_state(state, year):
    
    data = adjusted_data(state,year)
    
    try:
        response =energy_analysis_state.scan(
            FilterExpression=Attr('state').eq(state)&Attr('year').eq(year)
        )
        # energy_analysis_state.put_item(Item=data)
        if response.get('Items'):
            return response['Items'][0]
        else:
            energy_analysis_state.put_item(Item=data)
            return data
    except Exception as e:
        print(e)
        return e
    return data