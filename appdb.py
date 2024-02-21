import mysql.connector

# Conectar a la base de datos
def conectar_bd():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="getmailbdoriginal"
    )
