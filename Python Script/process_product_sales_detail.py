
from sqlalchemy import create_engine
from dotenv import load_dotenv
import pandas as pd  
from shared_functions import *

# Tables pf customer_transactions and product_catalog
table_customer_transasctions = 'customer_transactions'
table_product_catalog = 'product_catalog'
schema_pre_prd = 'pre_prd'
# Table of processed data of customer_transactions and product_catalog
table_product_sales_detail = "product_sales_detail"
schema_prd = "prd"

# SQL query to join customer_transactions and product_catalog table and store into dataframe
query_join = f"""SELECT ct.transaction_id, ct.customer_id, ct.product_id, pc.product_name, pc.category ,ct.quantity, ct.price, CAST(ct.timestamp AS DATE) AS transaction_date
          FROM {schema_pre_prd}.{table_customer_transasctions} ct
          LEFT JOIN {schema_pre_prd}.{table_product_catalog} pc
          ON ct.product_id = pc.product_id"""
df = get_from_postgres(query_join)

# Calculate total price of each transaction from quantity of buy and price of products
df['total_price']= df['quantity'] * df['price']

# Reorder columns
new_columns = ['transaction_id', 'customer_id', 'product_id', 'product_name', 'category', 'quantity', 'price', 'total_price', 'transaction_date']
df = df.reindex(columns = new_columns)

# Store data to postgresql database
insert_into_postgres(df, table_product_sales_detail, schema_prd)