#https://stackoverflow.com/questions/60005661/tensorflow-2-0-convert-keras-model-to-pb-file

print("Loading Tensorflow:")
import tensorflow as tf

print("Loading model")
pre_model = tf.keras.models.load_model("best_model.h5")

#test 1: what was recommmended on StackOverflow
print("Saving model, v1")
pre_model.save("saved_model")

#test 2: the format we want
print("Saving model, v2")
pre_model.save("saved_model.pbtxt")