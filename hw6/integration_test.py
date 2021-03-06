#!/usr/bin/env python
# coding: utf-8

from datetime import datetime
import pandas as pd
from sklearn.metrics import average_precision_score
import batch


def creat_input_file():
    data = [
        (None, None, dt(1, 2), dt(1, 10)),
        (1, 1, dt(1, 2), dt(1, 10)),
        (1, 1, dt(1, 2, 0), dt(1, 2, 50)),
        (1, 1, dt(1, 2, 0), dt(2, 2, 1)),
    ]

    columns = ['PUlocationID', 'DOlocationID', 'pickup_datetime', 'dropOff_datetime']
    df_input = pd.DataFrame(data, columns=columns)

    storage_options = {
        'client_kwargs': {'endpoint_url': 'http://localhost:4566'}
    }

    input_file = 's3://nyc-duration/ID1/testdata.parquet'

    df_input.to_parquet(
        input_file,
        engine='pyarrow',
        compression=None,
        index=False,
        storage_options=storage_options
    )

def test_integration_fhv():
    year = 2021
    month = 1

    input_file = batch.get_input_path(year, month)
    output_file = batch.get_output_path(year, month)

    batch.main(input_file, output_file, year, month)

    storage_options = {
        'client_kwargs': {'endpoint_url': 'http://localhost:4566'}
    }


    df_actual_result = pd.read_parquet(
        output_file,
        engine='pyarrow',
        storage_options=storage_options
    )

    print(df_actual_result)

    actual_sum_predicted_duration = df_actual_result['predicted_duration'].sum()

    print(f'actual_sum_predicted_duration={actual_sum_predicted_duration}')
    assert actual_sum_predicted_duration == 18031624.216666654

def test_integration_testdata():
    input_file = 's3://nyc-duration/ID1/testdata.parquet'
    output_file = 's3://nyc-duration/ID1/testdata_predictions.parquet'

    year = 2021
    month = 1
    batch.main(input_file, output_file, year, month)

    storage_options = {
        'client_kwargs': {'endpoint_url': 'http://localhost:4566'}
    }


    df_actual_result = pd.read_parquet(
        output_file,
        engine='pyarrow',
        storage_options=storage_options
    )

    print(df_actual_result)

    actual_sum_predicted_duration = df_actual_result['predicted_duration'].sum()

    print(f'actual_sum_predicted_duration={actual_sum_predicted_duration}')
    assert actual_sum_predicted_duration == 69.28869683240714


def dt(hour, minute, second=0):
    return datetime(2021, 1, 1, hour, minute, second)


if __name__ == "__main__":
    print("Create input file.")
    creat_input_file()
    print("Run integration test.")
    test_integration_testdata()

