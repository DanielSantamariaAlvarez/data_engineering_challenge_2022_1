import requests
import pandas as pd
import haversine as hav

def callUsers():
    response = requests.get(API)
    if response.status_code == 200:
        users = []
        for user_id in range(5):
            llamado = requests.get('https://sccr8pgns0.execute-api.us-east-1.amazonaws.com/dev/locations/'+str(user_id)).json()["data"]
            print(llamado)
            users = llamado
    else:
        print("error en la api")

def createAirportsCsv():
    data = pd.read_csv('https://davidmegginson.github.io/ourairports-data/airports.csv')
    dataW = data[data["wikipedia_link"].notnull()]
    dataW.to_csv("airports_w_wiki.csv", encoding='utf-8', index=False)

if __name__ == '__main__':
    API_AIRPORTS = "https://davidmegginson.github.io/ourairports-data/airports.csv"
    API_USERS = "https://sccr8pgns0.execute-api.us-east-1.amazonaws.com/dev/locations"
    lon1 = -103.548851
    lat1 = 32.0004311
    lon2 = -103.6041946
    lat2 = 33.374939

    print(hav.haversine(lat1, lon1, lat2, lon2))


    