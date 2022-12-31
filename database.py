from deta import Deta
import os
import streamlit as st
# from dotenv import load_dotenv

# load_dotenv('.env')

DETA_KEY = st.secrets["DETA_KEY"]


deta = Deta(DETA_KEY)

db = deta.Base('users_db')

def insert_user(username, name, password):
    return db.put({"key": username, 'name': name, 'password': password})

def fetch_all_users():
    res = db.fetch()
    return res.items

def get_user(username):
    return db.get(username)

def update_user(username, updates):
    return db.update(updates, username)

def delete_user(username):
    return db.delete(username)


# update_user('pparker', updates={'name': "Gabriel"})
# delete_user('pparker')


# print(get_user('rmiller')) -> is None
# print(get_user('pparker')) -> is {'key': 'pparker', 'name': 'Peter', 'password': 'abc123'}

# insert_user('pparker', 'Peter', 'abc123')
# print(fetch_all_users())



