import commands
import listenfunctions
import os
import queue
import random
import socket
import sys
from threading import Thread
import time


def format_message(channel, message):
    # Function for formatting messages ready to be sent to the server
    return "PRIVMSG " + channel + " :" + message + "\r\n"

# Prints welcome message on launch
motd = "Welcome to InsaiyanBot V2.0! W00t!"
print(("*" * len(motd)) + ("\n" + motd + "\n") + ("*" * len(motd)))

# Import or create user list
try:
    user_list = open("userlist.txt", "r").readlines()
    users = {}
    for u in user_list:
        users[u.split("::")[0].lower()] = u.split("::")[1]
except FileNotFoundError:
    print("User list not found. Creating user list file...")
    open("userlist.txt", "w+")
    input("User list file has been created:\n('" + os.path.dirname(os.path.realpath(__file__)) +
          "\\userlist.txt')\nThis list must be populated with at least one Twitch username and OAuth code in\nthe"
          " following format:\nuser1::oauth:abcdefgh12345\nuser2::oauth:abcdefgh12345\nuser3::oauth:abcdefgh12345"
          "\nThe OAuth code associated with a Twitch account can be found at this link:"
          "\nhttp://www.twitchapps.com/tmi/\nPress the enter key to exit.")
    sys.exit(1)
except:
    print("User list is incorrectly formatted. Press the enter key to exit.")
    sys.exit(1)

# Import or create authorized user list
try:
    auth_users = open("authorized.txt", "r").read().splitlines()
except FileNotFoundError:
    print("Authorized user list not found. Creating authorized user list file...")
    open("authorized.txt", "w+")
    print("Authorized user list file has been created:\n('" + os.path.dirname(os.path.realpath(__file__)) +
          "\\authorized.txt')")
    auth_users = []

# Pick Twitch user from user list to run bot as
while True:
    try:
        user_input = input("Please enter the Twitch username you would like to use from the user list.\n>")
        botnick = user_input.lower()
        botpass = users[user_input.lower()]
        break
    except KeyError:
        print("User '" + user_input + "' does not exist in the user list. User list:")
        for u in list(users.keys()):
            print("- " + u)

# Pick channel to join
channel = ""
while channel == "":
    channel = ("#" + input("Please enter the channel you would like to join. (Twitch username)\n>").lower())
    confirm = ""
    while confirm != "yes" and confirm != "no" and confirm != "y" and confirm != "n":
        confirm = input("Are you sure you want to join the channel '" + channel[1:] + "'? (yes or no)\n>").lower()
        if confirm == "yes" or confirm == "y":
            break
        elif confirm == "no" or confirm == "n":
            channel = ""
            break
        else:
            print("Invalid input.")

# Specify who the owner of this bot is
owner = ""
while owner == "":
    owner = input("Who is my owner? (Twitch username)\n>").lower()
    confirm = ""
    while confirm != "yes" and confirm != "no" and confirm != "y" and confirm != "n":
        confirm = input("Are you that '" + owner + "' is my owner? (yes or no)\n>").lower()
        if confirm == "yes" or confirm == "y":
            break
        elif confirm == "no" or confirm == "n":
            owner = ""
            break
        else:
            print("Invalid input.")

# Choose whether or not to enable clean chat mode
user_input = ""
while user_input != "yes" and user_input != "no" and user_input != "y" and user_input != "n":
    user_input = input("Clean chat mode? (yes or no)\n>").lower()
    if user_input != "yes" and user_input != "no" and user_input != "y" and user_input != "n":
        print("Invalid input.")

if user_input == "yes" or user_input == "y":
    clean = True
else:
    clean = False

# Choose whether or not to enable the bot's greeting
user_input = ""
while user_input != "yes" and user_input != "no" and user_input != "y" and user_input != "n":
    user_input = input("Greet on entry? (yes or no)\n>").lower()
    if user_input != "yes" and user_input != "no" and user_input != "y" and user_input != "n":
        print("Invalid input.")

if user_input == "yes" or user_input == "y":
    greet = True
else:
    greet = False

# Set server variables
server = "irc.chat.twitch.tv"
port = 6667

# Attempt to connect to server
print("Connecting, please wait...")
irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    irc.connect((server, port))
except:
    input("Failed to connect to server. Press the enter key to exit.")
    sys.exit(1)
irc.setblocking(False)

