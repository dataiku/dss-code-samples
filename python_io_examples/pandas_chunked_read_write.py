# -*- coding: utf-8 -*-
# This script reads a Dataiku dataset in chunks, applies a pandas transformation, and writes back the chunk

import dataiku
import pandas as pd

# Parameters
INPUT_DATASET_NAME = "foo"
CHUNKSIZE = 1000
OUTPUT_DATASET_NAME = "bar"

# Actual script
input_dataset = dataiku.Dataset(INPUT_DATASET_NAME)
output_dataset = dataiku.Dataset(OUTPUT_DATASET_NAME)

def my_custom_transformer(df):
    # i am a function! I can do many things!
    return(df)

i = 0
with output_dataset.get_writer() as writer:
    for chunk in input_dataset.iter_dataframes(chunksize = CHUNKSIZE, infer_with_pandas = False):
        print('Processing chunk %s with %s rows' % (i, chunk.shape[0]))
        transformed_chunk = chunk.apply(my_custom_transformer)
        if i == 0:
            output_dataset.write_schema_from_dataframe(transformed_chunk)
        else:
            writer.write_dataframe(transformed_chunk)
        i += 1