from dotenv import load_dotenv, find_dotenv
import os
load_dotenv(find_dotenv())

path_to_driver = os.getenv('path_to_gecko')
start_url = os.getenv('start_url')
host_db = os.getenv('host_db')
password_db = os.getenv('password_db')
name_db = os.getenv('name_db')
username_db = os.getenv('username_db')