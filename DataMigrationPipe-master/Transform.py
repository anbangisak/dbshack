import pandas as pd
from textblob import TextBlob
import json as JSON

def processTransform(dataDFList):
    for df in dataDFList:
        if (df[0] == 'id'):
            df[1] = processTable1(df[1])

    return dataDFList

def processTable1(df):
    df['sepallengthcm'] = df['sepallengthcm'].astype('float32')
    df['sepalwidthcm']  = df['sepalwidthcm'].astype('float32')
    df['petallengthcm'] = df['petallengthcm'].astype('float32')
    df['petalwidthcm']  = df['petalwidthcm'].astype('float32')
    df = df.dropna()
    return df

