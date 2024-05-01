import findspark
findspark.init()

import pandas as pd

from pyspark.sql.session import SparkSession
spark = SparkSession.builder.getOrCreate()

def create_dummy_dataframe():
    data = {
        'A': [1, 2, 3, 4, 5],
        'B': ['a', 'b', 'c', 'd', 'e'],
        'C': ['1,2', '3,4', '', '5', '1,,3,5'],
        'D': ['1998-02-03 11:11:11',
              '2020-12-25 08:04:02',
              '02/15/1950 04:59',
              '09/07/1925 02:39',
              '05/28/1975 01:19',]
    }
    df = pd.DataFrame(data)
    return df, data

def test_spark_type():
    df, data = create_dummy_dataframe()
    df = spark.createDataFrame(df)
    df.toPandas()
    return df

if __name__ == '__main__':
    df = test_spark_type()
    print(df.head())