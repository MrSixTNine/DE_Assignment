import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
import psycopg2
import pandas as pd
import time

# Load environment variables from config.env file
dotenv_path = os.path.join(os.path.dirname(__file__), 'config.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# Database connection details
DATABASE_TYPE = os.getenv('DATABASE_TYPE')
DBAPI = os.getenv('DBAPI')
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')
DATABASE = os.getenv('DATABASE')

def create_connection():
    """
    Create and return a connection to the PostgreSQL database.
    Retry up to 3 times with a delay of 5 seconds between retries.
    """
    attempts = 0
    max_attempts = 3
    conn = None
    while attempts < max_attempts:
        try:
            conn_string = f"dbname='{DATABASE}' user='{USER}' host='{HOST}' password='{PASSWORD}' port='{PORT}'"
            conn = psycopg2.connect(conn_string)
            print("Successfully connected to PostgreSQL!")
            return conn
        except psycopg2.Error as e:
            attempts += 1
            print(f"Attempt {attempts} failed: Error connecting to PostgreSQL: {e}")
            if attempts < max_attempts:
                print("Retrying...")
                time.sleep(5)  # Wait for 5 seconds before retrying
            else:
                print(f"Max retry attempts ({max_attempts}) reached. Could not connect to PostgreSQL.")
                return None

def create_table_to_postgres(query):
    """
    Execute a SQL query to create tables in PostgreSQL.
    
    Args:
    - query (str): SQL query to execute.
    """
    conn = create_connection()
    if conn is None:
        return
    
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        print("Successfully created schemas and tables")
    except psycopg2.Error as e:
        print(f"Error executing query: {e}")
    finally:
        if conn:
            conn.close()

def insert_into_postgres(df, table_name, schema_name):
    """
    Insert data from a pandas DataFrame into PostgreSQL table.
    
    Args:
    - df (pandas.DataFrame): DataFrame containing data to insert.
    - table_name (str): Name of the table to insert into.
    - schema_name (str): Name of the schema containing the table.
    """
    CONNECTION_URL = f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
    engine = create_engine(CONNECTION_URL)
    
    try:
        df.to_sql(table_name, engine, if_exists='append', index=False, schema=schema_name)
        print(f"Data successfully inserted into {schema_name}.{table_name}")
    except Exception as e:
        print(f"Error inserting data: {e}")
    finally:
        engine.dispose()

def get_from_postgres(query):
    """
    Execute a SQL query and return results as a pandas DataFrame.
    
    Args:
    - query (str): SQL query to execute.
    
    Returns:
    - pandas.DataFrame: Result of the query as a DataFrame.
    """
    conn = create_connection()
    if conn is None:
        return None
    
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(rows, columns=columns)
        return df
    except psycopg2.Error as e:
        print(f"Error executing query: {e}")
        return None
    finally:
        if conn:
            conn.close()

# Example usage
if __name__ == "__main__":
    create_tables_query = """
    CREATE SCHEMA IF NOT EXISTS pre_prd;
    
    CREATE TABLE IF NOT EXISTS pre_prd.product_catalog (
        product_id VARCHAR(10) NOT NULL,
        product_name VARCHAR(255) NOT NULL,
        category VARCHAR(255) NOT NULL,
        price FLOAT NOT NULL,
        created_by VARCHAR(255) DEFAULT 'Admin' NOT NULL,
        created_at TIMESTAMP DEFAULT timezone('Asia/Bangkok', NOW()),
        updated_by VARCHAR(255) DEFAULT 'Admin' NOT NULL,
        updated_at TIMESTAMP DEFAULT timezone('Asia/Bangkok', NOW()),
        CONSTRAINT product_product_id_pkey PRIMARY KEY(product_id)
    );
    
    CREATE TABLE IF NOT EXISTS pre_prd.customer_transactions (
        transaction_id VARCHAR(255) NOT NULL,
        customer_id VARCHAR(10) NOT NULL,
        product_id VARCHAR(10) NOT NULL,
        quantity INT NOT NULL,
        price FLOAT NOT NULL,
        "timestamp" TIMESTAMP,
        created_by VARCHAR(255) DEFAULT 'Admin' NOT NULL,
        created_at TIMESTAMP DEFAULT timezone('Asia/Bangkok', NOW()),
        updated_by VARCHAR(255) DEFAULT 'Admin' NOT NULL,
        updated_at TIMESTAMP DEFAULT timezone('Asia/Bangkok', NOW()),
        CONSTRAINT customer_transactions_transaction_id_pkey PRIMARY KEY(transaction_id),
        CONSTRAINT customer_transaction_product_id_fkey FOREIGN KEY (product_id) REFERENCES pre_prd.product_catalog(product_id)
    );
    
    CREATE TABLE IF NOT EXISTS prd.product_sales_detail (
        transaction_id VARCHAR(255) NOT NULL,
        customer_id VARCHAR(10) NOT NULL,
        product_id VARCHAR(10) NOT NULL,
        product_name VARCHAR(255) NOT NULL,
        category VARCHAR(255) NOT NULL,
        quantity INT NOT NULL,
        price FLOAT NOT NULL,
        total_price FLOAT NOT NULL,
        transaction_date DATE NOT NULL,
        created_by VARCHAR(255) DEFAULT 'Admin' NOT NULL,
        created_at TIMESTAMP DEFAULT timezone('Asia/Bangkok', NOW()),
        updated_by VARCHAR(255) DEFAULT 'Admin' NOT NULL,
        updated_at TIMESTAMP DEFAULT timezone('Asia/Bangkok', NOW()),
        CONSTRAINT product_sales_detail_transaction_id_pkey PRIMARY KEY(transaction_id),
        CONSTRAINT product_sales_detail_product_id_fkey FOREIGN KEY (product_id) REFERENCES pre_prd.product_catalog(product_id)
    );
    """
    
    # Create tables in PostgreSQL
    create_table_to_postgres(create_tables_query)
    
    # Example DataFrame to insert into PostgreSQL
    data = {
        'product_id': ['P001', 'P002'],
        'product_name': ['Product A', 'Product B'],
        'category': ['Category X', 'Category Y'],
        'price': [100.0, 200.0]
    }
    df = pd.DataFrame(data)
    
    # Insert into PostgreSQL
    insert_into_postgres(df, 'product_catalog', 'pre_prd')
    
    # Example query to fetch data from PostgreSQL
    query = "SELECT * FROM pre_prd.product_catalog"
    result_df = get_from_postgres(query)
    if result_df is not None:
        print("Data fetched successfully:")
        print(result_df)
