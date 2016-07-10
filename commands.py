import random
import requests

# Dictionary containing all current commands
# * = authorized user command
# ** = owner command
command_list = [
    '8ball',
    'authorize**',
    'advice',
    'catfacts',
    'coinflip',
    'dance',
    'deauthorize**',
    'disconnect*',
    'help',
    'hi',
    'ignore**',
    'rslookup',
    'say*',
    'slayertask',
    'spamemote*',
    'translate',
    'unignore**',
    'weather'
]


def com_8ball(sender, query):
    # Command(8ball) - Uses Delegator Magic Eight Ball API to give a response
    r = requests.get("https://8ball.delegator.com/magic/JSON/a")
    parsed_r = r.json()
    try:
        return "@" + sender + " " + parsed_r['magic']['answer']
    except KeyError:
        return "Something went wrong. Please try again later."


def com_authorize(auth_users, user):
    # Command(authorize) - Add a user to the authorized user list if they aren't already authorized
    if user.lower() in auth_users:
        return "@" + user + " is already an authorized user."
    else:
        open("authorized.txt", "a").write(user.lower() + "\n")
        return "##a " + user


def com_advice():
    # Command(advice) - Prints advice string from AdviceSlip API
    r = requests.get("http://api.adviceslip.com/advice")
    parsed_r = r.json()
    try:
        return parsed_r['slip']['advice']
    except KeyError:
        return "Something went wrong. Please try again later."


def com_catfacts():
    # Command(catfacts) - Prints cat fact from CatFacts API
    r = requests.get("http://catfacts-api.appspot.com/api/facts")
    parsed_r = r.json()
    if parsed_r['success'] == "true":
        return parsed_r['facts'][0]
    else:
        return "Something went wrong. Please try again later."


def com_coinflip():
    # Command(coinflip) - Simulates a coin flip (float at end is for a unique message)
    randnum = random.randint(0, 1)
    if randnum == 1:
        return "Heads %.5f" % random.random()
    else:
        return "Tails %.5f" % random.random()


def com_dance():
    # Command(dance) - Dances
    return ".me dances"


def com_deauthorize(auth_users, user):
    # Command(deauthorize) - Removes user from authorized user list
    if not user.lower() in auth_users:
        return "@" + user + " is not an authorized user."
    else:
        auth_users.remove(user.lower())
        auth_users_file = open("authorized.txt", "w+")
        for u in auth_users:
            auth_users_file.write(u + "\n")
        auth_users_file.close()
        return "##d " + user


def com_disconnect():
    # Command(disconnect) - Makes bot disconnect and exit
    return "##z"


def com_help(sender):
    # Command(help) - Whispers the sender a list of commands
    response = "InsaiyanBot's commands are preceded with a tilde (~). The following commands" \
               " are available in this build of InsaiyanBot (* = authorized user command, ** = owner command): "
    for c in command_list:
        response += c + ", "
    response = response[:-2]
    return".w " + sender + " " + response


def com_hi(sender):
    # Command(hi) - Says hello to the sender
    return "@" + sender + " Hello!"


def com_ignore(user):
    # Command(ignore) - Ignores the user passed to the function
    return "##i " + user


