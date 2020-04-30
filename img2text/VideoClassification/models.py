from tensorflow.keras.layers import Dense, Flatten, Dropout, ZeroPadding3D, BatchNormalization, Activation, LSTM, TimeDistributed, Conv2D, MaxPool2D, ReLU
from tensorflow.keras.models import load_model
from tensorflow.keras import Sequential,regularizers

# Hyperparameters
NUM_CLASSES = 32
LAMBDA  = 0.001
UNITS = 256

class Model():
    def __init__(self, seq_length, saved_model=None, features_length=2048):
        # Set default parameters
        self.seq_length = seq_length
        self.load_model = load_model
        self.saved_model = saved_model

        # Set metrics used for determining network state
        metrics = ['accuracy', 'top_k_categorical_accuracy']

        # Set image parameters
        self.input_shape = (seq_length, features_length)

        # Create Network from keras layers
        self.model = self.model()

        # Compile network
        self.model.compile(loss='categorical_crossentropy', optimizer='Adam', metrics=metrics)
        self.model.summary()

    def model(self):
        model = Sequential()
        model.add(LSTM(2048, return_sequences=False,
                       input_shape=self.input_shape,
                       dropout=0.5))
        model.add(Dense(512, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(NUM_CLASSES, activation='softmax'))

        return model
