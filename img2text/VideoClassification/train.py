from tensorflow.keras.callbacks import ModelCheckpoint, CSVLogger
from models import Model
from data import DataSet
import time
import os
import create_images
import extract_features
import operator

MODEL_NAME = 'VIDC'
EPOCHS = 10
SEQUENCE_LEN = 40


def train(seq_length, saved_model=None, image_shape=None, batch_size=32, num_epoch=100):

    checkpointer = ModelCheckpoint(
        filepath=os.path.join('checkpoints', MODEL_NAME + '-images.{epoch:03d}.hdf5'),
        save_best_only=True)

    # Log training metadata for recall and debugging
    timestamp = time.time()
    csv_logger = CSVLogger(os.path.join('logs', MODEL_NAME + '-' + 'training-' + str(timestamp) + '.log'))

    data = DataSet(seq_length=seq_length, image_shape=image_shape)

    # Obtain data in sequence form for training and validation
    X, y = data.get_all_sequences_in_memory('train')
    # X_test, y_test = data.get_all_sequences_in_memory('test')

    # Obtain model and fit
    rm = Model(seq_length, saved_model)
    rm.model.fit(X, y, batch_size=batch_size, verbose=1, callbacks=[checkpointer], epochs=num_epoch)
    rm.model.save_weights('./checkpoints/my_checkpoint')

def test():
    create_images.extract_files(predict=1)
    extract_features.extract_features(predict=1)
    rm = Model(SEQUENCE_LEN, None)
    rm.model.load_weights('./checkpoints/my_checkpoint')
    data = DataSet(seq_length=SEQUENCE_LEN, image_shape=None, predict=1)
    X = data.get_predict_sequences_in_memory()
    output = rm.model.predict(X)
    print(output)

def main():
    saved_model = None  # None or weights file

    # Chose images or features and image shape based on network.
    image_shape = None

    train(seq_length=SEQUENCE_LEN, saved_model=saved_model, image_shape=image_shape, num_epoch=EPOCHS)


if __name__ == '__main__':
    test()
