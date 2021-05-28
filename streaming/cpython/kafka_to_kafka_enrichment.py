# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np, json
from dataiku import pandasutils as pdu

# Read recipe inputs
topic1 = dataiku.StreamingEndpoint("topic-1")

# Write recipe outputs
output = dataiku.StreamingEndpoint("output")
output.set_schema(topic1.get_schema())

with output.get_writer() as writer:
    for msg in topic1.get_native_kafka_consumer():
        try:
            row = json.loads(msg.value)
            print("Processing message: ", row)
            row.append({'my-data' : '1234'})
            writer.produce(json.dumps(row).encode('utf8')) 
        except:
            continue
