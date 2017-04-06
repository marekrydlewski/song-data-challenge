from itertools import islice
from datetime import datetime
from pprint import pprint
from timeit import default_timer as timer


class Artist:
    max_id = 0
    def __init__(self, name):
        Artist.max_id += 1
        self.name = name
        self.idk = Artist.max_id


class Listening:
    def __init__(self, song_id=None , user_id=None, artist_id=None, date_id=None, time_id=None):
        self.song_id = song_id
        self.user_id = user_id
        self.artist_id = artist_id
        self.date_id = date_id
        self.time_id = time_id


class User:
    def __init__(self, idk):
        self.idk = idk


class Song:
    def __init__(self, title, song_id, performance_id):
        self.title = title
        self.song_id = song_id
        self.performance_ids = list(performance_id)

    def is_performance(self, performance_id):
        return performance_id in self.performance_ids

    def add_performance(self, performance_id):
        self.performance_ids.append(performance_id)


class Date:
    def __init__(self, t_stamp):
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
    def __init__(self, t_stamp):
        date = datetime.fromtimestamp(t_stamp)
        self.hour = date.hour
        self.minute = date.minute
        self.idk = self.hour * 24 + self.minute

def show_file(file_name, n=10):
    with open(file_name) as infile:
        head = list(islice(infile, n))
    print(*[h.strip().split("<SEP>") for h in head], sep='\n')


def process_tracks(file_name):
    with open(file_name) as infile:
        for line in islice(infile):
            line_sep = line.strip().split("<SEP>")
            performance, song, artist, title = line_sep

            # datetime.fromtimestamp(number_date)


def get_number_of_lines(file_name):
    with open(file_name, encoding="latin-1") as infile:
        lines =  sum(1 for line in infile)
    return lines

if __name__ == "__main__":
    tracks = "data\\unique_tracks.txt"
    triplets = "data\\triplets_sample_20p.txt"

    artists = {}
    artists_set = set()
    songs = {}
    users = {}
    dates = {}
    times = {}
    listenings = []

    show_file(tracks)
    show_file(triplets)
    # print(get_number_of_lines(tracks))
    # print(get_number_of_lines(triplets))

    start = timer()

    with open(tracks, encoding="latin-1") as infile:
        for line in (infile):
            performance_idk, song_idk, artist, title = line.strip().split("<SEP>")

            if not artist in artists:
                artists[artist] = Artist(artist)
                artists_set.add(Artist.max_id)
            if not song_idk in songs:
                songs[song_idk] = Song(title, song_idk, performance_idk)
            else:
                if songs[song_idk].is_performance(performance_idk):
                    songs[song_idk].add_performance(performance_idk)

    with open(triplets, encoding="latin-1") as infile:
        for line in islice(infile, 10000):
            user_id, song_id, date = line.strip().split("<SEP>")
            date_parsed = Date(int(date))
            time_parsed = Time(int(date))

            if not date_parsed in dates:
                dates[date_parsed.idk] = date_parsed
            if not time_parsed in times:
                times[time_parsed.idk] = time_parsed
            if not user_id in users:
                users[user_id] = User(user_id)

            listening = Listening()
            listening.song_id = song_id
            listening.user_id = user_id
            listening.date_id = date_parsed.idk
            listening.time_id = time_parsed.idk
            listenings.append(listening)

    end = timer()
    print(end - start)
    #pprint(artists)
    #pprint(songs)

