# -*- coding: utf-8 -*-
# This script retrieve the last build date value from a dataset

import dataikuapi
import calendar
from datetime import datetime
import dateutil.parser

HOST = "http://myhost:myport/"
API_KEY = "MY_API_KEY"
PROJECT_KEY = "MY_PROJECT"
DATASET_NAME = "MY_DATASET"

client = dataikuapi.DSSClient(HOST, API_KEY)
project = client.get_project(PROJECT_KEY)
dataset = project.get_dataset(DATASET_NAME)

dataset_metrics = dataset.get_last_metric_values()
if "reporting:BUILD_START_DATE" in dataset_metrics.get_all_ids():
    max_timestamp = 0
    for val in dataset_metrics.get_metric_by_id("reporting:BUILD_START_DATE").get("lastValues", []):
        if not "value" in val:
            continue
        # retrieve the timestamp
        timestamp = calendar.timegm(dateutil.parser.parse(val.get("value", "")).timetuple())
        if timestamp > max_timestamp:
            max_timestamp = timestamp
    if max_timestamp > 0:
        # the timezone is UTC
        print(datetime.utcfromtimestamp(max_timestamp).strftime('%Y-%m-%d %H:%M:%S'))
    else:
        print("no last build date value for this dataset")
else:
    print("no last build date value for this dataset")
