import pandas as pd
import requests

def download_file(url, filename):
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(filename, 'wb') as f:
            f.write(response.content)
    except requests.exceptions.RequestException as e:
        print(e)
        return None

def read_csv_file(filename):
    try:
        return pd.read_csv(filename, skipinitialspace=True)
    except (pd.errors.EmptyDataError, pd.errors.ParserError, FileNotFoundError) as e:
        print(e)
        return None

def merge_files():
    women_url = 'https://people.sc.fsu.edu/~jburkardt/data/csv/oscar_age_female.csv'
    men_url = 'https://people.sc.fsu.edu/~jburkardt/data/csv/oscar_age_male.csv'
    
    if download_file(women_url, 'oscar_age_female.csv') is None:
        return
    if download_file(men_url, 'oscar_age_male.csv') is None:
        return
    
    women_data = read_csv_file('oscar_age_female.csv')
    if women_data is None:
        return
    
    men_data = read_csv_file('oscar_age_male.csv')
    if men_data is None:
        return

    women_data['Gender'] = 'F'
    men_data['Gender'] = 'M'
    
    all_data = pd.concat([women_data, men_data])
    all_data = all_data.sort_values(['Year', 'Gender'])
    all_data = all_data.reset_index(drop=True)
    all_data['Index'] = all_data.index + 1
    
    try:
        all_data.to_csv('oscar_age_gender.csv', index=False, quoting=2)
    except (PermissionError, IOError) as e:
        print(e)

if __name__ == "__main__":
    merge_files()
