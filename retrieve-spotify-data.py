"""import relevant modules for spotify API"""
import spotipy
import requests
import time
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
"""for arduino/python connection"""
import serial
from pprint import pprint
"""other modules"""
import random

"""needs to be updated every hour via spotify api link"""
access_token_stat = "BQCwIqVSAg3fDPnO0IessgG3ed4BLJVjYqJm7gkop0jvaSW7X32qN-lWRKi45_iJFtyzMtjjk-FNBQG7r24Mw4b3nS_ntsrjbIDWoNkSHaUVttHdD9uCp-451QBSBchp7ZC-5OTKw7k08As1ThFHjhNrgCzvS_puIunS09j1sAA"
access_token_curr ="BQCIJRuLUM4wPhOiq9QTJAgq7fyriBtqrcgBm7HbizKdC3eLoWvs3b06BbwFgtd2dPTUTYubY3kYnLhKL9UiTr8JL9b3UDya7CApyDtPNs7y8QPhms_sVJVZfD2s6jUjPCGOlTui4hlr9O9-CXknwmsrMm6kSbywGTGn7GHj7-o"

"""checks whether or not there is a song currently playing on Spotify. Returns 1 (if playing) and 0 otherwise."""
def get_status():
    """authentification information """
    cid = 'f6fa391f2de840d187f61094f3dff6ba'
    secret = 'd675c8269a814a3c9d0d3d7c72ed4be7'

    URL_CHECK_STATUS = "https://api.spotify.com/v1/me/player"

    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    connection = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    response = requests.get(
        URL_CHECK_STATUS,
            headers={
                "Authorization": f"Bearer {access_token_stat}"
            }
    )
    json_response = response.json()
    status = json_response["is_playing"]

    if status == True:
        return 1
    return 0


"""fetches for json response of from API"""
def get_response():
    """authentification information """
    USERNAME = 'kyosuke912'
    CLIENT_ID = 'f6fa391f2de840d187f61094f3dff6ba'
    CLIENT_SECRET = 'd675c8269a814a3c9d0d3d7c72ed4be7'
    SCOPE = 'user-read-currently-playing'

    auth_manager = SpotifyOAuth(
        scope=SCOPE,
        username=USERNAME,
        redirect_uri='http://localhost:8080',
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET)
    """currently playing track URL """
    URL_CURR_PLAYING = "https://api.spotify.com/v1/me/player/currently-playing"

    """establish connection"""
    client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    connection = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


    response = requests.get(
        URL_CURR_PLAYING,
            headers={
                "Authorization": f"Bearer {access_token_curr}"
            }
    )
    spotify = spotipy.Spotify(auth_manager=auth_manager)

    """error: check if json response is in correct format
        e.g. if music not playing, will be caught as JSONDecodeError """
    try:
        json_response = response.json()
        return json_response, connection
    except requests.exceptions.JSONDecodeError:
        print("Music not playing ")
        exit(1)


    return json_response, connection
    # return json_response, connection,　auth_manager, spotify
    #

"""returns name of track + all audio features retrievable """
def get_audio_features(json_response, connection):
    """parse basic song info """
    name = json_response["item"]["name"]
    uri = json_response["item"]["href"]
    audio_features = connection.audio_features(uri)[0]
    return audio_features, name

"""method to adjust the ranges of the audio features for convenience"""
def adjust_range(old_value, old_min, old_max, new_min, new_max):
    old_range = (old_max - old_min)
    new_value = 0
    if (old_range == 0):
        new_value = new_min
    else:
        new_range = (new_max - new_min)
        new_value = (((old_value - old_min) * new_range) / old_range) + new_min
    return int(new_value)


"""returns an appropriate assignment which is one of: high, medium, low
given an audio feature and range of each of the assignments"""
def ret_audio_feature_range(feature, low_start, mid_start, high_start):
    if feature in range (low_start, mid_start):
        return 0
    elif feature in range (mid_start, high_start):
        return 1
    elif (feature >= high_start):
        return 2
    else:
        print("value is not in the appropriate range")

