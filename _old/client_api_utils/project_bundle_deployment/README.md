# manage bundle

This demonstration of scripted deployment implementing Dataiku client Python API. 

before executing any of those you'll need to install  dataiku client API   
```
# create a bundle from a design node 
./manage_bundles.py create PROJECT_KEY -d "http://YOUR_DESIGN_NODE:PORT/" -b BUNDLENAME-v123 -k "YOUR_API_KEY"

# deploy a bundle from an automation node
./manage_bundles.py deploy  PROJECT_KEY -d "http://YOUR_AUTOMATION_NODE:PORT/" -b BUNDLENAME-v123 -k "YOUR_API_KEY"  -p PATH_TO_YOUR_ARCHIVE.zip

````




