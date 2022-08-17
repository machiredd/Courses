import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import LabelBinarizer
from sklearn.cross_validation import train_test_split
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.cross_validation import KFold,cross_val_score
from sklearn.grid_search import GridSearchCV
from sklearn.preprocessing import StandardScaler
from keras.callbacks import TensorBoard


def build_fn(dropout=0.2,H=None):
    model = Sequential()
    for i in range(len(H)):
        if i == 0:
            model.add(Dense(H[i], input_dim=X.shape[1], activation='relu'))
            model.add(Dropout(dropout))
        else:
            model.add(Dense(H[i], activation='relu'))
            model.add(Dropout(dropout))
    model.add(Dense(6))
    model.add(Activation('softmax'))

    model.compile(loss='sparse_categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])
    return model


X_train1=np.asarray([line.rstrip('\n').split() for
                    line in open('UCI_HAR_Dataset/train/X_train.txt')],dtype=float)
y_train1=np.asarray([line.rstrip('\n').split() for
                    line in open('UCI_HAR_Dataset/train/y_train.txt')],dtype=float)
X_test1=np.asarray([line.rstrip('\n').split() for
                   line in open('UCI_HAR_Dataset/test/X_test.txt')],dtype=float)
y_test1=np.asarray([line.rstrip('\n').split() for
                   line in open('UCI_HAR_Dataset/test/y_test.txt')],dtype=float)


X=np.concatenate((X_train1, X_test1), axis=0)
y=np.concatenate((y_train1, y_test1), axis=0)

X_scaler = StandardScaler()
X = X_scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.3)

lb = LabelBinarizer()
Y_train = lb.fit_transform(y_train)
Y_test = lb.fit_transform(y_test)

print(X_train shape: ,X_train.shape)
print(X_test shape: ,X_test.shape)

dnn = KerasClassifier(build_fn, nb_epoch=10, batch_size=128, verbose=0)

param_grid = [{'H': [(16,), (64,), (128,), (64, 32), (32, 32), (64, 32, 32)]}]

cv_split = KFold(len(y_train),n_folds=2 )

hyp = GridSearchCV(dnn, param_grid, cv=cv_split, scoring='accuracy')

grid_result=hyp.fit(X_train, y_train)

print('Best score :',hyp.best_score_)
print('Best parameters: ', hyp.best_params_)

#pd.DataFrame(grid_result.history).plot()

board = TensorBoard(log_dir='/tmp/tb')



