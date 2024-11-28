import csv
import urllib.parse, urllib.request
import json
import iGetMusic as iGetcode 

itunes_identifiers = []

def retrieve_itunes_identifier(title, artist, releaseYear):
    headers = {
        "X-Apple-Store-Front" : "143446-10,32 ab:rSwnYxS0 t:music2",
        "X-Apple-Tz" : "7200" 
    }
    # This is adds a space between the data so that URL can be qouted properly 
    term = title + " " + artist + " " + releaseYear
    url = "https://itunes.apple.com/WebObjects/MZStore.woa/wa/search?clientApplication=MusicPlayer&term=" + urllib.parse.quote(term) 
    request = urllib.request.Request(url, None, headers)
    try:
        response = urllib.request.urlopen(request)
        data = json.loads(response.read().decode('utf-8'))
        songs = [result for result in data["storePlatformData"]["lockup"]["results"].values() if result["kind"] == "song"]
        #songs = [result for result in data["storePlatformData"]["lockup"]["results"].values()]

        with open('temp.csv', 'a', encoding='utf-8') as output_file:
            output_file.write(str(data))
        
        # Attempt to match by title & artist
        for song in songs: 
            with open('op.csv', 'w', encoding='utf-8') as output_file:
                if song["name"].lower() == title.lower():
                    if (artist.lower() in song["artistName"].lower()): 
                        output_file.write(str(song) + "\n")
                        return song["id"]
                    elif releaseDate in song["releaseDate"]:
                        print(f" {releaseDate} ---- {song["releaseDate"]}")
                        return song["id"]


    except:
        # We don't do any fancy error handling.. Just return None if something went wrong
        return None



with open('spotify.csv', encoding='utf-8') as playlist_file:
    playlist_reader = csv.reader(playlist_file)
    next(playlist_reader)

    for row in playlist_reader:
        title, artist, releaseDate = row[1], row[3].split(','), row[8].split('-')
        artist = artist[0]
        releaseYear = releaseDate[0]
        print(f" {title} ---- {artist}")
        itunes_identifier = retrieve_itunes_identifier(title, artist, releaseYear)

        if itunes_identifier:
            itunes_identifiers.append(itunes_identifier)
            #print("{} - {} => {}".format(title, artist, itunes_identifier))
        else:
            #print("{} - {} => Not Found".format(title, artist))
            noresult = "{} - {} => Not Found".format(title, artist)
            with open('noresult.txt', 'a+') as f:
                f.write(noresult)
                f.write('\n')


with open('itunes.csv', 'w', encoding='utf-8') as output_file:
    for itunes_identifier in itunes_identifiers:
        output_file.write(str(itunes_identifier) + "\n")


# Developped by @therealmarius on GitHub
# Based on the work of @simonschellaert on GitHub
# Github project page: https://github.com/therealmarius/Spotify-2-AppleMusic
# Ignoring feats
''' or dateOfRelease in song[""]'''