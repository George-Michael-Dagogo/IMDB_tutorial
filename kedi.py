import requests

def get_coincap_data(coin_symbol):
    base_url = "https://api.coincap.io/v2"
    endpoint = f"/assets/{coin_symbol}"

    # Make the API request
    response = requests.get(base_url + endpoint)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        
        # Extract relevant information
        coin_data = data['data']
        
        # Print or return the data
        print(f"Name: {coin_data['name']}")
        print(f"Symbol: {coin_data['symbol']}")
        print(f"Price USD: {coin_data['priceUsd']}")
        print(f"Market Cap USD: {coin_data['marketCapUsd']}")
        print(f"24h Change: {coin_data['changePercent24Hr']}%")
        print(f"Circulating Supply: {coin_data['supply']} {coin_data['symbol']}")
        print(f"Total Supply: {coin_data['maxSupply']} {coin_data['symbol']}")
        
        # You can return the data if needed
        return coin_data
    else:
        # Print an error message if the request was not successful
        print(f"Error: {response.status_code}")
        return None

# Example: Get data for Bitcoin (BTC)
btc_data = get_coincap_data("bitcoin")
