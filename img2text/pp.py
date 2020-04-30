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
    def __init__(self, input_shape=(200, 200, 3)):
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
        global images
        '''
        train_gen = tf.keras.preprocessing.image.ImageDataGenerator()
        val_gen = tf.keras.preprocessing.image.ImageDataGenerator()
        train_data_gen = train_gen.flow_from_directory(batch_size=BATCH_SIZE, directory=filepath, shuffle=True)
        val_data_gen = val_gen.flow_from_directory(batch_size=BATCH_SIZE, directory=testpath, shuffle=True)
        '''
        counter = 1
        f = open('./Data/train.txt', 'r')
        for line in f:
            if counter == 4:
                values = line.split(", ")
                values[1] = values[1][:-1]
                files.append(values[0])
                classes.append(ord(values[1]) - 65)
                #img = open(values[0], 'r')
                im = cv2.imread(values[0])
                images.append(im)
                counter = 0
            else:
                counter += 1


        classes_cat = np.asarray(tf.keras.utils.to_categorical(classes, NUM_CLASSES))
        checkpoint_path = "./checkpoints/cp-{epoch:04d}.ckpt"
        cp_callback = tf.keras.callbacks.ModelCheckpoint(
                            filepath=checkpoint_path,
                            save_weights_only=True,
                            period=1)

        images = np.reshape(images, [-1, 200, 200, 3])
        self.rnn.fit(images, classes_cat, epochs=50, callbacks=[cp_callback]) #validation_data=val_data_gen,
        self.rnn.save_weights(checkpoint_path.format(epoch=0))

    def load(self, weightpath):
        self.rnn.load_weights(weightpath)

    def predict(self, testpath):
        global images
        im = cv2.imread("./Data/asl_alphabet_test/B/test_b.PNG")
        print(np.shape(im))
        #im = im / 1
        images.append(im)
        im = cv2.imread("./Data/asl_alphabet_test/L/L_test.jpg")
        print(np.shape(im))
        images.append(im)
        images = np.reshape(images, [-1, 200, 200, 3])
        #im = np.expand_dims(im, -0)
        #test_gen = tf.keras.preprocessing.image.ImageDataGenerator()
        #test_data_gen = test_gen.flow_from_directory(batch_size=BATCH_SIZE, directory=testpath, shuffle=False, target_size=(256, 256))
        #test_data_gen = test_gen.flow(im, y)
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
        output = self.rnn.predict(images)

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
model.load("./checkpoints/cp-0050.ckpt")
#model.convert()
#model.predict("./Data/asl_alphabet_test/")
model.train("./Data/asl_alphabet_train/asl_alphabet_train/", "./Data/asl_alphabet_val/asl_alphabet_val/")
