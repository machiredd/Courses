import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import KFold,cross_val_score,GridSearchCV
from sklearn.preprocessing import StandardScaler

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

    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])
    return model


X_train=np.asarray([line.rstrip('\n').split() for
                    line in open('UCI_HAR_Dataset/train/X_train.txt')],dtype=float)
y_train=np.asarray([line.rstrip('\n').split() for
                    line in open('UCI_HAR_Dataset/train/y_train.txt')],dtype=float)
X_test=np.asarray([line.rstrip('\n').split() for
                   line in open('UCI_HAR_Dataset/test/X_test.txt')],dtype=float)
y_test=np.asarray([line.rstrip('\n').split() for
                   line in open('UCI_HAR_Dataset/test/y_test.txt')],dtype=float)


X=np.concatenate((X_train, X_test), axis=0)
y=np.concatenate((y_train, y_test), axis=0)

X_scaler = StandardScaler()
X = X_scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.3)

lb = LabelBinarizer()
Y_train = lb.fit_transform(y_train)
Y_test = lb.fit_transform(y_test)

print('X_train shape: ',X_train.shape)
print('X_test shape: ',X_test.shape)

dnn = KerasClassifier(build_fn, nb_epoch=10, batch_size=128, verbose=0)

param_grid = [{'H': [(16,), (64,), (16, 8), (32, 32), (32, 32, 32)]}]

inner_cv = KFold(n_splits=3, shuffle=True)
outer_cv = KFold(n_splits=3, shuffle=True)

hyp = GridSearchCV(dnn, param_grid, cv=inner_cv,
                   n_jobs=-1,scoring='accuracy')
scores = cross_val_score(hyp, X_train, Y_train, cv=outer_cv, n_jobs=1)

print(scores)
print('Mean classification accuracy: ',scores.mean())








#kfold = StratifiedKFold(y_train,n_folds=2)
#results = cross_val_score(dnn, X_train, Y_train, cv=kfold)
#print(results.mean())

#model=build_fn(dropout=0.2,H=(32,32,32))
#
#
#history = model.fit(X_train, Y_train,
#                    batch_size=256,
#                    epochs=20,
#                    verbose=1,
#                    validation_data=(X_test, Y_test))
