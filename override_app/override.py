import pandas as pd
import numpy as np


def getRatingData(musteri_or_grup='MUSTERI'):
    df = pd.read_csv("rating_adet.csv", index_col=0)
    rename_map = {'0': '+0', '1': '+1', '2': '+2', '3': '+3', '4': '+4', '5': '+5'}
    df = df.rename(columns=rename_map)
    return df


def getAllModelsRatingData(musteri_or_grup='MUSTERI'):
    return getRatingData(musteri_or_grup=musteri_or_grup)


def getReasonData(musteri_or_grup='MUSTERI'):
    return pd.read_csv("reason.csv", sep=';')


def getAllModelsReasonData(musteri_or_grup='MUSTERI'):
    return getReasonData(musteri_or_grup=musteri_or_grup)


def getBolgeData(musteri_or_grup='MUSTERI'):
    return pd.read_csv("bolge.csv", sep=';', encoding='latin-1')


def getAllModelsBolgeData(musteri_or_grup='MUSTERI'):
    return getBolgeData(musteri_or_grup=musteri_or_grup)


def getOverallData(musteri_or_grup='MUSTERI'):
    pass


def getAllModelsOverallData(musteri_or_grup='MUSTERI'):
    pass


def generate_color_scale():
    pass


def generate_color_scale_str():
    pass
