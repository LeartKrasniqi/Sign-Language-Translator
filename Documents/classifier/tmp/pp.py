import tensorflow as tf
from PIL import Image
import numpy as np
import time
import cv2

LINE_NUMBER = 78000
NUM_CLASSES = 26
BATCH_SIZE = 26
files = []
classes = []
images = []
# classes_cat = []

class Model(tf.Module):
    def __init__(self, input_shape=(256, 256, 3)):
        self.input_shape = input_shape
        # self.rnn = tf.keras.Sequential()
        self.setupLayers()


    def setupLayers(self):
        base_model = tf.keras.applications.InceptionV3(weights='imagenet', include_top=False, input_shape=self.input_shape)
        x = base_model.output
        x = tf.keras.layers.GlobalAveragePooling2D()(x)
        x = tf.keras.layers.Dense(1024, activation='relu')(x)
        predictions = tf.keras.layers.Dense(26, activation='softmax')(x)

        self.rnn = tf.keras.models.Model(inputs=base_model.input, outputs=predictions)
        self.rnn.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

    def train(self, filepath, testpath):
        train_gen = tf.keras.preprocessing.image.ImageDataGenerator()
        val_gen = tf.keras.preprocessing.image.ImageDataGenerator()
        train_data_gen = train_gen.flow_from_directory(batch_size=BATCH_SIZE, directory=filepath, shuffle=True)
        val_data_gen = val_gen.flow_from_directory(batch_size=BATCH_SIZE, directory=testpath, shuffle=True)
        '''
        for line in f:
            values = line.split(", ")
            values[1] = values[1][:-1]
            files.append(values[0])
            classes.append(ord(values[1]) - 65)
        '''
        # classes_cat = tf.keras.utils.to_categorical(classes, NUM_CLASSES)
        checkpoint_path = "./checkpoints/cp-{epoch:04d}.ckpt"
        cp_callback = tf.keras.callbacks.ModelCheckpoint(
                            filepath=checkpoint_path,
                            save_weights_only=True,
                            period=1)

        self.rnn.save_weights(checkpoint_path.format(epoch=0))
        self.rnn.fit_generator(train_data_gen, epochs=1, validation_data=val_data_gen, callbacks=[cp_callback])

    def load(self, weightpath):
        self.rnn.load_weights(weightpath)

    def predict(self, testpath):
        im = cv2.imread("./Data/asl_alphabet_test/B/test_b.png")
        im = im / 1
        im = cv2.resize(im, (256, 256))
        im = np.expand_dims(im, -0)
        y = "B"
        test_gen = tf.keras.preprocessing.image.ImageDataGenerator()
        #test_data_gen = test_gen.flow_from_directory(batch_size=BATCH_SIZE, directory=testpath, shuffle=False, target_size=(256, 256))
        test_data_gen = test_gen.flow(im, y)
        # val_image_batch, val_label_batch = next(iter(test_data_gen))
        #rescaled = (255.0 / val_image_batch.max() * (val_image_batch - val_image_batch.min())).astype(np.uint8)
        #im = Image.fromarray(rescaled)
        #im.save("test.png")
        '''
        im = cv2.imread("./TEST/_0_232052.jpg")
        im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
        im = im / 1
        im = cv2.resize(im, (256, 256))
        im = np.expand_dims(im, -0)
        '''
        time1 = time.time()
        output = self.rnn.predict(im)

        time2 = time.time()
        print(time2-time1)
        #true_label_ids = np.argmax(val_label_batch, axis=-1)
        print(output)
        # print(predictions)
        #print(true_label_ids)

    def convert(self):
        run_model = tf.function(lambda x : self.rnn(x))
        concrete_func = run_model.get_concrete_function(
            tf.TensorSpec(self.rnn.inputs[0].shape, self.rnn.inputs[0].dtype)
        )
        converter = tf.lite.TFLiteConverter.from_concrete_functions([concrete_func])
        converter.optimizations = [tf.lite.Optimize.OPTIMIZE_FOR_SIZE]
        tflite_quant_model = converter.convert()
        open("letter_net.tflite", "wb").write(tflite_quant_model)
        '''
        converter = tf.lite.TFLiteConverter.from_keras_model(self.rnn)
        self.tflite_model = converter.convert()
        open("converted_model.tflite", "wb").write(self.tflite_model)
        '''


model = Model()
model.load("./checkpoints/cp-0001.ckpt")
#model.convert()
'''
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
test_data_gen = test_gen.flow_from_directory(batch_size=26, directory="./Data/asl_alphabet_test/", shuffle=False, target_size=(256, 256), save_to_dir="./TEST", save_format="jpg")
val_image_batch, val_label_batch = next(iter(test_data_gen))

tflite_interpreter.set_tensor(input_details[0]['index'], val_image_batch)
# Run inference
tflite_interpreter.invoke()
# Get prediction results
tflite_model_predictions = tflite_interpreter.get_tensor(output_details[0]['index'])

print(tflite_model_predictions)
'''

model.predict("./Data/asl_alphabet_test/")
#model.train("./Data/asl_alphabet_train/asl_alphabet_train/", "./Data/asl_alphabet_val/asl_alphabet_val/")
