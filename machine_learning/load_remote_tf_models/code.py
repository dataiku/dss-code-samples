import dataiku
import tensorflow as tf
from tensorflow.keras.models import load_model
import os
import tempfile
from pathlib import Path
import shutil

'''
this example is based on the following Tf model hierachy:

/spam_detection/saved_model.pb
/spam_detection/variables/variables.data-00000-of-00001
/spam_detection/variables/variables.index
'''

folder = dataiku.Folder("NvrBgKDk")
model_folder = "spam_detection"

#Create temporary directory in /tmp
with tempfile.TemporaryDirectory() as tmpdirname:
    #Loop through every file of the TF model and copy it localy to the tmp directory
    for file_name in folder.list_paths_in_partition():
        local_file_path = tmpdirname + file_name
        #Create file localy
        if not os.path.exists(os.path.dirname(local_file_path)):
            os.makedirs(os.path.dirname(local_file_path))
        #Copy file from remote to local
        with folder.get_download_stream(file_name) as f_remote, open(local_file_path,'wb') as f_local:
            shutil.copyfileobj(f_remote,f_local)
    #Load model from local repository  
    model = tf.keras.models.load_model(os.path.join(tmpdirname,model_folder))   