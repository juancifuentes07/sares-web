import os

class Config:
   
    USUARIO = 'system' 
    PASSWORD = '12345'
    HOST = 'localhost'
    PUERTO = '1521'
    SERVICIO = 'xe' 

    SQLALCHEMY_DATABASE_URI = ( f'oracle+oracledb://{USUARIO}:{PASSWORD}@{HOST}:{PUERTO}/?service_name={SERVICIO}')
    SQLALCHEMY_TRACK_MODIFICATIONS = False