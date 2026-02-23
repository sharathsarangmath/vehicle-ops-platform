import json
import boto3
import os
from datetime import datetime

sqs = boto3.client('sqs', region_name='us-east-1')

REQUIRED_FIELDS = ['vehicle_id', 'speed_kmh', 'fuel_percent', 'lat', 'lon']
MAX_SPEED = 300
QUEUE_URL = os.environ.get('SQS_QUEUE_URL', '')

def validate_payload(data):
    errors = []

    for field in REQUIRED_FIELDS:
        if field not in data:
            errors.append(f"Missing required field: {field}")

    if 'speed_kmh' in data:
        if not isinstance(data['speed_kmh'], (int, float)):
            errors.append("speed_kmh must be a number")
        elif data['speed_kmh'] < 0 or data['speed_kmh'] > MAX_SPEED:
            errors.append(f"speed_kmh must be between 0 and {MAX_SPEED}")

    if 'fuel_percent' in data:
        if not isinstance(data['fuel_percent'], (int, float)):
            errors.append("fuel_percent must be a number")
        elif data['fuel_percent'] < 0 or data['fuel_percent'] > 100:
            errors.append("fuel_percent must be between 0 and 100")

    return errors

def lambda_handler(event, context):
    try:
        body = json.loads(event.get('body', '{}'))
    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid JSON'})
        }

    errors = validate_payload(body)
    if errors:
        return {
            'statusCode': 400,
            'body': json.dumps({'errors': errors})
        }

    body['received_at'] = datetime.utcnow().isoformat()

    sqs.send_message(
        QueueUrl=QUEUE_URL,
        MessageBody=json.dumps(body),
        MessageAttributes={
            'vehicle_id': {
                'StringValue': body['vehicle_id'],
                'DataType': 'String'
            }
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Telemetry received',
            'vehicle_id': body['vehicle_id'],
            'received_at': body['received_at']
        })
    }
