from tensorflow.keras.utils import Sequence
import math
import numpy as np
# from modules.convert_private_tehai import convert_selected_pai_to_num
import modules.encode as encode


class ActionPaihuDataSequence(Sequence):

    def __init__(self, df, batch_size=256, vmstat=False):
        self.df = df
        self.batch_size = batch_size
        self.vmstat = vmstat

    def __getitem__(self, i):
        sample_df = self.df.iloc[i *
                                 self.batch_size: (i + 1) * self.batch_size, :]

        # 手牌
        tehai_feature = np.array(
            list(map(encode.encode_tehai, sample_df.privateTehaiString.values)))

        # 河
        discard_feature = np.array(list(map(
            encode.encode_discard,
            sample_df.myPlayerDiscard.values,
            sample_df.lowerPlayerDiscard.values,
            sample_df.oppositePlayerDiscard.values,
            sample_df.upperPlayerDiscard.values
        )))

        # 副露
        meld_feature = np.array(list(map(
            encode.encode_discard,
            sample_df.myPlayerMeld.values,
            sample_df.lowerPlayerMeld.values,
            sample_df.oppositePlayerMeld.values,
            sample_df.upperPlayerMeld.values
        )))

        # ドラ表示牌
        dora_feature = np.array(
            list(map(encode.encode_dora, sample_df.doraOpen.values)))

        # プレイヤー
        player_feature = np.array(
            list(map(encode.encode_player, sample_df.player.values)))

        # リーチ
        # NOTE: 自分がリーチしている場合は除外
        reach_feature = [encode.encode_reach([i, j, k]) for i, j, k in zip(
            sample_df.isLowerPlayerReach.values,
            sample_df.isOppositePlayerReach.values,
            sample_df.isUpperPlayerReach.values
        )]

        # 場風
        bakaze_feature = np.array(
            list(map(encode.encode_bakaze, sample_df.bakaze.values)))

        # 局数
        kyoku_feature = np.array(
            list(map(encode.encode_kyoku, sample_df.kyokuNum.values)))

        # 持ち点
        lower_point_feature = np.array(list(map(
            encode.encode_point,
            sample_df.myPlayerPoints.values,
            sample_df.lowerPlayerPoints.values,
        )))
        opponent_point_feature = np.array(list(map(
            encode.encode_point,
            sample_df.myPlayerPoints.values,
            sample_df.oppositePlayerPoints.values,
        )))
        upper_point_feature = np.array(list(map(
            encode.encode_point,
            sample_df.myPlayerPoints.values,
            sample_df.upperPlayerPoints.values,
        )))

        # 安全牌
        safety_feature = [encode.encode_safety([i, j, k, l]) for i, j, k, l in zip(
            sample_df.myPlayerSafetyTile.values,
            sample_df.lowerPlayerSafetyTile.values,
            sample_df.oppositePlayerSafetyTile.values,
            sample_df.upperPlayerSafetyTile.values
        )]

        # 打牌者
        dahai_player_feature = np.array(
            list(map(encode.encode_player, sample_df.dahaiPlayer.values)))

        # 打牌
        selected_feature = np.array(
            list(map(encode.encode_dora, sample_df.selectedPai.values)))

        X = np.concatenate([
            tehai_feature,
            discard_feature,
            meld_feature,
            dora_feature,
            player_feature,
            reach_feature,
            bakaze_feature,
            kyoku_feature,
            lower_point_feature,
            opponent_point_feature,
            upper_point_feature,
            safety_feature,
            dahai_player_feature,
            selected_feature,
        ], 1)

        # レコード数×牌種数×チャネル数に変換
        X = X.reshape(-1, X.shape[1], 37)
        X = np.transpose(X, (0, 2, 1))

        Y = sample_df.action.values
        return X, Y

    def __len__(self):
        # バッチ数
        return math.ceil(len(self.df) / self.batch_size)

    def on_epoch_end(self):
        self.df = self.df.sample(frac=1)
