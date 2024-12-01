import requests
import csv
import time
import pyautogui
import pandas
import easygui

def main():
        
    spotifyCSV = 'spotify.csv'

    # Call function to get list of search terms from Spotify playlist
    songsList = spotify_playlist_reader(spotifyCSV)

    # Call the function to get corresponding Apple Song ID
    appleSongIDList = retrieve_apple_songID(songsList)

    # Call function to get Firrefox coordinates
    coordinates = get_firefox_coordinates()

# Function that reads Spotify playlist and returns song list
def spotify_playlist_reader(spotifyCSV):

    # Open the Spotify file obtained from https://exportify.app/
    with open(spotifyCSV, encoding='utf-8') as spotifyPlaylist:
        spotifyPlaylist = csv.reader(spotifyPlaylist)
        # Avoid table heading
        next(spotifyPlaylist)

        songsList = list()

        for song in spotifyPlaylist:

            # Extract relevant data
            title, artist, releaseDate = song[1], song[3].split(','), song[8].split('-')
            artist = artist[0]
            releaseYear = releaseDate[0]

            # Create  search term
            songInfo = {
                "title": title,
                "artist": artist,
                "releaseYear": releaseYear
            }
            songsList.append(songInfo)
            

    return songsList

# Function that Spotify song list and returns Apple Song ID
def retrieve_apple_songID(songsList):

    numberofSongs = len(songsList)
    songID = []

    # Open file to write Apple Song ID once found, write fields
    with open('AppleSongID.csv', 'w', encoding='utf-8') as AppleSongID_file:
        fields =["AppleSongID", "title", "artist", "releaseYear"]
        csvwriter = csv.writer(AppleSongID_file)
        csvwriter.writerow(fields)

        for i in range(numberofSongs):    
            # GET request
            searchTerm = songsList[i]["title"] + " " + songsList[i]["artist"] + " " + songsList[i]["releaseYear"]

            url = f'https://itunes.apple.com/search?term={searchTerm}&entity=song&limit=1' 
            response = requests.get(url) 
            response = response.json()
          
            # Check for match
            try: 
                songID = [response["results"][0]["trackId"]]
                writeSongString = str(songID[0])  + "," +  songsList[i]["title"] + "," + songsList[i]["artist"] + "," + songsList[i]["releaseYear"]
           
                print(f"Found match for: {songsList[i]["title"]}")
                
               # Once found, update a log with Apple Music songID
                AppleSongID_file.write(writeSongString)
                AppleSongID_file.write("\n")

            except:
                #print no match found message
                print(f"No songs matching a search for {songsList[i]["title"]} was found. Log updated")
                
                # Create and update a log of the songs not found
                with open('NoMatchFound.csv', 'a', encoding='utf-8') as NoMatchFound_file:
                                   # Once found, update a log with Apple Music songID
                    NoMatchFound_file.write(str(searchTerm))
                    NoMatchFound_file.write("\n")

    # Once all the recognition is done, read the IDs from CSV and return
    with open('AppleSongID.csv', mode ='r') as file:
        df = pandas.read_csv(file)
        appleSongIDList = df.AppleSongID
    return appleSongIDList

# Function to get browser coordinates from user
def get_firefox_coordinates():
    print ('Before coninuing:\nFollow steps in Instructions.txt to get coordinates of the POST request body and SEND button')
    
    # Get those coordinates from user
msg = "Enter your personal information"
title = "Credit Card Application"
fieldNames = ["Name","Street Address","City","State","ZipCode"]
fieldValues = []  # we start with blanks for the values
fieldValues = multenterbox(msg,title, fieldNames)

# make sure that none of the fields was left blank


# Function that that takes AM songID and adds them to AM playlist
def write_songs_to_apple_music(appleSongIDList):

    return None





main()