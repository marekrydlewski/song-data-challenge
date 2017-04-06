from itertools import islice
from datetime import datetime


class Artist:
    def __init__(self, name, idk):
        self.name = name
        self.idk = idk
        self.songs_ids = []


class Listening:
    def __init__(self, idk_song, idk_user, idk_artist, idk_date, idk_time):
        self.idk_song = idk_song
        self.idk_user = idk_user
        self.idk_artist = idk_artist
        self.idk_date = idk_date
        self.idk_time = idk_time


class User:
    def __init__(self, name, idk):
        self.idk = idk
        self.name = name


class Song:
    def __init__(self, title, idk_song, idk_performance):
        self.title = title
        self.idk_song = idk_song
        self.idk_performance = idk_performance


class Date:
    def __init(self, t_stamp):
        date = datetime.fromtimestamp(t_stamp)
        self.year = date.year
        self.month = date.month
        self.day = date.day
        # produce unique key:
        idk = self.year * 100
        idk += self.month
        idk *= 100
        idk += self.day
        self.idk = idk


class Time:
    def __init(self, t_stamp):
        date = datetime.fromtimestamp(t_stamp)
        self.hour = date.hour
        self.minute = date.minute
        self.idk = self.hour * 24 + self.minute

def show_file(file_name, n=10):
    with open(file_name) as infile:
        head = list(islice(infile, n))
    print(*[h.strip().split("<SEP>") for h in head], sep='\n')


def process_file(file_name):
    with open(file_name) as infile:
        for line in islice(infile):
            line_sep = line.strip().split("<SEP>")
            # datetime.fromtimestamp(number_date)


if __name__ == "__main__":
    tracks = "data\\unique_tracks.txt"
    triplets = "data\\triplets_sample_20p.txt"

    show_file(tracks)
    show_file(triplets)
