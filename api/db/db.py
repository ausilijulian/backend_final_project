from flask_mysqldb import MySQL
from api import app


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'user_project_final' #user_project_final
app.config['MYSQL_PASSWORD'] ='pass_project_final' #pass_project_final
app.config['MYSQL_DB'] = 'db_final_project'  

mysql = MySQL(app) 