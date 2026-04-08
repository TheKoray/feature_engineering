import pandas as pd
import numpy as np


def getRatingData(musteri_or_grup='MUSTERI', model_tipi='TÜM MODELLER'):
    df = pd.read_csv("rating_adet.csv")
    df = df[df['MUSTERI_OR_GRUP'] == musteri_or_grup].copy()
    if model_tipi and model_tipi != 'TÜM MODELLER':
        df = df[df['MODEL_TIPI'] == model_tipi].copy()
    df = df.drop(columns=['MUSTERI_OR_GRUP', 'MODEL_TIPI'])
    rename_map = {'0': '+0', '1': '+1', '2': '+2', '3': '+3', '4': '+4', '5': '+5'}
    df = df.rename(columns=rename_map)
    return df


def getAllModelsRatingData(musteri_or_grup='MUSTERI'):
    return getRatingData(musteri_or_grup=musteri_or_grup, model_tipi='TÜM MODELLER')


def getReasonData(musteri_or_grup='MUSTERI', model_tipi='TÜM MODELLER'):
    df = pd.read_csv("reason.csv", sep=';')
    df.columns = [c.strip().replace('"', '') for c in df.columns]
    df = df[df['MUSTERI_OR_GRUP'] == musteri_or_grup].copy()
    if model_tipi and model_tipi != 'TÜM MODELLER':
        df = df[df['MODEL_TIPI'] == model_tipi].copy()
    return df.drop(columns=['MUSTERI_OR_GRUP', 'MODEL_TIPI'])


def getAllModelsReasonData(musteri_or_grup='MUSTERI'):
    return getReasonData(musteri_or_grup=musteri_or_grup, model_tipi='TÜM MODELLER')


def getBolgeData(musteri_or_grup='MUSTERI', model_tipi='TÜM MODELLER'):
    df = pd.read_csv("bolge.csv", sep=';', encoding='utf-8')
    df.columns = [c.strip() for c in df.columns]
    df = df[df['MUSTERI_OR_GRUP'] == musteri_or_grup].copy()
    if model_tipi and model_tipi != 'TÜM MODELLER':
        df = df[df['MODEL_TIPI'] == model_tipi].copy()
    return df.drop(columns=['MUSTERI_OR_GRUP', 'MODEL_TIPI'])


def getAllModelsBolgeData(musteri_or_grup='MUSTERI'):
    return getBolgeData(musteri_or_grup=musteri_or_grup, model_tipi='TÜM MODELLER')


def getOverallData(musteri_or_grup='MUSTERI', model_tipi='TÜM MODELLER'):
    df = pd.read_csv("overall.csv", sep=';')
    df = df[df['MUSTERI_OR_GRUP'] == musteri_or_grup].copy()
    if model_tipi and model_tipi != 'TÜM MODELLER':
        df = df[df['MODEL_TIPI'] == model_tipi].copy()
    return df.drop(columns=['MUSTERI_OR_GRUP', 'MODEL_TIPI'])


def getAllModelsOverallData(musteri_or_grup='MUSTERI'):
    return getOverallData(musteri_or_grup=musteri_or_grup, model_tipi='TÜM MODELLER')


def generate_color_scale():
    pass


def generate_color_scale_str():
    pass
