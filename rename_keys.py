import sqlite3
import json 
from pprint import pprint

db = 'nps.db'
con = sqlite3.connect(db)

all_new_parks = []
all_parks = con.execute('SELECT * FROM parks')
for park_row in all_parks:

    park_code, name, data = park_row
    print(park_code)
    print(name)
    park_dict = json.loads(data)
    print(park_dict['weather'])

    # got dictionary 

    images = park_dict['images']
    del park_dict['images']
    
    park_dict['nps_park_images'] = images

    weather = park_dict['weather']
    del park_dict['weather']
    park_dict['weather_overview'] = weather

    operating = park_dict['operating_hours']
    del park_dict['operating_hours']
    park_dict['park_operating_hours'] = operating

    park_json_str = json.dumps(park_dict)
    all_new_parks.append([park_code, name, park_json_str])


    
for park in all_new_parks:
    code, _, json_str = park
    print(json_str)
    
    con.execute('UPDATE parks SET park_info = ? WHERE park_code = ?', ( json_str, code) )

con.commit()
con.close()