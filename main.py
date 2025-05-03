from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List, Literal
from datetime import datetime
import random

app = FastAPI()

class GeoJSONPoint(BaseModel):
    type: Literal["Point"]
    coordinates: List[float] = Field(..., min_items=2, max_items=2)

class SongEntry(BaseModel):
    song: str
    genre: str
    country: str
    timestamp: datetime

songs_by_genre = {
    "Reggaeton": ["Despacito", "Baila Baila", "Dákiti"],
    "Pop": ["Blinding Lights", "Levitating", "As It Was"],
    "Rock": ["Bohemian Rhapsody", "Smells Like Teen Spirit", "Enter Sandman"],
    "Electrónica": ["Titanium", "One More Time", "Levels"],
    "Cumbia": ["La Cumbia de los Trapos", "Nunca Es Suficiente", "Yo Tomo"]}


@app.get("/songs", response_model=List[SongEntry])
def get_songs(countries= {"Argentina", "France", "Spain", "Mexico"}):
    now = datetime.utcnow()
    result = []

    for country in countries:

        genre = random.choice(list(songs_by_genre.keys()))
        song = random.choice(songs_by_genre[genre])

        result.append(SongEntry(
            song=song,
            genre=genre,
            country=country,
            timestamp=now
        ))

    return result

if __name__ == "__main__":
    songs = get_songs()
    for song in songs:
        print(song)