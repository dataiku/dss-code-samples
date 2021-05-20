import dataikuapi


def build_apinode_client(params):
    client_design = dataikuapi.DSSClient(params["host"], params["api"])
    api_deployer = client_design.get_apideployer()
    api_url = api_deployer.get_infra(params["api_dev_infra_id"]).get_settings().get_raw()['apiNodes'][0]['url']
    return dataikuapi.APINodeClient(api_url, params["api_service_id"])


def test_standard_call(params):
    client = build_apinode_client(params)
    print("Test is using API node URL {}".format(client.base_uri))
    record_to_predict = {
        "State": "KS",
        "Account_Length": 128,
        "Area_Code": 415,
        "Phone": "382-4657",
        "Intl_Plan": False,
        "VMail_Plan": True,
        "VMail_Message": 25,
        "Day_Mins": 265.1,
        "Day_Calls": 110,
        "Day_Charge": 45.07,
        "Eve_Mins": 197.4,
        "Eve_Calls": 99,
        "Eve_Charge": 16.78,
        "Night_Mins": 244.7,
        "Night_Calls": 91,
        "Night_Charge": 11.01,
        "Intl_Mins": 10,
        "total_Mins": 717.2,
        "Intl_Calls": 3,
        "Intl_Charge": 2.7,
        "Total_Charge": 75.56,
        "CustServ_Calls": 1,
        "cluster_labels": "cluster_4"
    }
    prediction = client.predict_record(params["api_endpoint_id"], record_to_predict)
    assert prediction['result']['prediction'] == '1', "Prediction should be 1 but is {}".format(prediction['result']['prediction'])


def test_missing_param(params):
    client = build_apinode_client(params)
    print("Test is using API node URL {}".format(client.base_uri))
    record_to_predict = {
        "Account_Length": 128,
        "Area_Code": 415,
        "Phone": "382-4657",
        "Intl_Plan": False,
        "VMail_Message": 25,
        "Day_Mins": 265.1,
        "Day_Calls": 110,
        "Day_Charge": 45.07,
        "Eve_Mins": 197.4,
        "Eve_Calls": 99,
        "Eve_Charge": 16.78,
        "Night_Mins": 244.7,
        "Night_Calls": 91,
        "Night_Charge": 11.01,
        "Intl_Mins": 10,
        "total_Mins": 717.2,
        "Intl_Calls": 3,
        "Intl_Charge": 2.7,
        "Total_Charge": 75.56,
        "CustServ_Calls": 1,
        "cluster_labels": "cluster_4"
    }
    prediction = client.predict_record(params["api_endpoint_id"], record_to_predict)
    assert prediction['result']['ignored'] == True , "Request status status should be ignored = true is {}".format(prediction['result'])
    assert prediction['result']['ignoreReason'] == "IGNORED_BY_MODEL" , "Reason should be IGNORED_BY_MODELbut is {}".format(prediction['result'])
