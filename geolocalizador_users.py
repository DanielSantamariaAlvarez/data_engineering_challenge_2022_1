from geopy.geocoders import Nominatim
import json
import time 
geolocator = Nominatim(user_agent="usuarios")
users = None
list_users = []
with open('users.json') as f:
    users = json.load(f)

def cargar_users():

    for i in range(1000):
        user = users[i]
        lati = user['latitude']['N']
        long = user['longitude']['N']
        lalo = f'{lati}, {long}'
        localization = geolocator.reverse(lalo)
        if localization == None:
            list_users.append("none")
        else:
            try:
                list_users.append(localization.raw['address']['country'])
            except:
                list_users.append("none")


inicio = time.time()
cargar_users()

    
with open('users_country.json','w') as f:
        json.dump(list_users, f, indent=4, ensure_ascii=False)
fin = time.time()
print(fin-inicio)