def com_rslookup(mode, skill, username):
    # Command(rslookup) - Uses RuneScape Hiscores API to look up a user's level
    try:
        modes = {
            "rs3": "http://services.runescape.com/m=hiscore/index_lite.ws",
            "rs3im": "http://services.runescape.com/m=hiscore_ironman/index_lite.ws",
            "rs3hcim": "http://services.runescape.com/m=hiscore_hardcore_ironman/index_lite.ws",
            "osrs": "http://services.runescape.com/m=hiscore_oldschool/index_lite.ws",
            "osrsim": "http://services.runescape.com/m=hiscore_oldschool_ironman/index_lite.ws",
            "osrsuim": "http://services.runescape.com/m=hiscore_oldschool_ultimate/index_lite.ws",
            "dmm": "http://services.runescape.com/m=hiscore_oldschool_deadman/index_lite.ws",
            "sdmm": "http://services.runescape.com/m=hiscore_oldschool_seasonal/index_lite.ws"
        }
        modes_full = {
            "rs3": "RS3",
            "rs3im": "RS3 Ironman",
            "rs3hcim": "RS3 Hardcore Ironman",
            "osrs": "OSRS",
            "osrsim": "OSRS Ironman",
            "osrsuim": "OSRS Ultimate Ironman",
            "dmm": "Deadman Mode",
            "sdmm": "Seasonal Deadman Mode"
        }
        params = {
            "player": username
        }
        try:
            r = requests.get(modes[mode], params)
        except KeyError:
            return "Invalid mode given. Valid modes: rs3, rs3im, rs3hcim, osrs, osrsim, osrsuim, dmm, sdmm. Usage:" \
                   " ~rslookup <mode> <skill> <rsn>"
        levels = r.text.split("\n")
        skills = {
            "attack": 1,
            "defence": 2,
            "strength": 3,
            "constitution": 4,
            "hitpoints": 4,
            "ranged": 5,
            "prayer": 6,
            "magic": 7,
            "cooking": 8,
            "woodcutting": 9,
            "fletching": 10,
            "fishing": 11,
            "firemaking": 12,
            "crafting": 13,
            "smithing": 14,
            "mining": 15,
            "herblore": 16,
            "agility": 17,
            "thieving": 18,
            "slayer": 19,
            "farming": 20,
            "runecrafting": 21,
            "hunter": 22,
            "construction": 23,
            "summoning": 24,
            "dungeoneering": 25,
            "divination": 26,
            "invention": 27
        }
        if skill.lower() == "total":
            breakdown = levels[0].split(",")
            if int(breakdown[1]) >= 0:
                return "The " + modes_full[mode] + " account '" + username + "' has a total level of " + \
                        format(int(breakdown[1]), ",d") + " with " + format(int(breakdown[2]), ",d") + \
                        "xp and is ranked " + format(int(breakdown[0]), ",d") + " on the hiscores."
            else:
                return "This player's total level is not ranked in the hiscores."
        else:
            try:
                breakdown = levels[skills[skill.lower()]].split(",")
                if int(breakdown[1]) >= 0:
                    response = "The " + modes_full[mode] + " account '" + username + "' has"
                    if skill.lower()[0] in "aeiou":
                        response += " an "
                    else:
                        response += " a "
                    response += skill.lower() + " level of " + breakdown[1] + " with "\
                                + format(int(breakdown[2]), ",d") + "xp and is ranked " + \
                                format(int(breakdown[0]), ",d") + " in this skill on the hiscores."
                    return response
                else:
                    return "This player's " + skill.lower() + " level is not ranked in the hiscores."
            except KeyError:
                return "'" + skill + "' is not a valid skill. Usage: ~rslookup <mode> <skill> <rsn>"
    except:
        return "Couldn't find any results for " + modes_full[mode] + " account with username '" + username \
               + "'. Are you sure you typed it correctly?"


def com_say(message):
    # Command(say) - Repeats whatever string comes after the command
    return message


def com_slayertask(sender):
    # Command(slayertask) - Gives the sender a slayer task
    r = requests.get("http://services.runescape.com/m=itemdb_rs/bestiary/bestiary/slayerCatNames.json")
    parsed_r = r.json()
    monsters = list(parsed_r.keys())
    randnum = random.randint(0, len(monsters)-1)
    return "@" + sender + " Go kill " + str(random.randint(75, 250)) + " " + monsters[randnum] + "."


def com_spamemote(emote):
    #Command(spamemote) - Spams first argument after command across 3 messages
    return "##se " + emote


def com_translate(lang, query):
    #Command(translate) - Translates query using yandex API
    params = {
        "format": "plain",
        "key": "trnsl.1.1.20160707T195819Z.095fc8279bc639ed.f179d2e56d2ad59d8a016a8cb6aaa7bd7c9df67d",
        "lang": lang,
        "text": query
    }
    r = requests.get("https://translate.yandex.net/api/v1.5/tr.json/translate", params)
    parsed_r = r.json()
    if parsed_r['code'] == 200:
        print("success")
        response = "Translated: " + parsed_r['text'][0]
    else:
        response = "Language code is either unsupported or invalid. Look up ISO 639-1 language codes. "
        response += "Usage: ~translate fr hello OR ~translate en-fr hello"
    return response


def com_unignore(user):
    # Command(unignore) - Unignores the user passed to the function
    return "##u " + user


