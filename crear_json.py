import json
import haversine as hav
import pandas as pd


def loadUsers():
    with open('users.json') as f:
        users = json.load(f)
    return users

def loadUsersCountry():
    with open('users_country.json') as f:
        users_country = json.load(f)
    return users_country

def loadAirports():
    airports = pd.read_csv('airports_w_wiki.csv')
    return airports

def loadAirportsCountry():
    with open('airports_country.json') as f:
        airports_country = json.load(f)
    return airports_country



def crear_json():
    users = loadUsers()
    users_country = loadUsersCountry()
    airports = loadAirports()
    airports_country = loadAirportsCountry()
    ordenador = {}
    union = []
    paises_users = {}
    paises_airports ={}

    # Crear la lista de los paises y que usuarios están en ese país
    for i in range(len(users_country)):
        try:
            paises_users[users_country[i]].append(i)
        except:
            paises_users[users_country[i]]=[i]
    
    # Crear el diccionario de los paises y que aeropuertos perteneces a ese país
    for j in range(len(airports_country)):
        try:
            paises_airports[airports_country[j]].append(j)
        except:
            paises_airports[airports_country[j]] = [j]
    
    # Meter al diccionario los aeropuertos más cercanos a cada usuario
    for pais, usuarios in paises_users.items():

        try:
            lista_aeropuertos = paises_airports[pais]
            for i in usuarios:
                min = 999999999999
                aerop = {}
                for j in lista_aeropuertos:
                    user = users[i]
                    lati = user['latitude']['N']
                    long = user['longitude']['N']
                    aero = airports.iloc[j].to_dict()
                    latitud2 = float(aero['latitude_deg'])
                    longitud2 = float(aero['longitude_deg'])
                    distancia = hav.haversine((lati), (long), (longitud2), (latitud2))
                    if distancia > min:
                        min = distancia
                        aerop = aero
                dicc = user
                dicc.update({'distance':min})
                dicc.update(aerop)
                dicF = {i:dicc}
            ordenador.update(dicF)



        except:
            for i in usuarios:
                min = 999999999999
                aerop = {}
                for _, j in airports.iterrows():
                    user = users[i]
                    lati = float(user['latitude']['N'])
                    long = float(user['longitude']['N'])
                    aero = j.to_dict()
                    latitud2 = float(aero['latitude_deg'])
                    longitud2 = float(aero['longitude_deg'])
                    distancia = hav.haversine((lati), (long), (longitud2), (latitud2))
                    if distancia > min:
                        min = distancia
                        aerop = aero
                dicc = user
                dicc.update({'distance':min})
                dicc.update(aerop)
                dicF = {i:dicc}
            ordenador.update(dicF)
                    
        
    sorted(ordenador.keys())
    for i in ordenador:
        union.append(i)
    

    return union


with open('api.json','w') as f:
        json.dump(crear_json(), f, indent=4, ensure_ascii=False)

