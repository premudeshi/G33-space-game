import pygame


    
def login():
    username = input("please enter your username: ")
    userFile = open("accounts/accounts.txt", "r")
    userFile.seek(0)
    for line in userFile:
        currentUsername = line.strip()
        if currentUsername == username:
            password = input("please enter your password: ")
            currentPassword = userFile.readline().strip()
            if password == currentPassword:
                return True
            print("password: " + currentPassword + "\nyour password: " + password)
                    
    return False
        
def signUp():
    readUserFile = open("accounts/accounts.txt", "r")
    with open("accounts/accounts.txt", "a") as userFile:
        while True:
            newUsername = input("please enter your desired username: ")
            for line in readUserFile:
                if line.strip() == newUsername:
                    print("username already in use.")
                    return False
            while True:
                newPassword = input("please enter your desired password: ")
                matchPassword = input("please enter your desired password again: ")
                if newPassword == matchPassword:
                    userFile.write("\n" + newUsername.strip() + "\n" + newPassword.strip() + "\n")
                    print("account created. Please log in to play the game.")
                    return True