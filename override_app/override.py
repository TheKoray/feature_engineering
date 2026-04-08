import pandas as pd
import numpy as np


def getRatingData(musteri_or_grup='MUSTERI', model_tipi='TÜM MODELLER'):
    """Rating datasını SQL'den çeken fonksiyon. MUSTERI veya GRUP ve MODEL_TIPI'ye göre filtreleme yapar."""
    query = f"""
    SELECT
        SUM(pvt.[-5]) AS [-5],
        SUM(pvt.[-4]) AS [-4],
        SUM(pvt.[-3]) AS [-3],
        SUM(pvt.[-2]) AS [-2],
        SUM(pvt.[-1]) AS [-1],
        ISNULL(CAST(pvt.RATING AS VARCHAR), 'TOTAL') AS RATING,
        SUM(t.RATING_ADET) AS RATING_ADET,
        SUM(t.OVERRIDE_ADET) AS OVERRIDE_ADET,
        CAST(
            ROUND(
                SUM(t.OVERRIDE_ADET) * 100.0 / NULLIF(SUM(t.RATING_ADET), 0)
            , 2)
        AS DECIMAL(10,2)) AS OVERRIDE_ORAN,
        SUM(pvt.[0]) AS [+0],
        SUM(pvt.[+1]) AS [+1],
        SUM(pvt.[+2]) AS [+2],
        SUM(pvt.[+3]) AS [+3],
        SUM(pvt.[+4]) AS [+4],
        SUM(pvt.[+5]) AS [+5]
    FROM (
        SELECT *
        FROM (
            SELECT
                RAT_AFTER_EARLY_WARN AS RATING,
                OVERRIDE_NOTCHES_WT_DIRECTION,
                UNIQUE_ID
            FROM X
            WHERE MUSTERI_GRUP = '{musteri_or_grup}' and MODEL_TIPI = '{model_tipi}'
        ) AS data
        PIVOT (
            COUNT(UNIQUE_ID)
            FOR OVERRIDE_NOTCHES_WT_DIRECTION IN ([-5],[-4],[-3],[-2],[-1],[0],[+1],[+2],[+3],[+4],[+5])
        ) AS pvt
    ) pvt
    LEFT JOIN (
        SELECT
            RAT_AFTER_EARLY_WARN,
            COUNT(UNIQUE_ID) AS RATING_ADET,
            COUNT(CASE WHEN OVERRIDE_EDILMIS_FLAG = 1 THEN UNIQUE_ID END) AS OVERRIDE_ADET
        FROM X
        WHERE MUSTERI_GRUP = '{musteri_or_grup}' and MODEL_TIPI = '{model_tipi}'
        GROUP BY RAT_AFTER_EARLY_WARN
    ) t
    ON pvt.RATING = t.RAT_AFTER_EARLY_WARN
    GROUP BY ROLLUP(pvt.RATING)
    ORDER BY
        CASE WHEN pvt.RATING IS NULL THEN 1 ELSE 0 END,
        pvt.RATING
    """
    df = read_from_sql(query)
    return df


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
