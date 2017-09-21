#!/usr/bin/env python

import pandas as pd
from glob import glob
import os, sys

def clean_str_cols(df, encoding='ascii'):
    """
    As string columns are stored as 'objects' it can cause many problems, especially when reading and writig CSVs. This function
    forces the columns to be strings and be encoded as a specified encoding.
    
    Solves `UnicodeEncodeError` errors when using `to_csv`.
    """
    df = df.copy()

    for col, dtype in df.dtypes.items():
        if dtype.kind == 'O':   # If string datatype
            df[col] = df[col].astype('str')  # The col can be reported as being a object when it contains mixed datatypes
            df[col] = df[col].str.encode(encoding, errors='ignore').str.decode(encoding)

    return df

header_folder = 'headers'
zip_extract_folder = 'zip_extract'
output_folder = 'output'

# If first argumnet file name. Restart from that position
first_file = None
if len(sys.argv) > 1:
	first_file = sys.argv[1]

file_map = {
    # RECORD_IDENTIFIER -> Output file, Header file
    10: ('ID10_Header_Records.csv',     'Record_10_HEADER_Header.csv'),
    11: ('ID11_Street_Records.csv',     'Record_11_STREET_Header.csv'),
    15: ('ID15_StreetDesc_Records.csv', 'Record_15_STREETDESCRIPTOR_Header.csv'),
    21: ('ID21_BLPU_Records.csv',       'Record_21_BLPU_Header.csv'),
    23: ('ID23_XREF_Records.csv',       'Record_23_XREF_Header.csv'),
    24: ('ID24_LPI_Records.csv',        'Record_24_LPI_Header.csv'),
    28: ('ID28_DPA_Records.csv',        'Record_28_DELIVERYPOINTADDRESS_Header.csv'),
    29: ('ID29_Metadata_Records.csv',   'Record_29_METADATA_Header.csv'),
    30: ('ID30_Successor_Records.csv',  'Record_30_SUCCESSOR_Header.csv'),
    31: ('ID31_Org_Records.csv',        'Record_31_ORGANISATION_Header.csv'),
    32: ('ID32_Class_Records.csv',      'Record_32_CLASSIFICATION_Header.csv'),
    99: ('ID99_Trailer_Records.csv',    'Record_99_TRAILER_Header.csv'),
}

open_files = {} # Need here so 'finally' doesn't throw an exception
try:
    ## Open files and write headers
    number_of_columns = {} # Record how many columns
    for rec_id, (output_file, header_file) in file_map.items():
        header_file_path = os.path.join(header_folder, header_file)
        output_file_path = os.path.join(output_folder, output_file)

        data = pd.read_csv(header_file_path)
        open_mode = "w" if first_file is None else "a"  # Append if restarting
        open_file = open(output_file_path, open_mode)
        
        if first_file is None:  # Only write if not restarting
            data.to_csv(open_file, index=False)

        open_files[rec_id] = open_file
        number_of_columns[rec_id] = data.shape[1]

    ## Split and merge data
    input_files = glob(os.path.join(zip_extract_folder, '*.csv'))
    input_files = sorted(input_files)
	
    # Restart from where we left off
    if first_file is not None:
        first_file = os.path.join(zip_extract_folder, first_file)
        first_file_ix = input_files.index(first_file)
        input_files = input_files[first_file_ix:]
        print("Restarting from", first_file)

    n_files = len(input_files)
    for i, input_file in enumerate(input_files):
        print("File number {} out of {} Reading {}".format(i+1, n_files, os.path.basename(input_file)))

        max_number_of_cols = max(number_of_columns.values())
        data = pd.read_csv(input_file, header=None, names=range(max_number_of_cols), error_bad_lines=False, warn_bad_lines=True)
        
        for rec_id, sub_data in data.groupby(0):
            rec_id = int(rec_id)
            open_file = open_files[rec_id]
            n_cols = number_of_columns[rec_id]
            try:
                sub_data.iloc[:,:n_cols].to_csv(open_file, header=None, index=False, mode='a', encoding='utf8')
            except UnicodeEncodeError:
                # Some of the files are currupt and for others Pandas gets confused due to the mixed datatypes
                clean_str_cols(sub_data.iloc[:,:n_cols]).to_csv(open_file, header=None, index=False, mode='a', encoding='utf8')
        
finally:
    # Allways close files
    for rec_id, open_file in open_files.items():
        open_file.close()
    print("Closed all files")
