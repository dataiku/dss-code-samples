# Load a TensorFlow model stored on a remote DSS Folder 

## Questions 
* My TF model is stored in a remote DSS Fodler (for exmaple, an s3 Folder), as multiple files. How can I load it into a Python recipe or Notebook in DSS ?

## Answers
This is only possible by first loading the remote TF files into DSS local Filesystem. This script shows an option of doing through temporary directories.