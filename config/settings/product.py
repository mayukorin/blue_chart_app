# -*- coding: utf-8 -*-
"""
Created on Sat Jan  9 20:18:25 2021

@author: Mayuko
"""


from .base import *
import dj_database_url
from socket import gethostname
import cloudinary

hostname = gethostname()

db_from_env = dj_database_url.config()

DATABASES = {
    'default': dj_database_url.config()
}
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

ALLOWED_HOSTS = ['*']

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'doniovn9v',
    'API_KEY': '549853496254611',
    'API_SECRET': 'lnwOYqll249Tl2TmY1E8ybdJdTQ'
}

cloudinary.config(
  cloud_name = "doniovn9v",
  api_key = "549853496254611",
  api_secret = "lnwOYqll249Tl2TmY1E8ybdJdTQ"
)
