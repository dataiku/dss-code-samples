# Recommender Systems in Dataiku Visual ML

This project demonstrates the technical feasibility of using [Collaborative Filtering Recommender Systems](https://en.wikipedia.org/wiki/Collaborative_filtering) as Custom Python models within our Visual ML interface.

# Why?
In our current Visual ML, there is (seemingly) no way to use recommender systems. Users have to code it in their own code recipes, which makes it harder to train, test and deploy.

# Getting started

## Prerequisites

* Have a training dataset with the following schema:
    - **user_id**: unique identifier for users - integer
    - **item_id:** unique identifier for items - integer
    - **rating:** explicit rating (e.g. number of stars or like/dislike) or implicit rating (e.g. clicked or visited page) - decimal or integer
* Be in a Dataiku user group with the permission to create code environments and write (safe) code

## Limitations

* First of all, [collaborative filtering](https://towardsdatascience.com/various-implementations-of-collaborative-filtering-100385c6dfe0) is a relatively simple (but powerful) type of method for designing recommender systems. They model user and item interactions through ratings ; but cannot use external features.
* It currently works exclusively for models implemented in the [Surprise](https://surprise.readthedocs.io/en/stable/prediction_algorithms_package.html) Python package.
* This package requires user and item identifiers to be numeric. If identifiers are strings, something like sklearn's [label encoder](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.LabelEncoder.html) may be recommended.

## How To Use It?

### Environment and Library Setup

1. Create a Python code environment with these requested packages:
```
scikit-learn>=0.19.1,<0.20
xgboost==0.71
statsmodels>=0.8,<0.9
jinja2>=2.10,<2.11
flask>=0.12,<0.13
scikit-surprise==1.0.6
```
2. Add the following Python files in your project's code libraries: https://github.com/dataiku/dss-code-samples/tree/master/reco
    -  [without Internet access] you can copy paste the content of the files (do not forget `__init__.py`)
    - [with Internet access] you can add the `reco` path within this repository as a git reference in your code library, targeting the `python/reco` path.

### Visual ML Design

1. In "Features handling", select your user_id and item_id columns as your only features. Column names can be your own, but user_id and item_id must be **in that order**. If needed, you can reorder the columns in the Script before the Visual ML analysis. Make sure to use numerical handling with **no rescaling**.
2. In "Algorithms", select "Add Custom Python Model" and paste the following code snippet:
```
from reco.surprise_wrapper import SurpriseRecommender
from surprise import SVDpp
clf = SurpriseRecommender(rating_scale = (0,10), model = SVDpp())
```
The SurpriseRecommender class is a wrapper around the Python [Surprise](http://surpriselib.com) package. To instanciate it, you need to specify the scale of the ratings as a tuple of (min, max) values ; and choose which model class to use within the Surprise library.
3. Proceeed with training in our Visual ML as normal.


### Deployment

As usual, once a collaborative filtering model has been deployed to a the project flow, you can use it to score in batches, and turn it into an API endpoint. You can follow the standard deployment method from API Designer to API Deployer which applies to any prediction model endpoint.

After pushing to the API deployer, you should have a live API endpoint that accepts the user_id and item_id values as features and returns an output like the following:

Call:

```
curl -X POST \
  https://API_NODE_URL//public/api/v1/<API_SERVICE_ID>/<API_ENDPOINT_ID>/predict \
  --data '{ "features" : {
    "userID": "1",
    "itemID": "100"
  }}'
  ```

  Output:

  ```
  {"result": {"prediction":3.870503508945169, "ignored" : false},
   "timing  : {"preProcessing" : 79, "wait" : 27, "enrich" : 6, "preparation" : 4, "prediction" : 27380, "postProcessing" : 17},
   "apiContext": {"serviceId" : "SERVICE_ID", "endpointId" : "ENDPOINT_ID", "serviceGeneration" : "v1" }
   }
  ```

  See [here](https://doc.dataiku.com/dss/latest/apinode/index.html) for more information on the API Deployer.
