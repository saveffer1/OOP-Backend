# ===============================================================================#
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional
from enum import Enum
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
#===============================================================================#
### src classes
from src.account import User, Admin
from src.image import Image
#===============================================================================#

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def main():
    print("complete!")