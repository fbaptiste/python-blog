import os

from dotenv import load_dotenv


load_dotenv()

print('SWAPI_BASE_URL: ', os.getenv('SWAPI_BASE_URL'))
print('SWAPI_FILMS: ', os.getenv('SWAPI_FILMS'))
print('SECRET_1: ', os.getenv('SECRET_1'))
print('SECRET_2: ', os.getenv('SECRET_2'))

