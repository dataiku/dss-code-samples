# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np, json
from dataiku import pandasutils as pdu

# Read recipe inputs
in_events = dataiku.StreamingEndpoint("in-events")
in_events_messages = in_events.get_native_kafka_consumer() # use as a generator

logreg_model = dataiku.Model('mIkUmJfL')
predictor = logreg_model.get_predictor()

# Write recipe outputs
out_events = dataiku.StreamingEndpoint("out-events")
out_events.set_schema(in_events.get_schema())

with out_events.get_native_kafka_producer() as out_events_writer:
    for f_event in in_events_messages:
        # Extract the event data
        print('Receiving event:')
        print(f_event.value)
        f_event_data = json.loads(f_event.value)
        df = pd.DataFrame.from_records([f_event_data])
        # Make the prediction
        pred = predictor.predict(df)
        print('Prediction result:')
        print(pred)
        # Add the prediction result to the event
        f_event_data['prediction'] = pred['prediction'][0]
        f_event_data['proba_0'] = pred['proba_0'][0]
        f_event_data['proba_1'] = pred['proba_1'][0]

        # Publish the message to Kafka
        print('Publishing event:')
        print(f_event_data)
        v = json.dumps(f_event_data).encode('utf8')
        out_events_writer.produce(v, f_event.partition_key, f_event.timestamp)
