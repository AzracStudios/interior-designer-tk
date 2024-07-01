import os
import mysql.connector
from mysql.connector import errorcode
import argparse
from uuid import uuid4
import hashlib
from utils import encrypt, correct_path

from sql.tables import TABLES

parser = argparse.ArgumentParser(
    prog="Urban Utopia Admin",
)

parser.add_argument("u")
parser.add_argument("p")

args = parser.parse_args()

MYSQL_USERNAME = args.u
MYSQL_PASSWORD = args.p
MYSQL_DBNAME = "urban_utopia"
FILE_STORE_LOCATION = f"{'/'.join(__file__.split(os.sep)[:-1])}/data/"

connection = mysql.connector.connect(
    user=MYSQL_USERNAME,
    password=MYSQL_PASSWORD,
    host="127.0.0.1",
)

cursor = connection.cursor(buffered=True)

## Create and use database
cursor.execute(f"create database if not exists {MYSQL_DBNAME}")
cursor.execute(f"use {MYSQL_DBNAME}")

## Create tables
for table_name, table_desc in TABLES.items():
    try:
        cursor.execute(table_desc)
    except mysql.connector.Error as err:
        continue


def store_image(file_path):
    file_ext = file_path.split(os.sep)[-1].split(".")[-1]

    new_file_name = f"{uuid4()}.{file_ext}"
    new_file_loc = FILE_STORE_LOCATION + new_file_name
    
    with open(file_path, "rb") as src:
        with open(correct_path(new_file_loc), "wb") as dest:
            dest.writelines(src.readlines())

    return new_file_loc


def login_user(email, password, hashed=False):
    cursor.execute(f"select password from users where email='{email}'")
    real_pwd = cursor.fetchone()

    if real_pwd is None:
        return -1

    if (encrypt(password) if not hashed else password) != real_pwd[0]:
        return 0

    return 1


def register_user(fullname, email, password, hashed=False):
    cursor.execute(
        f"insert into users (uid, name, email, password) values ('{uuid4()}', '{fullname}', '{email}', '{encrypt(password)}')"
    )

    connection.commit()

    return 1

def get_name(email):
    cursor.execute(
        f"select name from users where email='{email}'"
    )

    return cursor.fetchone()[0]


def change_password(email, password):
    cursor.execute(f"select * from users where email='{email}'")
    user = cursor.fetchone()
    if user == None:
        return -1

    cursor.execute(
        f"update users set password='{encrypt(password)}' where email='{email}'"
    )

    connection.commit()

    return 1


def get_user(email):
    cursor.execute(f"select * from users where email='{email}'")
    return cursor.fetchone()


def fetch_rooms():
    cursor.execute("select * from rooms")
    return cursor.fetchall()


def fetch_room_by_id(id):
    cursor.execute(f"select * from rooms where uid='{id}'")
    return cursor.fetchone()


def fetch_styles():
    cursor.execute(f"select * from styles")
    return cursor.fetchall()


def fetch_style_by_id(id):
    cursor.execute(f"select * from styles where uid='{id}'")
    return cursor.fetchone()


def fetch_designs(roomid, styleid):
    cursor.execute(
        f"select * from designs where roomId='{roomid}' and styleId='{styleid}'"
    )
    print(roomid, styleid)
    res = cursor.fetchall()
    print(res)
    return res


def fetch_design_by_id(id):
    cursor.execute(f"select * from designs where uid='{id}'")
    return cursor.fetchone()


# cursor.close()
# connection.close()
