This sample shows how to create a specific library to connect to a secured Kafka broker.
By default, DSS is shipped with [pykafka](https://github.com/Parsely/pykafka), which does not support SASL ( [SASL Support #651](https://github.com/Parsely/pykafka/issues/651) ).

If you need SASL, an alternative is to build your own client, leveraging an library that does support SASL. In this sample, we are using [kafka-python](https://pypi.org/project/kafka-python/).
In order to use this sample:
 - The wrapper code is in kafka_wrapper.py. Upload this file in you project library, under lib/python
 - Create (or update) a code-env with the requested package 'kafka-python'
 - Setup your Kafka connection with a Security mode to Generic SASL and the correct SASL JAAS config parameters
 - Create 2 Streaming endpoints on this connection
 - Create a continuous python recipe using the code in python_recipe.py
 - Setup the recipe to use the code-env you configured with kafka-python
 - Save and run


To learn more on Streaming, see [Dataiku documentation](https://doc.dataiku.com/dss/latest/streaming/index.html)

