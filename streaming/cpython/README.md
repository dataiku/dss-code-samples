# kafka_to_kafka_enrichment.py

A simple code that will add a field in all message with a fixed value.

# kafka_to_kafka_prediction.py

This sample is using a existing saved model in yourn project.
All incoming messages will be send to the model for a prediction, the prediction result will be added to the message and send to an output topic

Note: you need a code-env with both pykafka & scikit-learn
