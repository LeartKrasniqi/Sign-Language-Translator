import tensorflow as tf
import numpy as np
import time

LINE_NUMBER = 78000
NUM_CLASSES = 26
BATCH_SIZE = 26
files = []
classes = []
images = []

tflite_interpreter = tf.lite.Interpreter(model_path="./letter_net.tflite")
input_details = tflite_interpreter.get_input_details()
output_details = tflite_interpreter.get_output_details()

tflite_interpreter.resize_tensor_input(input_details[0]['index'], (3, 256, 256, 3))
tflite_interpreter.resize_tensor_input(output_details[0]['index'], (3, 26))
tflite_interpreter.allocate_tensors()

input_details = tflite_interpreter.get_input_details()
output_details = tflite_interpreter.get_output_details()

print("== Input details ==")
print("shape:", input_details[0]['shape'])
print("type:", input_details[0]['dtype'])
print("\n== Output details ==")
print("shape:", output_details[0]['shape'])
print("type:", output_details[0]['dtype'])

test_gen = tf.keras.preprocessing.image.ImageDataGenerator(rescale = 1./255)
test_data_gen = test_gen.flow_from_directory(batch_size=26, directory="./asl_alphabet_test/", shuffle=False, target_size=(256, 256))
val_image_batch, val_label_batch = next(iter(test_data_gen))

tflite_interpreter.set_tensor(input_details[0]['index'], val_image_batch)
# Run inference
tflite_interpreter.invoke()
# Get prediction results
tflite_model_predictions = tflite_interpreter.get_tensor(output_details[0]['index'])

print(tflite_model_predictions)
