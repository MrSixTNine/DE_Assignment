import subprocess
import logging
import sys

# Setup logging to log to console
logging.basicConfig(stream=sys.stdout, level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def run_script(script_name):
    try:
        result = subprocess.run(['python', script_name], check=True, capture_output=True, text=True)
        logging.info(f"Successfully ran {script_name}: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Error running {script_name}: {e.stderr}")
        return False

def main():
    scripts = [
        'create_tables.py',
        'ingest_product_catalog.py',
        'ingest_customer_transactions.py',
        'process_product_sales_detail.py'
    ]
    
    for script in scripts:
        logging.info(f"Running script: {script}")
        if not run_script(script):
            logging.error(f"Pipeline stopped due to error in {script}")
            sys.exit(1)  # Exit the script if any script fails

if __name__ == '__main__':
    main()
