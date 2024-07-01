"""
Classes for representing music data, from the API point of view.

It provides both classes as returned by the API, and also Input classes for creating objects.

Classes:
- RootAPI: Represents the data returned by the root endpoint.
- AlbumAPI: Represents an album in the music database.
- SongAPI: Represents a song in the music database.
- ArtistAPI: Represents an artist in the music database.
- PlaylistAPI: Represents a playlist in the music database.
- PlaylistInput: Input to provide in a POST request to create a playlist.

"""
from typing import List, Optional
from pydantic import BaseModel, Field


class RootAPI(BaseModel):
    song_count: int = Field(..., alias="# of songs")


class AlbumAPI(BaseModel):
    uid: str


class SongAPI(BaseModel):
    uid: str
    title: str
    loudness: float
    liveness: float
    tempo: float
    valence: float
    instrumentalness: float
    danceability: float
    speechiness: float
    duration: int
    mode: bool
    popularity: int
    acousticness: float
    key: int
    energy: float

    albums: Optional[List[AlbumAPI]] = None


class ArtistAPI(BaseModel):
    uid: str
    name: str
    songs: Optional[List[SongAPI]]


class PlaylistAPI(BaseModel):
    uid: str
    title: str
    songs: Optional[List[SongAPI]]


class PlaylistInput(BaseModel):
    title: str
    songs: List[str]