# examine_key(1)

"""finds the most recurring value (high, mid, low) for every song, and returns it """
def find_most_recurring_val(list):
    count_map = {}
    for item in list:
        if item not in count_map:
            count_map[item] = 1
        else:
            count_map[item] += 1
    map_vals = count_map.values()
    return max(map_vals)

"""print function for debugging"""
def print_features(track_name,loudness_val,valence_val,dance_val,acousticness_val,tempo_val,energy_val):
        print("\n")
        print("track_name: ", track_name)
        print("loudness = ", loudness_val)
        print("valence = ", valence_val)
        print("danceability = ", dance_val)
        print("acousticness = ", acousticness_val)
        print("tempo = ", tempo_val)
        print("energy = ", energy_val)
        print("\n")

"""creates a list of relevant rooms to the currently playing song."""
def analyze_audio_features(json_response, connection):
    # json_response, connection = get_response()
    audio_features, track_name = get_audio_features(json_response, connection)

    """extract audio features """
    danceability = audio_features["danceability"]
    acousticness = audio_features["acousticness"]
    tempo = audio_features["tempo"]
    loudness = audio_features["loudness"]
    energy = audio_features["energy"]
    valence = audio_features["valence"]
    key = audio_features["key"]

    """change all relevant ranges to 0 to 100"""
    adjusted_danceability = adjust_range(danceability, 0, 1, 0, 100 )
    adjusted_loudness = adjust_range(loudness, -60, 0, 0, 100 ) #higher the louder scale(0, 100)
    adjusted_acousticness = adjust_range(acousticness, 0, 1, 0, 100)
    adjusted_valence= adjust_range(valence, 0, 1, 0, 100)
    adjusted_energy = adjust_range(energy, 0, 1, 0, 100 ) #higher the more energetic
    adjusted_tempo = tempo

    feature_values = [adjusted_danceability, adjusted_acousticness, adjusted_tempo, adjusted_loudness, adjusted_energy, adjusted_valence]
    high_low_list = []

    dance_val = ret_audio_feature_range(adjusted_danceability, 0, 63, 72)
    loudness_val = ret_audio_feature_range(adjusted_loudness, 0, 82, 86)
    tempo_val = ret_audio_feature_range(adjusted_acousticness, 0, 100, 121)
    acousticness_val = ret_audio_feature_range(adjusted_acousticness, 0, 30, 60)
    valence_val = ret_audio_feature_range(adjusted_valence, 0, 50,73)
    energy_val = ret_audio_feature_range(adjusted_energy, 0, 40, 70)

    # print_features(track_name,loudness_val,valence_val,dance_val,acousticness_val,tempo_val,energy_val)

    feature_values = [dance_val, loudness_val, tempo_val, acousticness_val, valence_val, energy_val]

    high = 2
    mid = 1
    low = 0

    disco_room = 6
    panic_room = 5
    jungle_room = 4
    sun_room = 2
    cloud_room = 3
    star_room =1
    ret_room_list = []

    if (energy_val == high and loudness_val ==high) or (find_most_recurring_val(feature_values) ==high) or ((energy_val == high or loudness_val ==high) and ((tempo_val == high  or acousticness_val == low) or (dance_val ==high))):
        ret_room_list.append(disco_room)
        # print("added disco_room")

    if (acousticness_val == (high or mid) and (tempo_val == (high or mid or low))) or (((loudness_val or energy_val)== (mid or low)) and valence == mid) or (find_most_recurring_val(feature_values) ==mid) or (dance_val ==low):
        ret_room_list.append(jungle_room)
        # print("added jungle_room")

    if((acousticness_val == (low or mid) and loudness_val == (low or mid) and valence_val == mid) or acousticness_val == high):
        ret_room_list.append(panic_room)
        # print("added panic_room")

    if (valence_val == (low or mid or high) and tempo_val == (low or mid)) or ((loudness_val == low or mid ) and tempo_val == (low or mid)) or (energy_val == mid and loudness_val == mid) or (acousticness_val == high and loudness_val ==high):
        ret_room_list.append(sun_room)
        # print("added sun_room")

    if(acousticness_val == (low or mid) and loudness_val == (low or mid) and valence_val == mid):
        ret_room_list.append(cloud_room)
        # print("added cloud_room")

    if ((valence_val == low) or ((loudness_val or energy_val) == low) and (tempo_val == low))or (find_most_recurring_val(feature_values) ==low):
        ret_room_list.append(star_room)
        # print("added star_room")


    if not ret_room_list:
        random_room_num = random.randint(1,8)
        new_room_num = 0
        """increase chances of cloud_room being picked when """
        if random_room_num == (7 or 8):
            new_room_num == cloud_room
        # print("added random_room_num", random_room_num)
        ret_room_list.append(new_room_num)
    # print(ret_room_list)
    return ret_room_list

