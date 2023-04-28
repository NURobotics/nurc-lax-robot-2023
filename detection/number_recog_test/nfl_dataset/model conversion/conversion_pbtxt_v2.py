import tensorflow as tf

#solve the GFile and GraphDef issues:
#https://stackoverflow.com/questions/57614436/od-graph-def-tf-graphdef-attributeerror-module-tensorflow-has-no-attribut

#import tensorflow.compat.v1 as tf
#tf.disable_v2_behavior()

#from tensorflow.python.platform import gfile
#import tensorflow as tf
#import tensorflow.compat.v1 as tf
#tf.disable_v2_behavior() 

import tensorflow as tf

from tensorflow.io import gfile
#from keras.models import load_model

#run this model in streamlit_shell; make sure the tensorflow version is 2.6.0
#so that it mimics the functions that existed in Sep 2021 when ChatGPT was trained

#new: activate conda environment tfold in order to produce these files; Python version 3.7; can try
#tensorflow v 1.14.0 or 1.10.0

#model = load_model('your_model.h5')


#-----------------PART 2------------------#

# Convert Keras model to TensorFlow format
tf.keras.backend.set_learning_phase(0)
model = tf.keras.models.load_model('best_model.h5')
tf.keras.backend.set_learning_phase(0)

# Save TensorFlow model in .pb format
tf.saved_model.save(model, 'saved_model')

#-----------------PART 3------------------#

# Load TensorFlow .pb model
#with gfile.FastGFile('saved_model/saved_model.pb', 'rb') as f:
with gfile.GFile('saved_model/saved_model.pb', 'rb') as f:
    #graph_def = tf.GraphDef()
    graph_def = tf.compat.v1.GraphDef() 
    graph_def.ParseFromString(f.read())
    #graph_def.ParseFromString(f.read(-1)) 

# Write TensorFlow .pbtxt model
with open('saved_model/saved_model.pbtxt', 'wb') as f:
    f.write(tf.compat.as_bytes(str(graph_def)))# 1qqqqqqqqqqqqqqq