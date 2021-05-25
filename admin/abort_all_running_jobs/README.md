# Abort all running jobs in a DSS project

## Questions
* I want to abort all running jobs of a specific DSS project.

## Answers
This is possible by listing all running jobs of a project and loop over them to apply the [`abort()`](https://doc.dataiku.com/dss/latest/python-api/jobs.html#dataikuapi.dss.job.DSSJob.abort) method of the DSS public API.
