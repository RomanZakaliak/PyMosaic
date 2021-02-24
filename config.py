"""
    This file contains some settings for application functionality
"""


import os

#Root application path
APP_PATH = os.path.dirname(__file__)

#Templates(*.html.jinja files) path
TEMPLATES_PATH = os.path.join(APP_PATH, 'templates')

#Static files path (css, js, image files)
STATIC_PATH = os.path.join(APP_PATH, 'static')

#Thumbnails path
THUMBNAILS_FOLDER = os.path.join(STATIC_PATH, 'thumbnails')

#Path to processed images
RESULT_FOLDER = os.path.join(STATIC_PATH, 'result')

#list of allowed extensions for upload
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}