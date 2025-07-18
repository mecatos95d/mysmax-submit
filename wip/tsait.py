from tsai.basics import *

X, y, splits = get_classification_data('ECG200', split_data=False)
tfms = [None, TSClassification()]
batch_tfms = TSStandardize()
clf = TSClassifier(X, y, splits=splits, path='models', arch="InceptionTimePlus", tfms=tfms, batch_tfms=batch_tfms, metrics=accuracy, cbs=ShowGraph())
clf.fit_one_cycle(100, 3e-4)
clf.export("clf.pkl")

from tsai.inference import load_learner

clf = load_learner("models/clf.pkl")
probas, target, preds = clf.get_X_preds(X[splits[1]], y[splits[1]])
