import boto3
#from dotenv import load_dotenv
import os
 
# Load environment variables from .env file
#load_dotenv()
AWS_ACCESS_KEY_ID=''
AWS_SECRET_ACCESS_KEY=''
AWS_DEFAULT_REGION='us-west-2'
# Configure AWS client using environment variables
bedrock_client = boto3.client(
    service_name='bedrock-agent-runtime',
    region_name=os.getenv('AWS_DEFAULT_REGION'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)
 
session = boto3.session.Session()
region = session.region_name
 
def retrieveAndGenerate(input_text, sourceType, model_id, region, document_s3_uri=None, data=None, identifier=None):
    model_arn = f'arn:aws:bedrock:{region}::foundation-model/{model_id}'
 
    if sourceType == "S3":
        return bedrock_client.retrieve_and_generate(
            input={'text': input_text},
            retrieveAndGenerateConfiguration={
                'type': 'EXTERNAL_SOURCES',
                'externalSourcesConfiguration': {
                    'modelArn': model_arn,
                    'sources': [
                        {
                            "sourceType": sourceType,
                            "s3Location": {
                                "uri": document_s3_uri  
                            }
                        }
                    ]
                }
            }
        )
       
    else:
        return bedrock_client.retrieve_and_generate(
            input={'text': input_text},
            retrieveAndGenerateConfiguration={
                'type': 'EXTERNAL_SOURCES',
                'externalSourcesConfiguration': {
                    'modelArn': model_arn,
                    'sources': [
                        {
                            "sourceType": sourceType,
                            "byteContent": {
                                "identifier": identifier,
                                "contentType": "text/plain",
                                "data": data  
                            }
                        }
                    ]
                }
            }
        )
 
model_id = "anthropic.claude-3-sonnet-20240229-v1:0"
document_uri = "s3://s3bucket/filename.pdf"
 
def my_chatbot(question):
    response = retrieveAndGenerate(
        input_text=question,
        sourceType="S3",
        model_id=model_id,
        region=region,
        document_s3_uri=document_uri
    )
    return response
 
my_question = "What are the skills of candidate?"
response = my_chatbot(question=my_question)
print(response['output']['text'])
