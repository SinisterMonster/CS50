import requests
import csv



def main():
        
    spotifyCSV = 'spotify.csv'

    # Call function to get search terms from Spotify playlist
    songDetails = spotify_playlist_reader(spotifyCSV)

    print(songDetails)

    # Call the function to get corresponding Apple Song ID
    #appleSongID = retrieve_apple_songID(songDetails)

    #print(searchTermList)




def spotify_playlist_reader(spotifyCSV):

    # Open the Spotify file obtained from places like https://exportify.app/
    with open(spotifyCSV, encoding='utf-8') as spotifyPlaylist:
        spotifyPlaylist = csv.reader(spotifyPlaylist)
        # Avoid table heading
        next(spotifyPlaylist)

        songDetails = []

        for song in spotifyPlaylist:

            #Extract relevant data
            title, artist, releaseDate = song[1], song[3].split(','), song[8].split('-')
            artist = artist[0]
            releaseYear = releaseDate[0]

            # Create  search term
            songDetails = {
                "title": title,
                "artist": artist,
                "releaseYear": releaseYear
            }

    return songDetails


'''def retrieve_apple_songID(songDetails):
    
    # GET request
    searchTerm = songDetails["title"] + " " + songDetails["artist"] + " " + songDetails["releaseYear"]
    url = f'https://itunes.apple.com/search?term={searchTerm}&entity=song&limit=1' 
    response = requests.get(url) 
    response = response.json()

    # Check for response
    try: 
        songID = [response["results"][0]["trackId"]]
        print(f"Found match for: {songDetails["title"]}")
        
        # Once found, update a log
        with open('temp.csv', 'a', encoding='utf-8') as output_file:
            output_file.write(str(data))

    except:
        print(f"No songs matching a search for {songDetails["title"]} was found")
        return None

'''
main()