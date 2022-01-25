import requests
import pandas as pd
import haversine as hav
import numba
import json

@numba.jit
def callUsers(users):
    response = requests.get("https://sccr8pgns0.execute-api.us-east-1.amazonaws.com/dev/locations")
    if response.status_code == 200:
        for user_id in range(10000):
            llamado = requests.get('https://sccr8pgns0.execute-api.us-east-1.amazonaws.com/dev/locations/'+str(user_id)).json()["data"]
            users.append(llamado)
    else:
        print("error en la api")
    print(users)

def createUsersInJson():
    # Tiempo aproximado de hora a hora y media para traer los 10000 usuarios
    # con mi internet de 6 megas
    users=[]
    callUsers(users)
    with open('users.json','w') as f:
        json.dump(users, f, indent=4)

def createAirportsCsv():
    data = pd.read_csv('https://davidmegginson.github.io/ourairports-data/airports.csv')
    dataW = data[data["wikipedia_link"].notnull()]
    dataW.to_csv("airports_w_wiki.csv", encoding='utf-8', index=False)

def loadUsers():
    users = None
    with open('users.json') as f:
        users = json.load(f)
    return users

@numba.jit
def createJsonAirport():
    json1 = []
    users = loadUsers()
    data = pd.read_csv('airports_w_wiki.csv')

    for i in users:
        latitud1 = float(i['latitude']['N'])
        longitud1 = float(i['longitude']['N'])
        id = int(i['user_id']['N'])
        max = 0
        airport = ''

        for _, fila in data.iterrows():
            j = fila.to_dict()
            latitud2 = float(j['latitude_deg'])
            longitud2 = float(j['longitude_deg'])
            distancia = hav.haversine((longitud1), (latitud1), (longitud2), (latitud2))
            if distancia > max:
                max = distancia
                airport = j
        newDict = {'user_id':id, 'latitude':latitud1, 'longitude':longitud1}
        newDict.update({'distance':max})
        newDict.update(airport)
        finalDict = {id:newDict}
        json1.append(finalDict)
        
    return json


    


if __name__ == '__main__':
    API_AIRPORTS = "https://davidmegginson.github.io/ourairports-data/airports.csv"
    API_USERS = "https://sccr8pgns0.execute-api.us-east-1.amazonaws.com/dev/locations"

    users = createJsonAirport()
    with open('airports.json', 'w') as f:
        json.dump(users, f, indent=4)



    


    