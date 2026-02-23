from kafka import KafkaConsumer
import json
from datetime import datetime

# Alert thresholds
SPEED_LIMIT = 120
FUEL_THRESHOLD = 15

def check_alerts(data):
    alerts = []
    if data.get('speed_kmh', 0) > SPEED_LIMIT:
        alerts.append({
            'type': 'SPEED_ALERT',
            'message': f"Speed {data['speed_kmh']} exceeds limit {SPEED_LIMIT}"
        })
    if data.get('fuel_percent', 100) < FUEL_THRESHOLD:
        alerts.append({
            'type': 'LOW_FUEL_ALERT',
            'message': f"Fuel {data['fuel_percent']}% below threshold {FUEL_THRESHOLD}%"
        })
    return alerts

def main():
    print("🚗 Vehicle Consumer started — waiting for messages...")

    consumer = KafkaConsumer(
        'vehicle-telemetry',
        bootstrap_servers=['kafka:9092'],
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        auto_offset_reset='earliest',
        group_id='vehicle-consumer-group'
    )

    for message in consumer:
        data = message.value
        timestamp = datetime.utcnow().isoformat()

        print(f"\n📨 Message received at {timestamp}")
        print(f"   Vehicle:  {data.get('vehicle_id')}")
        print(f"   Speed:    {data.get('speed_kmh')} km/h")
        print(f"   Fuel:     {data.get('fuel_percent')}%")

        alerts = check_alerts(data)

        if alerts:
            for alert in alerts:
                print(f"   🚨 ALERT: {alert['type']} — {alert['message']}")
        else:
            print(f"   ✅ Status: Normal")

if __name__ == "__main__":
    main()