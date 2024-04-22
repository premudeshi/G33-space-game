import json
import requests
import pygame

from utils import getPath

# Loads any .json file, returns it in python dictionary.
def read_json_file(file_path):
    with open(getPath() + file_path, 'r') as file:
        data = json.load(file)
    return data
#Overwrites json files
def write_json_file(data, file_path):
    with open(getPath() + file_path, 'w') as file:
        json.dump(data, file)


# login takes a username and password and determine if it matches any users in the system
def login(username, password):
    data = read_json_file('accounts/accounts.json')
    for player in data['playerBase']:
        if player['username'] == username:
            if player['pass'] == password:
                return True
    return False

      
# signUp lets the user create a new account      
def signUp(username, password, matchPassword):
    if password == matchPassword:
        data = {'username' : username}
        response = requests.post('https://spaceshooter.udeshi.co.tz/users/create', json=data)
        if response.status_code == 200:
            #print("OK")
            dat = response.json()
            jsDat = read_json_file('accounts/accounts.json')
            userDat = jsDat['playerBase']
            tempDat = {'username':username,
                       'uuid' : dat['uuid'],
                       'key':dat['key'],
                       'pass':password}
            userDat.append(tempDat)
            write_json_file(jsDat, 'accounts/accounts.json')
            return True
        else:
            return False
    else:
        return False

# read the hi scores from the hi score file
def storeScores():
    response = requests.get('https://spaceshooter.udeshi.co.tz/scores/5')
    if response.status_code == 200:
        scores = response.json()
        return scores
    else:
        print(response.status_code)
        return []

# write the hi scores down in case the user set a new one
def writeScores(newName, newPoints):
    dat = read_json_file('accounts/accounts.json')
    for user in dat['playerBase']:
        if user['username'] == newName:
            data = {'username':newName, 'uuid':user['uuid'], 'secret':user['key']}
            break
    data['score'] = newPoints
    response = requests.post('https://spaceshooter.udeshi.co.tz/scores/create', json=data)
    if response.status_code == 200:
        pass
    else:
        print(response.json().get('message'))