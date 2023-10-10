import threading
import requests
import bs4
import lyricsgenius as genius
import yt_dlp as youtube_dl
import os
import subprocess
import discord


class MusicManager:
    def __init__(self, genius_token):
        self.genius = genius.Genius(genius_token)
        self.songs_path = "songs/"
        self.queue = []
        self.is_playing = False
        self.voice_client = None
        self.current_song = None

        # new thread for playing music
        self.play_thread = threading.Thread(target=self.play_loop, args=())
        self.play_thread.daemon = True
        self.play_thread.start()

    def get_song(self, song_name, artist_name):
        '''
        Returns the path to the song folder if song can be found, else returns None.

        Returns the path to the song if it exists in the songs folder. If it does not exist, it will download the song and return the path to the song.

        Both the song and the lyrics will be downloaded.
        '''
        song = self.genius.search_song(song_name, artist_name)
        
        if song is None:
            print('Could not find song')
            return None
        
        # make path for song 
        song_directory = f'{song_name} - {artist_name}'

        # if song exists in downloaded songs, return path to song
        downloaded_songs = os.listdir(self.songs_path)
        for file in downloaded_songs:
            if song_directory == file:
                print('Song already downloaded so returning existing path')
                return os.path.join(self.songs_path, file)
            
        
        # make directory for song
        song_path = os.path.join(self.songs_path, song_directory)
        os.mkdir(song_path)

        # get lyrics and save to lyrics.txt
        lyrics = song.lyrics
        lyrics_path = f'{song_path}/lyrics.txt'
        with open(lyrics_path, 'w') as f:
            print('Saving lyrics to lyrics.txt')
            f.write(lyrics)


        # download song
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': f'{song_path}/audio/{song_name} - {artist_name}.%(ext)s',  # output file name
        }

        search_query = f'{song_name} {artist_name} audio'
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            # search query (which is not a url)
            ydl.download([f"ytsearch:{search_query}"])
        
        return song_path
    
    def play_loop(self):
        '''
        Plays the song in the queue.
        '''
        while True:
            if self.is_playing:
                print('is_playing is true')
                continue

            if len(self.queue) > 0:
                song_path = self.queue.pop(0)
                self.play_song(song_path, self.voice_client)
            else:
                self.is_playing = False
                continue
                
    
    def play_song(self, song_path):
        '''
        Plays the song at the given path.
        '''
        print('staring play_song function for ' + song_path)
        self.is_playing = True

        # song path is the path to the song folder in the audio folder, it is the only folder in the audio folder
        audio_path = os.path.join(song_path, 'audio', os.listdir(os.path.join(song_path, 'audio'))[0])

        print(f"Playing {audio_path}")

        # play song
        source = discord.FFmpegPCMAudio(audio_path)
        self.voice_client.play(source, after=lambda e: self.play_manager())
        self.voice_client.source = discord.PCMVolumeTransformer(self.voice_client.source)
        self.voice_client.source.volume = 0.07

        print('should be playing now')

    def queue_song(self, song_name, artist_name, voice_client):
        '''
        Adds the song at the given path to the queue.
        '''
        self.voice_client = voice_client
        song_path = self.get_song(song_name, artist_name)

        self.queue.append(song_path)

        return song_path


    
            

            
        
        



def main():
    music_manager = MusicManager()

    music_manager.get_song('18', 'One Direction')
