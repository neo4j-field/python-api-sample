"""Application main file."""
from typing import List

from fastapi import FastAPI, HTTPException
from neomodel import DoesNotExist

from .database_models import Artist, Song, Playlist
from .api_models import (
    AlbumAPI, ArtistAPI, PlaylistAPI, SongAPI, PlaylistInput, RootAPI
)


# Create app
app = FastAPI(title="neomodel sample project")


@app.get("/")
async def root() -> RootAPI:
    return RootAPI(song_count=len(Song.nodes))


@app.get("/artists")
async def get_artists(
    page_size: int = 10,
    page_number: int = 0
) -> List[ArtistAPI]:
    from_ = page_number * page_size
    to = from_ + page_size
    artists = Artist.nodes.order_by("name")[from_:to]
    return [
        ArtistAPI(
            uid=a.uid,
            name=a.name,
            songs=[
                SongAPI(
                    uid=s.uid,
                    title=s.title,
                    popularity=s.popularity,
                    loudness=s.loudness,
                    liveness=s.liveness,
                    tempo=s.tempo,
                    valence=s.valence,
                    instrumentalness=s.instrumentalness,
                    danceability=s.danceability,
                    speechiness=s.speechiness,
                    duration=s.duration,
                    mode=s.mode,
                    acousticness=s.acousticness,
                    key=s.key,
                    energy=s.energy,
                )
                for s in a.songs.all()
            ],
        )
        for a in artists
    ]


@app.get("/songs")
async def get_song(song_uid: str) -> SongAPI:
    song = Song.nodes.get(uid=song_uid)
    return SongAPI(
        uid=song.uid,
        title=song.title,
        loudness=song.loudness,
        liveness=song.liveness,
        tempo=song.tempo,
        valence=song.valence,
        instrumentalness=song.instrumentalness,
        danceability=song.danceability,
        speechiness=song.speechiness,
        duration=song.duration,
        mode=song.mode,
        popularity=song.popularity,
        acousticness=song.acousticness,
        key=song.key,
        energy=song.energy,
        albums=[AlbumAPI(uid=a.uid) for a in song.albums.all()],
    )


@app.post("/playlists")
async def create_playlist(input: PlaylistInput) -> PlaylistAPI:
    try:
        playlist = Playlist(
            title=input.title,
        ).save()

        for _song in input.songs:
            song = Song.nodes.get(uid=_song)
            playlist.songs.connect(song)

    except DoesNotExist as exc:
        raise HTTPException(status_code=500, detail="Item not found") from exc
    return PlaylistAPI(
        uid=playlist.uid,
        title=playlist.title,
        songs=[
            SongAPI(uid=s.uid, title=s.title, popularity=s.popularity)
            for s in playlist.songs.all()
        ],
    )
