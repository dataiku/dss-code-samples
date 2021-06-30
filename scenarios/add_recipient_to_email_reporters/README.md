This code sample illustrates how to use the Dataiku DSS API to interact with scenarios settings.
The use case is to add a new recipient for all the existing "Send email" reporters for all the scenarios of a specified project.

In practice, it:
1. lists all the existing scenarios in a specified project
2. searches for all the "Send email" reporters
3. retrieves for each of them, the list of recipients
4. updates for each of them, the recipients list if the new recipient doesn't already exist

This script is detailled in the article [How to programmatically set email recipients in a "Send email" reporter using the API?](https://community.dataiku.com/t5/Product-Knowledge-Base/How-to-programmatically-set-email-recipients-in-a-quot-Send/ta-p/7413) from the [Dataiku DSS Product Kowledge Base](https://community.dataiku.com/t5/Product-Knowledge-Base/tkb-p/dss-knowledge-base).
