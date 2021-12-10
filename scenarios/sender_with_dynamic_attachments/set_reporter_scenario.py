import dataiku
import copy

# Template to reuse when adding attachments to the sender_scenario settings
ATTACHMENT_TEMPLATE = {'params': {'attachedDataset': '',
      'exportParams': {'advancedMode': False,
       'destinationDatasetProjectKey': '',
       'destinationType': 'DOWNLOAD',
       'format': {'params': {'arrayMapFormat': 'json',
         'charset': 'utf8',
         'compress': '',
         'dateSerializationFormat': 'ISO',
         'escapeChar': '\\',
         'fileReadFailureBehavior': 'FAIL',
         'hiveSeparators': ['\x02',
          '\x03',
          '\x04',
          '\x05',
          '\x06',
          '\x07',
          '\x08'],
         'normalizeBooleans': False,
         'normalizeDoubles': True,
         'parseHeaderRow': True,
         'probableNumberOfRecords': 0,
         'quoteChar': '"',
         'readAdditionalColumnsBehavior': 'INSERT_IN_DATA_WARNING',
         'readDataTypeMismatchBehavior': 'DISCARD_WARNING',
         'readMissingColumnsBehavior': 'DISCARD_SILENT',
         'separator': ',',
         'skipRowsAfterHeader': 0,
         'skipRowsBeforeHeader': 0,
         'style': 'excel',
         'writeDataTypeMismatchBehavior': 'DISCARD_WARNING'},
        'type': 'csv'},
       'originatingOptionId': 'tsv-excel-header',
       'overwriteDestinationDataset': False,
       'selection': {'maxRecords': 100000,
        'ordering': {'enabled': False, 'rules': []},
        'partitionSelectionMethod': 'ALL',
        'samplingMethod': 'FULL',
        'selectedPartitions': [],
        'targetRatio': 0.02}}},
     'type': 'DATASET'}

# (!) REPLACE BY THE NAME OF THE SENDER SCENARIO (!)
SENDER_SCENARIO = ""

client = dataiku.api_client()
project = client.get_default_project()
project_key = project.get_settings().project_key

# Compute record counts for all datasets (can also be set visually)
datasets_record_counts = {} 
for ds in project.list_datasets():
    dataset = project.get_dataset(ds["name"])
    dataset.compute_metrics()
    metrics = dataset.get_last_metric_values()
    for m in metrics.get_raw().get("metrics"):
        if m["metric"]["id"] == "records:COUNT_RECORDS":
            datasets_record_counts[ds["name"]] = m["lastValues"][0]["value"]

# Edit the reporter
sender_scenario = project.get_scenario(SENDER_SCENARIO)
settings = sender_scenario.get_settings()
# Here we assume that there is only 1 reporter of type email
reporter = settings.raw_reporters[0]

# Reset list of attachments to start from a clean slate
reporter["messaging"]["configuration"]["attachments"] = []

# Add non-empty datasets to attachments
for k,v  in datasets_record_counts.items():
    # Simple predicate: only attach non-empty Datasets (i.e. nb of rows > 0)
    if int(v) > 0:
        attachment = copy.deepcopy(ATTACHMENT_TEMPLATE)
        attachment["params"]["attachedDataset"] = k
        attachment["params"]["exportParams"]["destinationDatasetProjectKey"] = project_key
        reporter["messaging"]["configuration"]["attachments"].append(attachment)
settings.save()
# From here you can check in the "Send datasets" scenario settings that the reporter has been successfully updated

# Finally, run the sender scenario
sender_scenario.run()
