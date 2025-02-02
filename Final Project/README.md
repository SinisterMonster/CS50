# SPOTIFY TO APPLE MUSIC TRANSFER TOOL
## LINKS
#### Video Project Introduction: https://youtu.be/KPafML5UjuA
#### Video Demo Part 1 - Finding coordinates of POST and SEND:  https://youtu.be/dklv2hH9PsA
#### Video Demo Part 2 - Project in action:  https://youtu.be/GxLMj8egJDA

## DESCRIPTION
#### Problem Description:

- Wanted to move from Spotify to Apple Music due to recent multiple cost increase
- Most available transfer tools for this purpose are either paid or require an yearly subscription to Apple's Developer program which gives you access to their Music API to make this project easier. 
- None of these were good options for me

#### Project Pre-requisites:
- This project requires the following Python libraries to run:
~~~
requests
csv
time
pyautogui
pandas
easygui
~~~

- And a browser. I used Mozilla Firefox. Other browsers will work too but will require some minor adjustments


#### Project Description:

This Project was broken down into the following major sections to make managing this easier:

##### Extract playlist information from Spotify
This part was very easy. I used tools avaible online for free such as https://exportify.app/. Tools such as this read your playlist and produce a .csv file that you can download.

##### Create a search keyphrase
The downloaded csv file is opened using a GUI to load into the program. This is handled by a very simple function using the *easygui* library with just one line:

~~~
spotifyCSV= fileopenbox(msg="Choose your Spotify playlist csv")
~~~

The filename from the above function is handed over to *spotify_playlist_reader* which is supposed to produce a keyphrase for each song in the playlist which is used in the next step:

~~~
songsList = spotify_playlist_reader(spotifyCSV)
~~~


##### Obtain Apple SongID
The searrch keyphrase from *spotify_playlist_reader* is handed to *retrieve_apple_songID* via a call to that function:
~~~
[appleSongIDList, appleSongTitleList] = retrieve_apple_songID(songsList)
~~~

This function is designed to use to *requests* library to obtain a response from  iTunes which contains quite a lot of data, most of which is cleaned off since its not too relevant. The SongID is what what we are after in all this. Some broad strokes error checking is also done because during testing certain songs with special characterrs in their names didnt yield a favourable result. The gist of the code looks like this: 

~~~
searchTerm = songsList[i]["title"] + " " + songsList[i]["artist"] + " " + songsList[i]["releaseYear"]

url = f'https://itunes.apple.com/search?term={searchTerm}&entity=song&limit=1' 
response = requests.get(url) 

~~~

If a response is obtained and a song match is found, the code then updates a csv log (*AppleSongID.csv*) as follows and prints a message for the user:
~~~
songID = [response["results"][0]["trackId"]]
writeSongString = str(songID[0])  + "," +  songsList[i]["title"] + "," + songsList[i]["artist"] + "," + songsList[i]["releaseYear"]

print(f"Found match for: {songsList[i]['title']}")

# Once found, update a log with Apple Music songID
AppleSongID_file.write(writeSongString)
AppleSongID_file.write("\n")
~~~

If a response is obtained and a song match is NOT found, the code then updates another csv log (*NoMatchFound.csv*) as follows and also updates the user as follows:
~~~
#print no match found message
print(f"No songs matching a search for {songsList[i]['title']} was found. Log updated")

# Create and update a log of the songs not found
with open('NoMatchFound.csv', 'a', encoding='utf-8') as NoMatchFound_file:
                    # Once found, update a log with Apple Music songID
    NoMatchFound_file.write(str(searchTerm))
    NoMatchFound_file.write("\n")
~~~
This log is particularly useful to later manually add hard to find songs.

This function then returns:
~~~
return appleSongIDList, appleSongTitleList
~~~

##### Obtain browser PUSH and SEND coordinates
You obtain the coordinates as shown in the *Video Demo Part 1*. This section is run using Windows Terminal. Steps are as follows:

1. Create an empty playlist in AM
2. Open browsers developer tools and go to **Networks** tab
3. Add a random song to the mepty playlist. You will notice the incrreased activity in the **Networks** tab
4. Find a POST request starting with https://amp-api.music.apple.com/v1/me/library/playlists/. This is what the brrowser sent to add that song. See image below:

![alt text](<Screenshot 2024-12-01 171959.png>)

5. Right click on this POST request -> **Edit and Resend**
6. Scroll down to the very end of the section that opened. You should see a request similar to the one in the image below. The *id* will be different. But this number is what uniqlely identifies a song in Apple Music (*SongID*). The coordinates of the locations we want is highlighted in red.

![alt text](image.png)

7. Open a python terminal and run `import pyautogui`to import it. This is used to obtain coordinates on the screen.
8. With the Terminal still selected hover mouse over the *id* and run `pyautogui.position()`
9. With the Terminal still selected hover mouse over the *Send* button and run `pyautogui.position()`
10. These are the coordinates for the songID for the POST request and the Send button to send that request respectively.


##### Submit PUSH requests to Apple Music to add songs
This function brings everything togther. It takes the coordinates of the browser window and sends clicks to the *SongID* section, replaces it with the *SongID* we obtained via lookup and then clicks the *Send* button

~~~
for i in range(len(appleSongIDList)):
    print(f"\nAdding {appleSongTitleList[i]}...")
    
    # Add songs by sending POST requests
    pyautogui.doubleClick(int(coordinates[0]), int(coordinates[1]))
    pyautogui.typewrite(str(appleSongIDList[i]))
    pyautogui.click(int(coordinates[2]), int(coordinates[3]))
    time.sleep(2)
~~~

## LIMITATIONS
The following are some of the limitations I identified during testing and its mostly centered around detection of SongID's. 
- Song discovery algorithm isnt perfect. During testing it only detected 50-60% of songs
- If the name of the song has special characters, especially commas, it doesnt work. This is because I use cvs for logging- This is a future improvement action for me
- Some songs dont have an exact match and I havent figured out how to handle them yet

## DISCLAIMER
I dont think anyone will use this unpolished tool I made for myself and a friend but please test it on a smaller scale before you get 100 Katy Perry's Chained to the Rhythm in one playlist (this may or may not have happened to me). I take no responsibility for the damage this causes to your song collection but feedback on how to improve this is most welcome :)