import json
import pandas as pd
import os
from shared_functions import *
import sys
from pathlib import Path
from dotenv import load_dotenv

# Name of schema and table for store customer transactions data
schema_name = 'pre_prd'
table_name = 'customer_transactions'

# Get the current directory (where this script is located)
current_dir = Path(sys.path[0])

# Construct the relative path to the JSON file
file_name = 'customer_transactions[2].json'
file_path = os.path.join(current_dir, '..', 'Sources', file_name)

# Read JSON file to datafram
with open(file_path, 'r') as file:
    data = json.load(file)
df = pd.DataFrame(data)

# Convert data type
df['transaction_id'] = df['transaction_id'].astype(str)
df['customer_id'] = df['customer_id'].astype(str)
df['product_id'] = df['product_id'].astype(str)
df['quantity'] = df['quantity'].astype(int)
df['price'] = df['price'].astype(float)
df['timestamp'] = pd.to_datetime(df['timestamp'])

## Clean data
# Drop row if transaction_id duplicates 
df.drop_duplicates(subset='transaction_id', keep="first", inplace=True)
# Drop NA value of customer_id and product_id
df.dropna(subset=['customer_id','product_id'], inplace=True)
# Convert 'price' and 'quantity' to numeric, invalid parsing will be set as NaN
df['price'] = pd.to_numeric(df['price'], errors='coerce')
df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')
# Filter out rows where 'price' is less than 0 or NaN
df = df[(df['price'] >= 0) & (df['price'].notna())]
df = df[(df['quantity'] >= 0) & (df['price'].notna())]

# Store data to postgresql database
insert_into_postgres(df, table_name, schema_name)


