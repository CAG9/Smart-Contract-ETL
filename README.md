# Smart Contract ETL
 A ETL to extract contract's deployer address and transaction hash from the smart contracts related to Tether in Coinbase
## Result
![alt text](https://github.com/CAG9/Smart-Contract-ETL/blob/main/Smart-contract-Result.png)
## Requirements
- Coinbase API
- Etherscan API 

## Tools and Technologies
- Python 3
- requests
- json
- pprint
- time
- numpy 
- pandas as pd
- mysql.connector

## More info
### Coinbase https://pro-api.coinmarketcap.com/v2/cryptocurrency/info
Returns all static metadata available for one or more cryptocurrencies. This information includes details like logo, description, official website URL, social links, and links to a cryptocurrency's technical documentation.
### Etherscan Url
Return a contract's deployer address and transaction hash it was craeted
### TxHash
Transaction hash (txid) is an identifier used to uniquely identify a particular transaction.
