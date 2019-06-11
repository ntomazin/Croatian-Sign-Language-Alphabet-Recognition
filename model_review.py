from keras.models import load_model
import pickle
import numpy as np
from keras.utils import np_utils


model = load_model('cnn_model.h5')

with open("val_images", "rb") as f:
    val_images = np.array(pickle.load(f))
with open("val_labels", "rb") as f:
    val_labels = np.array(pickle.load(f), dtype=np.int32)

val_images = np.reshape(val_images, (val_images.shape[0], 50, 50, 1))
val_labels = np_utils.to_categorical(val_labels)


print(model.evaluate(val_images, val_labels, verbose=0))