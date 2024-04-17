import pygame


# login takes a username and password and determine if it matches any users in the system
def login(username, password):
    # "the system" in question:
    userFile = open("accounts/accounts.txt", "r")
    userFile.seek(0)
    # for every line in the file
    for line in userFile:
        # take the username
        currentUsername = line.strip()
        # if the usernames match, check if the passwords match. If so, log the user in.
        if currentUsername == username:
            currentPassword = userFile.readline().strip()
            if password == currentPassword:
                return True
    # if we reach here, no match was found, so user cannot log in
    return False
      
# signUp lets the user create a new account      
def signUp(username, password, matchPassword):
    readUserFile = open("accounts/accounts.txt", "r")
    # append mode will let us add them into the system at the end
    with open("accounts/accounts.txt", "a") as userFile:
        # check through every username to ensure they arent taken. Return false if it is
        for line in readUserFile:
            if line.strip() == username:
                return False
        # if here, then there was no issue with the username. If the entered passwords match, we can create the new user by appending the file
        if password == matchPassword:
            userFile.write("\n" + username.strip() + "\n" + password.strip() + "\n")
            return True
        # passwords didnt match, return false
        else:
            return False
# read the hi scores from the hi score file
def storeScores():
    # open file
    readScoreFile = open("accounts/scores.txt", 'r')
    # arrays to hold the names and points
    nameArr = [" ", " ", " ", " ", " "]
    scoreArr = [0, 0, 0, 0, 0]
    # loop through the 5 scores and add them to the leaderboard arrays
    i = 0
    for line in readScoreFile:
        nameArr[i] = line.strip()
        scoreArr[i] = int(readScoreFile.readline())
        i+= 1
    # return the arrays
    return nameArr, scoreArr
    
# write the hi scores down in case the user set a new one
def writeScores(nameArr, scoreArr, newName, newPoints):
    # very very ugly code, but it works. Simply check the position of the new score to determine if it belongs on the leaderboard. If so, bump the others down.
    if (newPoints >= scoreArr[0]):
        scoreArr[4] = scoreArr[3]
        nameArr[4] = nameArr[3]
        scoreArr[3] = scoreArr[2]
        nameArr[3] = nameArr[2]
        scoreArr[2] = scoreArr[1]
        nameArr[2] = nameArr[1]
        scoreArr[1] = scoreArr[0]
        nameArr[1] = nameArr[0]
        scoreArr[0] = newPoints
        nameArr[0] = newName
    elif (newPoints >= scoreArr[1]):
        scoreArr[4] = scoreArr[3]
        nameArr[4] = nameArr[3]
        scoreArr[3] = scoreArr[2]
        nameArr[3] = nameArr[2]
        scoreArr[2] = scoreArr[1]
        nameArr[2] = nameArr[1]
        scoreArr[1] = newPoints
        nameArr[1] = newName
    elif (newPoints >= scoreArr[2]):
        scoreArr[4] = scoreArr[3]
        nameArr[4] = nameArr[3]
        scoreArr[3] = scoreArr[2]
        nameArr[3] = nameArr[2]
        scoreArr[2] = newPoints
        nameArr[2] = newName
    elif (newPoints >= scoreArr[3]):
        scoreArr[4] = scoreArr[3]
        nameArr[4] = nameArr[3]
        scoreArr[3] = newPoints
        nameArr[3] = newName
    elif (newPoints >= scoreArr[4]):
        scoreArr[4] = newPoints
        nameArr[4] = newName
        
    # now write the new scores and names to the hi score file
    writeScoreFile = open("accounts/scores.txt", 'w')
    for i in range (5):
        writeScoreFile.write(str(nameArr[i]) + '\n' + str(scoreArr[i]) + '\n')