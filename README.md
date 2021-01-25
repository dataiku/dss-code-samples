# dss-code-samples
Various code samples for using DSS

## Refactoring 

### Getting started

(DSS >= 8.0.3)

#### Use within DSS (as project library)
- Register in Project Lib Git
- No need to specify remote DSS params
- Profit

#### Outside of DSS
- Clone repository, tarzip it
- Create virtualenv with dss requirements and tarzipped archive
- Profit ...?

You can reuse them as they are, customize them for your own needs, and even package them into plugins.

Create a dedicated virtual environment and install the following packages:
* `dataiku-internal-client`:  follow the instructions in the [DSS doc](https://doc.dataiku.com/dss/latest/python-api/outside-usage.html#installing-the-package)
* `dataikuapi`: 
  ```
  $ pip install dataiku-api-client
  ```
* `pandas`:
  ```
  $ pip install "pandas>=1.0,<1.1"
  ```

### Structure

```
dss-code-samples
|_admin
|_applications
|_datasets
|_formulas
|_metrics_and_checks
|_machine_learning
|_partitioning
|_scenarios
|_statistics
|_webapps
```



