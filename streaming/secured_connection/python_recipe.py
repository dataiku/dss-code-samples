# -*- coding: utf-8 -*-
import kafka_wrapper
import datetime
from kafka.errors import KafkaError

# Read recipe inputs
topic_in = dataiku.StreamingEndpoint("topic_in")
kafka_consumer = kafka_wrapper.get_native_kafka_consumer(topic_in)

topic_out = dataiku.StreamingEndpoint("topic_out")
kafka_producer = kafka_wrapper.get_native_kafka_producer(topic_out)
output_topic = topic_out.get_location_info(True).get("info", {}).get('topic', '')

# Process messages from the input stream
for message in kafka_consumer:
    print ("Processing new message", message.value)
    payload = json.loads(message.value)
    payload['ctime'] = datetime.datetime.now().isoformat()
    future = kafka_producer.send(
        topic = output_topic , 
        value = json.dumps(payload).encode('utf-8')
    )
    try:
        r = future.get(timeout=10)
        print ("> Message successfully sent to topic '%s', partition %d at offset %d" % (output_topic, r.partition, r.offset))
    except KafkaError:
        print ("Fail to produce message to kafka")
