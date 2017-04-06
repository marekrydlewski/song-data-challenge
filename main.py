from itertools import islice
from collections import Counter
from datetime import datetime
from pprint import pprint
import sys
from timeit import default_timer as timer


class Artist:
    max_id = 0

    def __init__(self, name):
        Artist.max_id += 1
        self.name = name
        self.idk = Artist.max_id


class Listening:
    def __init__(self, song_id=None, user_id=None, artist_id=None, date_id=None, time_id=None):
        self.song_id = song_id
        self.user_id = user_id
        self.artist_id = artist_id
        self.date_id = date_id
        self.time_id = time_id

    def __str__(self):
        return "{0}, {1}, {2}, {3}, {4}\n".format(self.song_id, self.user_id, self.artist_id, self.date_id,
                                                  self.time_id)


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


def show_file(file_name, n=3):
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
        lines = sum(1 for _ in infile)
    return lines


def get_most_popular_songs(listenings, songs):
    cnt = Counter()
    for l in listenings:
        cnt[l.song_id] += 1
    return [(songs[c[0]].title, c[1]) for c in cnt.most_common(10)]


def get_most_popular_artists(listenings, artists):
    cnt = Counter()
    for l in listenings:
        cnt[l.artist_id] += 1
    return [(artists[c[0]].name, c[1]) for c in cnt.most_common(10)]


def get_month_distribution(listenings, dates):
    cnt = Counter()
    for l in listenings:
        my_date = dates[l.date_id]
        cnt[my_date.month] += 1
    return sorted(cnt.items())


def get_user_ranking(listenings):
    user_songs = {}
    for l in listenings:
        if l.user_id in user_songs:
            user_songs[l.user_id].add(l.song_id)
        else:
            user_songs[l.user_id] = set()
    cnt = Counter()
    for k, val in user_songs.items():
        cnt[k] = len(val)
    return cnt.most_common(10)


def get_queen_users(listenings, artists):
    queen_id = artists["Queen"].idk
    queen_users = {}
    cnt = Counter()
    for l in listenings:
        if l.artist_id == queen_id:
            cnt[l.song_id] += 1
            if l.song_id in queen_users:
                queen_users[l.song_id].add(l.user_id)
            else:
                queen_users[l.song_id] = set()

    most_popular = [c[0] for c in cnt.most_common(3)]
    users_sets = [queen_users[mp] for mp in most_popular]
    return list(users_sets[0].intersection(users_sets[1]).intersection(users_sets[2]))[:10]


if __name__ == "__main__":
    tracks = "data\\unique_tracks.txt"
    triplets = "data\\triplets_sample_20p.txt"

    artists = {}
    artists_id_to_artist = {}
    artists_of_songs = {}
    songs = {}
    users = {}
    dates = {}
    times = {}
    listenings = []

    show_file(tracks)
    show_file(triplets)
    print()

    # print(get_number_of_lines(tracks))
    # print(get_number_of_lines(triplets))

    start = timer()

    with open(tracks, encoding="latin-1") as infile:
        for line in (infile):
            performance_idk, song_idk, artist, title = line.strip().split("<SEP>")
            if artist not in artists:
                new_artist = Artist(artist)
                artists[artist] = new_artist
                artists_id_to_artist[new_artist.idk] = new_artist

            artists_of_songs[song_idk] = artists[artist].idk
            if song_idk not in songs:
                songs[song_idk] = Song(title, song_idk, performance_idk)
            else:
                if songs[song_idk].is_performance(performance_idk):
                    songs[song_idk].add_performance(performance_idk)

    with open(triplets, encoding="latin-1") as infile:
        for line in infile:
            user_id, song_id, date = line.strip().split("<SEP>")
            date_parsed = Date(int(date))
            time_parsed = Time(int(date))

            if date_parsed not in dates:
                dates[date_parsed.idk] = date_parsed
            if time_parsed not in times:
                times[time_parsed.idk] = time_parsed
            if user_id not in users:
                users[user_id] = User(user_id)

            listening = Listening()
            listening.song_id = song_id
            listening.user_id = user_id
            listening.date_id = date_parsed.idk
            listening.time_id = time_parsed.idk
            listening.artist_id = artists_of_songs[song_id]
            listenings.append(listening)

    end = timer()
    print(end - start)

    print("sizes:")
    print(sys.getsizeof(listenings))
    print(sys.getsizeof(artists))
    print(sys.getsizeof(artists_id_to_artist))
    print(sys.getsizeof(songs))
    print(sys.getsizeof(users))
    print(sys.getsizeof(dates))
    print(sys.getsizeof(times))

    print()
    print("tasks:")

    start = timer()
    most_popular_songs = get_most_popular_songs(listenings, songs)
    end = timer()
    print(*most_popular_songs, sep="\n")
    print(end - start)
    print()

    start = timer()
    most_popular_artists = get_most_popular_artists(listenings, artists_id_to_artist)
    end = timer()
    print(*most_popular_artists, sep="\n")
    print(end - start)
    print()

    start = timer()
    months_counted = get_month_distribution(listenings, dates)
    end = timer()
    print(*months_counted, sep="\n")
    print(end - start)
    print()

    start = timer()
    user_ranking = get_user_ranking(listenings)
    end = timer()
    print(*user_ranking, sep="\n")
    print(end - start)
    print()

    start = timer()
    queens = get_queen_users(listenings, artists)
    end = timer()
    print(*queens, sep="\n")
    print(end - start)
    print()
