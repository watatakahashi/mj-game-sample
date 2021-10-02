import tensorflow as tf
from tensorflow import keras
import numpy as np
import pandas as pd
import os
import time

from sequence import PaihuDataSequence

class Predictor:
    model = None

    def __init__(self):
        self.model = tf.keras.models.load_model(
           os.getcwd() + '/models/model.h5', custom_objects=None, compile=True, options=None
            )

    def predict(self, df):
        start = time.time()

        pred = self.model.predict(PaihuDataSequence(df))
        prob_list = np.round(pred[0], 2)
        # print(np.round(pred, 2))

        elapsed_time = time.time() - start
        print("打牌決定時間:{0}".format(elapsed_time) + "[sec]")

        return np.argmax(pred[0]), prob_list
