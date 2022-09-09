from requests import Request, Session,get
import json
import pprint
import time
import numpy as np
import pandas as pd
import mysql.connector

import coinbase_key
import etherscan_key
import database


coinbase_api_key = coinbase_key.KEY
etherscan_api_key = etherscan_key.KEY
BASE_URL = "https://api.etherscan.io/api"
my_db = mysql.connector.connect(host = 'localhost',
                                user = database.USER,
                                password = database.PASSWORD,
                                database = database.DATABASE)
cursor = my_db.cursor()





def make_url_etherscan(module, action, address, **kwargs):
    url = BASE_URL + f"?module={module}&action={action}&contractaddresses={address}&apikey={etherscan_api_key}"
    for key, value in kwargs.items():
        url += f"&{key}={value}"
    return url

def get_smart_contracts(coinbase_api_key,url):
    url = url
    parameters = {
    'slug':"tether"
    }

    headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': coinbase_api_key
    }
    session = Session()
    session.headers.update(headers)
    response = session.get(url,params = parameters)
    contracts = json.loads(response.text)
    return contracts

def process_coinbase_data(contracts):
    contracts_addresses = []
    contracts_name = []
    for contract in (contracts['data']['825']['contract_address']):
        contracts_addresses.append(contract['contract_address'])
        contracts_name.append(contract['platform']['name'])
    return contracts_addresses,contracts_name

def etherscan_contracts(contracts_addresses):
    count_batch = 0
    contract_creator = []
    txHash = []
    for address in contracts_addresses:
        get_url = make_url_etherscan("contract","getcontractcreation",address)
        response = get(get_url)
        data = response.json()
        print('Working ...')
        if data['status'] == '1':
            contract_creator.append(data['result'][0]['contractCreator'])
            txHash.append(data['result'][0]['txHash'])

        else:
            contract_creator.append(np.nan)
            txHash.append(np.nan)

        count_batch += 1
        if count_batch == 5:
            count_batch = 0
            time.sleep(6)
    return contract_creator,txHash

def create_dataframe(contracts_addresses,contracts_name,contract_creator,txHash):
    data = {'address': contracts_addresses,
            'name': contracts_name,
            'creator_address':contract_creator,
            'txHash':txHash}
    df = pd.DataFrame(data)
    return df
  
def clean_Dataset(dataframe):
    return dataframe[dataframe['txHash'].notnull()]

def load(dataframe):

    print(f"Uploading {dataframe.shape[0]} to db")

    cursor.execute('CREATE TABLE IF NOT EXISTS contracts (address VARCHAR(300), name VARCHAR(300), creator_address VARCHAR(300),txHash VARCHAR(300))')

    for index, row in dataframe.iterrows():
        query = """INSERT INTO contracts (address, name, creator_address,txHash)VALUES (%s, %s, %s,%s) """
        record = (row['address'], row['name'], row['creator_address'], row['txHash'])
        cursor.execute(query, record)
        my_db.commit()




if __name__ == "__main__":
    coinbase_url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/info'
    contracts = get_smart_contracts(coinbase_api_key,coinbase_url)
    contracts_addresses,contracts_name = process_coinbase_data(contracts) # dataset1 contains:contracts_addresses and contracts_name
    contract_creator,txHash = etherscan_contracts(contracts_addresses)
    dataframe = create_dataframe(contracts_addresses,contracts_name,contract_creator,txHash)
    dataframe = clean_Dataset(dataframe)
    load(dataframe)
    print('Done!')



    
    
     
     






