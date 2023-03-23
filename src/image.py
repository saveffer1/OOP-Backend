import ntpath
import cloudinary
from cloudinary.utils import cloudinary_url
from cloudinary.uploader import upload as cloudinary_upload
from abc import ABC, abstractmethod
from dataclasses import dataclass
import configparser
config = configparser.ConfigParser()
config.read("./src/assets/config.ini")

cloudinary.config(
    cloud_name = config["cloudinary"]["cloud_name"],
    api_key = config["cloudinary"]["api_key"],
    api_secret = config["cloudinary"]["api_secret"],
    secure=True
)

@dataclass
class Image():
    name : str
    width : int
    high : int
    
    def upload_image(self) -> str:
        cloudinary_upload(self.name, public_id=str(ntpath.basename(self.name)).split('.')[0])
        url, options = cloudinary_url(
            str(ntpath.basename(self.name)).split('.')[0], width=self.width, height=self.high, crop="fill")
        return f"https://res.cloudinary.com/{config['cloudinary']['cloud_name']}/image/upload/{ntpath.basename(self.name)}"

    def __str__(self) -> str:
        return f"Image({self.name}, {str(ntpath.basename(self.name)).split('.')[0]}, {self.width}, {self.high})"