from time import sleep
import struct

"""Add boolean status to first element of list and 0's as fillers"""
def updated_list(raw_list):
    new_list = [0] * 7

    new_list[0] = int(get_status())

    for i in range(1,len(raw_list)+1):
        if raw_list[i-1]!=0:
            new_list[raw_list[i-1]] = raw_list[i-1]
            # new_list.insert(i, raw_list[i-1])
            # new_list[i] = raw_list[i-1]

        # else:
            # new_list.insert(i, )
            # new_list[i] = 0
    # for i in range(len(raw_list)+1, len(new_list)-1):
    #     new_list[i] = 0
    return new_list

x = 0
def send_list_to_arduino():
    OUTPUT_QUEUE_SIZE = 64
    ser = serial.Serial('/dev/cu.usbserial-0001', 9600)

    ser.read(1)

    while True:
        json_response, connection = get_response()
        list_to_send = analyze_audio_features(json_response, connection)
        print(list_to_send)
        new_list = updated_list(list_to_send)
        print("list is", new_list)

        if ser.out_waiting < OUTPUT_QUEUE_SIZE:
            time.sleep(2)
            # print("NEW LIST VALUEs")
            print(new_list[0],new_list[1],new_list[2],new_list[3],new_list[4],new_list[5],new_list[6])
            ser.write(struct.pack('>BBBBBBB',new_list[0],new_list[1],new_list[2],new_list[3],new_list[4],new_list[5],new_list[6]))
            # ser.readline()

"""methods not being used"""
# def send_status_to_arduino():
#     OUTPUT_QUEUE_SIZE = 64
#     ser = serial.Serial('/dev/cu.usbserial-0001', 9600)
#     ser.read(1)
#     while True:
#         play_status = int(get_status())
#         print("status is", play_status)
#         if ser.out_waiting < OUTPUT_QUEUE_SIZE:
#             time.sleep(0.5)
#             # play_status_byte_array = (play_status).to_bytes(1, byteorder='big')
#             ser.write(struct.pack('>B', play_status))
#             # ser.write(play_status)

# def return_room_numbers(overall_mood):
#     for mood in overall_mood:
#         if examine_key(key) != overall_mood:
#             overall_mood.append(examine_key(key))
#     return overall_mood
#
# def examine_key(num):
#     num_to_al = {0: 'C', 1: 'C#/Db', 2: 'D', 3: 'D#/Eb', 4: 'E ', 5: 'F ', 6: ' F#/Gb ', 7: 'G', 8: 'G#/Ab', 9: 'A', 10: 'A#/Bb ', 11: 'B'}
#     al_to_des = {'C': '', 'C#/Db': '', 'D': 'a', 'D#/Eb': '', 'E': '', 'F': '', 'F#/Gb': '', 'G': '', 'G#/Ab': '', 'A': '', 'A#/Bb': '', 'B': ''}
#     print(num_to_al[num])



def main():
    json_response, connection = get_response()
    play_status = get_status()
    list_to_send = analyze_audio_features(json_response, connection)
    send_list_to_arduino()

if __name__ == "__main__":
    main()
