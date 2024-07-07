import pandas as pd
import  os
import sys
from sqlalchemy import create_engine
from shared_functions import *
from pathlib import Path

# Name of schema and table for store customer transactions data
schema_name = 'pre_prd'
table_name = 'product_catalog'

# Get the current directory (where this script is located)
current_dir = Path(sys.path[0])
print(current_dir)

# Construct the relative path to the JSON file
file_name = 'product_catalog[1].csv'
file_path = os.path.join(current_dir, '..', 'Sources', file_name)

df = pd.read_csv(file_path)

# Convert 'price' to numeric, invalid parsing will be set as NaN
df['price'] = pd.to_numeric(df['price'], errors='coerce')

# Filter out rows where 'price' is less than 0 or NaN
df = df[(df['price'] >= 0) & (df['price'].notna())]

# Function to generate product name based on product_id
def generate_product_name(row):
    if pd.isna(row['product_name']):
        product_num = row['product_id'][1:]  # Extract numeric part of product_id
        product_num_int = int(product_num)
        return f"Product {product_num_int}"
    return row['product_name']

# Apply function to 'product_name' column
df['product_name'] = df.apply(generate_product_name, axis=1)

# Store data to postgresql database
insert_into_postgres(df, table_name, schema_name)

