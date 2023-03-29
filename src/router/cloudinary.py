import os
import cloudinary
from cloudinary.utils import cloudinary_url
from cloudinary.uploader import upload as cloudinary_upload
from cloudinary.uploader import destroy as cloudinary_destroy

import configparser
config = configparser.ConfigParser()
config.read("./config.ini")

cloudinary.config(
    cloud_name = config["cloudinary"]["cloud_name"],
    api_key = config["cloudinary"]["api_key"],
    api_secret = config["cloudinary"]["api_secret"],
    secure=True
)