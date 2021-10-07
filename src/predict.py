from tensorflow.keras.models import load_model
import numpy as np
import os
import time
from sequence import PaihuDataSequence


class Predictor:
    model = None

    def __init__(self):
        self.model = load_model(
            os.getcwd() +
            '/models/model.h5',
            custom_objects=None,
            compile=True,
            options=None)

    def predict(self, df):
        start = time.time()
        seq = PaihuDataSequence(df)
        encoded_x = np.expand_dims(seq.__getitem__(0)[0][0], axis=0)

        pred = self.model(encoded_x)
        prob_list = np.round(pred[0], 2)
        # print(np.round(pred, 2))

        elapsed_time = time.time() - start
        print("打牌決定時間:{0}".format(elapsed_time) + "[sec]")

        return np.argmax(pred[0]), prob_list

    def multi_predict(self, df):
        seq = PaihuDataSequence(df)
        # print(df.privateTehaiString)
        pred = self.model.predict(seq)
        # print('pred', pred)
        max_indexes = np.argmax(pred, axis=1)
        # print('max_indexes', np.round(max_indexes, 2))
        return max_indexes