# Authorize bot once connected to server
time.sleep(1)
irc.send(("PASS " + botpass + "\r\n").encode())
time.sleep(1)
irc.send(("USER " + botnick + " " + botnick + " " + botnick + " :Hello, I am InsaiyanBot V2.0!\r\n").encode())
time.sleep(1)
irc.send(("NICK " + botnick + "\n").encode())
time.sleep(1)
irc.send(("JOIN " + channel + "\n").encode())

# Create message queue object
message_queue = queue.Queue()

# Define loop for message queue
def thread_test(message_queue):
    while True:
        time.sleep(1.6)
        if not message_queue.empty():
            message = message_queue.get()
            irc.send(message.encode())

# Begin message queue loop
message_loop = Thread(target=thread_test, args=(message_queue,))
message_loop.start()

# Listen options
brobbob = True
brobfreezy = True
firstMessage = False

# Begin listen loop
while True:
    # Get raw response from server and format it if in clean chat mode
    try:
        data = irc.recv(2048).decode()
        if data != "":
            if not firstMessage:
                print("Connected!")
            if clean and data.find("PRIVMSG") != -1:
                message = data.split(":")
                message.pop(0)
                message.pop(0)
                final_message = ""
                for s in message:
                    final_message += s + ":"
                final_message = final_message[:-1]
                print(data.split("!")[0][1:] + ":", final_message, end="")
            if not clean:
                print(data)
        response = ""
    except Exception:
        data = ""

    # Reply to PING requests so the bot doesn't get disconnected
    if data.find("PING") != -1:
        response = "PONG " + data.split()[1] + "\r\n"
        irc.send(response.encode())
        if not clean:
            print(response)
        response = ""

    # If a message is sent to the server, see if it meets listening criteria or if it's a command
    if data.find("PRIVMSG") != -1:
        if brobbob and channel == "#brobsonstreams":
            if random.randint(1, 10000) == 1:
                message_queue.put(format_message(channel, listenfunctions.brobbob(data.split("!")[0][1:])))
                print("*" + botnick + ":", listenfunctions.brobbob(data.split("!")[0][1:]))
        if brobfreezy and channel == "#brobsonstreams":
            if random.randint(1, 500) == 1:
                message_queue.put(format_message(channel, listenfunctions.brobfreezy()))
                print("*" + botnick + ":", listenfunctions.brobfreezy())
        if greet:
            message_queue.put(format_message(channel, listenfunctions.greet()))
            print("*" + botnick + ":", listenfunctions.greet())
            greet = False
        if data.split(":")[2].find("~") == 0:
            response = commands.handle_command(data.split(":")[2][1:-2], data.split("!")[0][1:], owner, auth_users)

    # Update authorized user list if it's updated in commands script (authorization)
    if response.find("##a") == 0:
        auth_users.append(response.split(" ")[1])
        response = "@" + response.split(" ")[1] + " is now an authorized user."

    # Update authorized user list if it's updated in commands script (deauthorization)
    if response.find("##d") == 0:
        auth_users = open("authorized.txt", "r").read().splitlines()
        response = "@" + response.split(" ")[1] + " is no longer an authorized user."

    if response.find("##z") == 0:
        message_queue.put(format_message(channel, "Disconnecting, goodbye everyone... BibleThump"))
        time.sleep(5)
        sys.exit(0)

    # Handle ignore request from commands script
    if(response.find("##i")) == 0:
        ignore_user = response.split(" ")[1]
        message_queue.put(format_message(channel, ".ignore " + ignore_user))
        response = "@" + ignore_user + " has been ignored."

    # Handle spamemote request from commands script
    if response.find("##se") == 0:
        emote = response.split(" ")[1]
        for i in range(28, 31):
            message_queue.put(format_message(channel, (emote + " ") * i))
            print("*" + botnick + ":", (emote + " ") * i)
        response = ""

    # Handle unignore request from commands script
    if (response.find("##u")) == 0:
        unignore_user = response.split(" ")[1]
        message_queue.put(format_message(channel, ".unignore " + unignore_user))
        response = "@" + unignore_user + " has been unignored."

    # Forward response to message queue if it's not empty
    if response != "":
        if clean:
            print("*" + botnick + ":", response)
            response = format_message(channel, response)
        if not clean:
            response = format_message(channel, response)
            print(response)
        message_queue.put(response)
        response = ""

    # Clear current data block
    data = ""

    # Mark that a response was received from the server to confirm connection
    firstMessage = True
