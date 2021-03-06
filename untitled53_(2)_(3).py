# -*- coding: utf-8 -*-
"""Untitled53_(2) (3).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1E-EmILlu1WsL6ELTnMFm2_9ahvNvmgkA
"""

import tensorflow as tf
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, Normalizer
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.layers import Embedding, LSTM
from keras.layers import Conv1D, MaxPooling1D, Flatten
from matplotlib import pyplot

name = ["duration","protocol","service","flag","src",
    "dst","land","wrong_fragment","urgent","hot","num_failed_logins",
    "logged_in","num_compromised","root_shell","su_attempted","num_root",
    "num_file_creations","num_shells","num_access_files","num_outbound_cmds",
    "is_host_login","is_guest_login","count","srv_count","serror_rate",
    "srv_serror_rate","rerror_rate","srv_rerror_rate","same_srv_rate",
    "diff_srv_rate","srv_diff_host_rate","dst_host_count","dst_host_srv_count",
    "dst_host_same_srv_rate","dst_host_diff_srv_rate","dst_host_same_src_port_rate",
    "dst_host_srv_diff_host_rate","dst_host_serror_rate","dst_host_srv_serror_rate",
    "dst_host_rerror_rate","dst_host_srv_rerror_rate","label"]

df = pd.read_csv('dataset.csv', names=name)
df

df['label'] = df['label'].replace(['neptune.','ipsweep.','nmap.','satan.','smurf.','portsweep.','back.','teardrop.','guess_passwd.','pod.','warezmaster.','land.','imap.','ftp_write.','multihop.','buffer_overflow.','phf.','perl.','loadmodule.'],'attack')

df['protocol'] = df['protocol'].astype('category')
df['service'] = df['service'].astype('category')
df['flag'] = df['flag'].astype('category')
# df['label'] = df['label'].astype('category')
cat_columns = df.select_dtypes(['category']).columns
df[cat_columns] = df[cat_columns].apply(lambda x: x.cat.codes)

df

df.drop_duplicates(subset=None, keep='last', inplace=True)
df.shape

df['label'].value_counts(normalize= False, sort=True)

df['label'] = df['label'].astype('category')
cat_columns = df.select_dtypes(['category']).columns
df[cat_columns] = df[cat_columns].apply(lambda x: x.cat.codes)

df

df.isnull().sum()

data = df.values
data

x = data[:, 0:41]
x

y = data[:,41]
y

# scaler = StandardScaler()
# rescaleX = scaler.fit_transform(x)

# rescaleX

Normal = Normalizer()
xNormal = Normal.fit_transform(x)

xNormal

x.shape

y.shape

lab_encoder = LabelEncoder()
y = lab_encoder.fit_transform(y)

y

y.shape

x_train, x_test, y_train, y_test = train_test_split(x,y, train_size=0.7, shuffle=True, random_state=1)

x_train.shape

x_test.shape

y_test.shape

model = Sequential()
model.add(Dense(128,input_dim =41 , activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(1, activation='sigmoid'))
model.compile(optimizer = 'adam',
              loss = 'binary_crossentropy',
              metrics = [['accuracy'],['Precision'],['Recall']])
print(model.summary())

history = model.fit(x_train, y_train,
                    validation_split=0.2,
                    batch_size=32,
                    epochs=100,
                    callbacks=[
                               tf.keras.callbacks.EarlyStopping(
                                   monitor='val_loss',
                                   patience=3,
                                   restore_best_weights=True
                               )
                    ])

results = model.evaluate(x_test, y_test, verbose=0)


print(' Test loss: {:.4f}'.format(results[0]))
print('Accuracy: {:.2f}%'.format(results[1]*100))

from sklearn.metrics import confusion_matrix
y_pred = model.predict(x_test)
y_pred

y_pred = model.predict_classes(x_test)
y_pred

cm = confusion_matrix(y_test, y_pred)

cm

import seaborn as sns
sns.heatmap(cm/np.sum(cm), annot=True, 
            fmt='.2%', cmap='Blues')

sns.heatmap(cm, annot=True)