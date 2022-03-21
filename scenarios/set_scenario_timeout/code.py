###########################################################################################
# !! CUSTOM SCENARIO EXAMPLE !!                                                           #
# See https://doc.dataiku.com/dss/latest/scenarios/custom_scenarios.html for more details #
###########################################################################################

import time
import dataiku
from dataiku.scenario import Scenario, BuildFlowItemsStepDefHelper
from dataikuapi.dss.future import DSSFuture

TIMEOUT_SECONDS = 3600

s = Scenario()

# Replace this commented block by your Scenario steps
# Example: build a Dataset
step_handle = s.build_dataset("your_dataset_name", asynchronous=True)

start = time.time()
while not step_handle.is_done():
    end = time.time()
    print("Duration: {}s".format(end-start))
    if end - start > TIMEOUT_SECONDS:
        f = DSSFuture(dataiku.api_client(), step_handle.future_id)
        f.abort()
        raise Exception("Scenario was aborted because it took too much time.")


