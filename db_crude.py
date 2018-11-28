from lib.db import Db
from lib.user import User

config = {
    'db':{
        'host':'localhost',
        'user' : 'dipendra',
        'password': 'postgres',
        'dbname ': 'webproject'
    }
}

try:
    Db.connect(config['db'])
     
     user = {
         'first_name': 'Dipendra',
         'middle_name': '',
         'last_name': 'Karki',
         'email': 'dipendra@gmail.com',
         'password': '1234'
     }

     u = User.remove(1)
     print(dict(u))
     Db.close()
except Exception as e:
    print(e)

    