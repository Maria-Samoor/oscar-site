import pandas as pd
import requests
import csv

def download_file(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(response.content)

def merge_files():
    women_url = 'https://people.sc.fsu.edu/~jburkardt/data/csv/oscar_age_female.csv'
    men_url = 'https://people.sc.fsu.edu/~jburkardt/data/csv/oscar_age_male.csv'    
    download_file(women_url, 'oscar_age_female.csv')
    download_file(men_url, 'oscar_age_male.csv')
    women_data = pd.read_csv('oscar_age_female.csv', skipinitialspace=True)
    men_data = pd.read_csv('oscar_age_male.csv', skipinitialspace=True)
    women_data['Gender'] = 'F'
    men_data['Gender'] = 'M'
    all_data = pd.concat([women_data, men_data])
    all_data = all_data.sort_values(['Year', 'Gender'])
    all_data = all_data.reset_index(drop=True)
    all_data['Index'] = all_data.index + 1
    all_data.to_csv('oscar_age_gender.csv', index=False, quoting=2)

if __name__ == "__main__":
    merge_files()
