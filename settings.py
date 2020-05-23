from dotenv import load_dotenv, find_dotenv
import os
load_dotenv(find_dotenv())

path_to_driver = os.getenv('path_to_gecko')
start_url = os.getenv('start_url')