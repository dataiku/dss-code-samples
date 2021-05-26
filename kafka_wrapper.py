import re, ssl, random
from kafka import KafkaProducer, KafkaClient, KafkaConsumer
from kafka.errors import KafkaError

def get_native_kafka_consumer(input_stream):
    location_info = input_stream.get_location_info(True).get("info", {})
    topic = location_info.get('topic', '')
    connection_params = location_info.get("connectionParams", {})
    try:
        matcher = re.findall('\"(.*?)\"', connection_params.get('saslJAASConfig'))
        sasl_plain_username = matcher[0]
        sasl_plain_password = matcher[1]
    except AttributeError:
        print("Cannot find SASL configuration in JAAS string")
    print("Found SASL auth for user ", sasl_plain_username)

    consumer_group = "dataiku." + str(random.randint(0, 1000))
    print("Consumer will use group ID '" + consumer_group + "'")

    consumer = KafkaConsumer(
        topic,
        bootstrap_servers = connection_params.get('bootstrapServers'),
        security_protocol = "SASL_SSL",
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1),
        sasl_mechanism = connection_params.get('saslMechanism'),
        sasl_plain_username = sasl_plain_username,
        sasl_plain_password = sasl_plain_password
    )
    return consumer

def get_native_kafka_producer(output_stream):
    location_info = output_stream.get_location_info(True).get("info", {})
    connection_params = location_info.get("connectionParams", {})

    try:
        matcher = re.findall('\"(.*?)\"', connection_params.get('saslJAASConfig'))
        sasl_plain_username = matcher[0]
        sasl_plain_password = matcher[1]
    except AttributeError:
        print("Cannot find SASL configuration in JAAS string")
    print("Found SASL auth for user ",sasl_plain_username)

    producer = KafkaProducer(
        bootstrap_servers = connection_params.get('bootstrapServers'),
        security_protocol = "SASL_SSL",
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1),
        sasl_mechanism = connection_params.get('saslMechanism'),
        sasl_plain_username = sasl_plain_username,
        sasl_plain_password = sasl_plain_password
    )
    return producer