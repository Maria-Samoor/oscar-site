import pandas as pd
import requests
import logging
import os 

# create logs directory if it does not exist 
os.makedirs('logs', exist_ok=True)

# get the logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# create file handler for info level logs
info_logger = logging.FileHandler('logs/info.log', mode='w')
info_logger.setLevel(logging.INFO)  

# create file handler for error level logs
error_logger = logging.FileHandler('logs/errors.log', mode='w')
error_logger.setLevel(logging.ERROR)  # only capture error messages

# create a simple log message format
log_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
info_logger.setFormatter(log_format)
error_logger.setFormatter(log_format)

# add both handlers to the logger
logger.addHandler(info_logger)
logger.addHandler(error_logger)

def download_file(url, filename):
    """download a file from given url"""
    try:
        logger.info(f"starting download of {filename}")
        response = requests.get(url, timeout=10)
        response.raise_for_status() 
        with open(filename, 'wb') as f:
            f.write(response.content)
        logger.info(f"successfully downloaded {filename}")
        return True  
    except requests.exceptions.RequestException as e:
        logger.error(f"download failed for {filename}: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"unexpected error downloading {filename}: {str(e)}")
        return False

def read_csv_file(filename):
    """read a csv file into a pandas dataframe"""
    try:
        logger.info(f"reading file: {filename}")
        df = pd.read_csv(filename, skipinitialspace=True)
        logger.info(f"successfully read {filename}")
        return df
    except pd.errors.EmptyDataError:
        logger.error(f"file is empty: {filename}")
        return None
    except pd.errors.ParserError:
        logger.error(f"file format problem: {filename}")
        return None
    except FileNotFoundError:
        logger.error(f"file not found: {filename}")
        return None
    except Exception as e:
        logger.error(f"error reading {filename}: {str(e)}")
        return None

def merge_files():
    """main function to download, merge and save oscar data"""
    logger.info("starting data processing")
    
    women_url = 'https://people.sc.fsu.edu/~jburkardt/data/csv/oscar_age_female.csv'
    men_url = 'https://people.sc.fsu.edu/~jburkardt/data/csv/oscar_age_male.csv'
    output_file = 'oscar_age_gender.csv'
    
    if not download_file(women_url, 'oscar_age_female.csv'):
        logger.error("failed to download women's data")
        return
    if not download_file(men_url, 'oscar_age_male.csv'):
        logger.error("failed to download men's data")
        return
    
    women_data = read_csv_file('oscar_age_female.csv')
    if women_data is None:
        logger.error("couldn't read women's data")
        return
    men_data = read_csv_file('oscar_age_male.csv')
    if men_data is None:
        logger.error("couldn't read men's data")
        return
    
    try:
        logger.info("merging datasets")
        women_data['Gender'] = 'F'
        men_data['Gender'] = 'M'
        combined_data = pd.concat([women_data, men_data])
        combined_data = combined_data.sort_values(['Year', 'Gender'])
        combined_data = combined_data.reset_index(drop=True)
        combined_data['Index'] = combined_data.index + 1
        try:
            combined_data.to_csv(output_file, index=False, quoting=2)
            logger.info(f"saved merged data to {output_file}")
        except (PermissionError, IOError):
            logger.error(f"couldn't save file (permission issue): {output_file}")
        except Exception as e:
            logger.error(f"unexpected error saving file: {output_file} - {str(e)}")        
    except Exception as e:
        logger.error(f"error during data merging and processing: {str(e)}")

if __name__ == "__main__":
    logger.info("script started")
    merge_files()
    logger.info("script finished")