def com_weather(zipcode):
    #Command(weather) - Displays the weather for the given zip code using OpenWeatherMap API
    params = {
        "appid": "266a964f9fd10eb5bb378bb413d4b71e",
        "units": "imperial",
        "zip": zipcode + ",us"
    }
    r = requests.get("http://api.openweathermap.org/data/2.5/weather", params)
    parsed_r = r.json()
    if parsed_r['cod'] == 200:
        response = "Weather report for " + parsed_r['name'] + " - "
        response += "Current conditions: " + parsed_r['weather'][0]['main']
        response += " (" + str(parsed_r['clouds']['all']) + "% cloud cover). "
        response += "The current temperature is " + str(parsed_r['main']['temp']) + "°F with "
        response += str(parsed_r['main']['humidity']) + "% humidity. "
        response += "Winds are moving at " + str(parsed_r['wind']['speed']) + "mph."
    else:
        response = "Invalid zip code given. Usage: ~weather <zipcode>"
    return response


def handle_command(command_string, sender, owner, auth_users):
    # Splits raw command string into a command and arguments
    args = command_string.split(" ")
    command = args.pop(0)

    # Passes relevant arguments to the correct command function
    if command.lower() == "8ball":
        if len(args) < 1:
            return "@" + sender + " you didn't ask a question. Usage: ~8ball <question>"
        else:
            query = ""
            for i in args:
                query += i + " "
            query = query[:-1]
            return com_8ball(sender, query)

    elif command.lower() == "advice":
        return com_advice()

    elif command.lower() == "authorize":
        if sender != owner:
            return ".w " + sender + " This command is for my owner's use only."
        elif len(args) < 1:
            return "You didn't provide a user to authorize. Usage: ~authorize <user>"
        else:
            return com_authorize(auth_users, args[0])

    elif command.lower() == "catfacts":
        return com_catfacts()

    elif command.lower() == "coinflip":
        return com_coinflip()

    elif command.lower() == "dance":
        return com_dance()

    elif command.lower() == "deauthorize":
        if sender != owner:
            return ".w " + sender + " This command is for my owner's use only."
        elif len(args) < 1:
            return "You didn't provide a user to deauthorize. Usage: ~deauthorize <user>"
        else:
            return com_deauthorize(auth_users, args[0])

    elif command.lower() == "disconnect":
        if sender not in auth_users and sender != owner:
            return ".w " + sender + " This command is for authorized users only."
        else:
            return com_disconnect()

    elif command.lower() == "help":
        return com_help(sender)

    elif command.lower() == "hi":
        return com_hi(sender)

    elif command.lower() == "ignore":
        if sender != owner:
            return ".w " + sender + " This command is for my owner's use only."
        elif len(args) < 1:
            return "You didn't provide a user to ignore. Usage ~ignore <user>"
        else:
            return com_ignore(args[0])

    elif command.lower() == "rslookup":
        if len(args) < 3:
            return "Too few arguments given. Usage: ~rslookup <mode> <skill> <rsn> - Valid modes: rs3, rs3im, rs3hcim" \
                   ", osrs, osrsim, osrsuim, dmm, sdmm"
        else:
            mode = args.pop(0).lower()
            skill = args.pop(0).lower()
            rsn = ""
            for i in args:
                rsn += i + " "
            rsn = rsn[:-1]
            return com_rslookup(mode, skill, rsn)

    elif command.lower() == "say":
        if sender not in auth_users and sender != owner:
            return ".w " + sender + " This command is for authorized users only."
        else:
            message = ""
            for i in args:
                message += i + " "
            message = message[:-1]
            return com_say(message)

    elif command.lower() == "slayertask":
        return com_slayertask(sender)

    elif command.lower() == "spamemote":
        if sender not in auth_users and sender != owner:
            return ".w " + sender + " This command is for authorized users only."
        else:
            emote = args[0]
            return com_spamemote(emote)

    elif command.lower() == "translate":
        if len(args) < 2:
            return "Too few arguments given. Usage: ~translate fr hello OR ~translate en-fr hello"
        else:
            lang = args.pop(0)
            query = ""
            for i in args:
                query += i + " "
            query = query[:-1]
            return com_translate(lang, query)

    elif command.lower() == "unignore":
        if sender != owner:
            return ".w " + sender + " This command is for my owner's use only."
        elif len(args) < 1:
            return "You didn't provide a user to unignore. Usage: ~unignore <user>"
        else:
            return com_unignore(args[0])

    elif command.lower() == "weather":
        if len(args) < 1:
            return "Please provide a zip code for weather lookup. Usage: ~weather <zip>"
        elif not args[0].isnumeric():
            return "Invalid zip code given. Usage: ~weather <zip>"
        else:
            return com_weather(args[0])

    # Returns an empty response if an invalid command was given
    else:
        return ""
