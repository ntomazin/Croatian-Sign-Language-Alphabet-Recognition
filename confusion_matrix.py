from sklearn import metrics
#from load_img import test_images,test_labels
from keras.models import load_model
import pickle
import numpy as np
from keras.utils import np_utils
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from gestures import get_pred_text



def cm_analysis(y_true, y_pred, ymap=None, figsize=(10,10)):
    """
    Generate matrix plot of confusion matrix with pretty annotations.
    The plot image is saved to disk.
    args:
      y_true:    true label of the data, with shape (nsamples,)
      y_pred:    prediction of the data, with shape (nsamples,)
      filename:  filename of figure file to save
      labels:    string array, name the order of class labels in the confusion matrix.
                 use `clf.classes_` if using scikit-learn models.
                 with shape (nclass,).
      ymap:      dict: any -> string, length == nclass.
                 if not None, map the labels & ys to more understandable strings.
                 Caution: original y_true, y_pred and labels must align.
      figsize:   the size of the figure plotted.
    """
    labels = []
    if ymap is not None:
        y_pred = [ymap[yi] for yi in y_pred]
        y_true = [ymap[yi] for yi in y_true]
    else:
        for i in range(0,63):
            labels.append(get_pred_text(i))
        #for yt in zip(y_true,y_pred):
        #    y_true = get_pred_text(yt)
        #    y_pred = get_pred_text(yp)
    cm = metrics.confusion_matrix(y_true, y_pred)
    cm_sum = np.sum(cm, axis=1, keepdims=True)
    cm_perc = cm / cm_sum.astype(float) * 100
    annot = np.empty_like(cm).astype(str)
    nrows, ncols = cm.shape
    for i in range(nrows):
        for j in range(ncols):
            c = cm[i, j]
            p = cm_perc[i, j]
            if i == j:
                s = cm_sum[i]
                annot[i, j] = '%.1f%%\n%d/%d' % (p, c, s)
            elif c == 0:
                annot[i, j] = ''
            else:
                annot[i, j] = '%.1f%%\n%d' % (p, c)
    cm = pd.DataFrame(cm)
    cm.index.name = 'Actual'
    cm.columns.name = 'Predicted'
    fig, ax = plt.subplots(figsize=figsize)
    sns.heatmap(cm, annot=annot, fmt='', ax=ax)
    plt.savefig('confusion_matrix')
    plt.show()



model = load_model('cnn_model.h5')
with open("test_images", "rb") as f:
    test_images = np.array(pickle.load(f))
with open("test_labels", "rb") as f:
    test_labels = np.array(pickle.load(f), dtype=np.int32)

test_images = np.reshape(test_images, (test_images.shape[0], 50, 50, 1))
test_labels = np_utils.to_categorical(test_labels)

predicted = model.predict(test_images)
predicted = np.argmax(predicted, axis=1)
#print (predicted.shape)
expected = np.argmax(test_labels, axis = 1)
#confusion_matrix = metrics.confusion_matrix(expected, predicted)
#print(confusion_matrix)

cm_analysis(expected, predicted, ymap=None, figsize=(10,10))