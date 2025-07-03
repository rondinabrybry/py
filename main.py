from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from datetime import datetime

app = FastAPI()

@app.get('/')
def welcome():
    return {'message': 'Hey'}

class Song(BaseModel):
    id: int
    title: str
    length: int
    date_released: datetime
    price: float
    
    
songs = []

@app.get("/songs", response_model=List[Song])
async def read_songs():
    return songs

@app.post("/songs", response_model=Song)
async def create_song(song: Song):
    songs.append(song)
    return song

@app.put("/songs/{song_id}", response_model=Song)
async def update_song(song_id: int, song: Song):
    songs[song_id] = song
    return song

@app.delete("/songs/{song_id}")
async def delete_song(song_id: int):
    del songs[song_id]
    return {"message": "Song deleted"}
    
    
# sorry i only know the basics