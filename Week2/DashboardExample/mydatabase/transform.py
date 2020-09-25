import pandas as pd
import sqlite3


def get_data():
    conn = sqlite3.connect(r"./mydatabase/wine_data.sqlite")
    c = conn.cursor()
    df = pd.read_sql("select * from wine_data", conn)
    #df = df[['country', 'description', 'rating', 'price', 'province', 'title', 'winery', 'color']]
    df = df[['country', 'description', 'rating', 'price', 'province', 'title', 'variety', 'winery', 'color', 'varietyID']]
    return df
