# DSS code samples

This repository contains various examples of code-based operations for Dataiku DSS.

## Getting started

**Pre-requisites**
* Dataiku DSS >= 8.0.3
* Python >= 3.6

**Within DSS**
* Create a [Git reference]() in your DSS project pointing to this repository and import what you want/need in your recipes/notebooks/etc.
* You can also just copy-paste directly in your project libraries/recipes/notebooks/etc. the parts you're interested in.

**Outside of DSS**
You can run some of the functions outside of DSS. To set up a proper virtual environment, follow these steps:

```bash
# Clone the repository
git clone git@github.com:dataiku/dss-code-samples.git
cd dss-code-samples

# Create and activate a dedicated virtual environment
python -m venv venv
source venv/bin/activate

# Install the dataiku public API client
pip install dataiku-api-client "pandas>=1.0,<1.1"
```

You will also need to install the `dataiku` internal API's Python, as described in the [DSS reference documentation](https://doc.dataiku.com/dss/latest/python-api/outside-usage.html#installing-the-package)). 

Finally, you will have to specify the DSS instance URL and an API key to authenticate against it, as illustrated in this example:

```python
import dataiku
from admin.jobs import list_jobs_by_status

# Setup your DSS instance parameters
dataiku.set_remote_dss(url=YOUR_DSS_INSTANCE_URL, api_key=YOUR_API_KEY)

# Run your code
client = dataiku.api_client()
jobs_status = list_jobs_by_status(client=client, project_key=YOUR_PROJECT_KEY)
print(jobs_status)
```

## Contributing

All contributions are more than welcome! If you wish to submit an idea, feel free to open an issue and/or submit a pull request.

## License
Copyright (C) 2021 Dataiku
Licensed under the Apache License, version 2.0


