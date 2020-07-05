from os import getenv
import discord
from random import randint
import asyncio
from dotenv import load_dotenv

load_dotenv()
token = getenv('TOKEN')
tier1_id = getenv('tier1')
tier2_id = getenv('tier2')
tier3_id = getenv('tier3')
tier4_id = getenv('tier4')
signup_channel = getenv('signup_channel')
prefix = '>'

client = discord.Client()


class PlayerInfo:
    def __init__(self):
        self.name = 'N/A'
        self.tier = 1
        self.roles = []

    def __repr__(self):
        return '<name=%s tier=%s roles=%s>' % (self.name, self.tier, self.roles)

    def __str__(self):
        return 'Name: %s    Tier: %s    Roles: %s' % (self.name, self.tier, self.roles)

    def is_empty(self):
        if self.name == 'N/A':
            return True
        else:
            return False


def get_player_info(plr):
    plr_info = PlayerInfo()
    if tier1_id in [y.id for y in plr.roles]:
        plr_info.tier = 1
    elif tier2_id in [y.id for y in plr.roles]:
        plr_info.tier = 2
    elif tier3_id in [y.id for y in plr.roles]:
        plr_info.tier = 3
    elif tier4_id in [y.id for y in plr.roles]:
        plr_info.tier = 4

    plr_info.name = '<!' + str(plr.id) + '>'
    plr_info.roles = [1, 2, 3, 4, 5]  # Temporary, no lobby react command yet


def remove_blanks(word_list):
    element = 0
    while element < len(word_list):
        if word_list[element] == '':
            del word_list[element]
            element -= 1
        element += 1
    return word_list


def is_command(text, pref):
    if not text.author.bot:
        if str(text.channel.type) != 'private':
            if text.content.startswith(pref) and text.content[1] != ' ':
                return True
            else:
                return False
        else:
            return False
    else:
        return False


def get_mention_info(mention_str, server):
    try:
        mention_str = mention_str[2:-1]

        if mention_str[0] == '!':  # If the mention is a user
            mention_str = mention_str[1:]
            mentioned = client.get_user(int(mention_str))
        elif mention_str[0] == '&':  # If the mention is a role
            mention_str = mention_str[1:]
            mentioned = server.get_role(int(mention_str))
        else:
            return False

        return mentioned

    except IndexError or ValueError:
        return False


def balance_lobby(players):
    lobby = [
        [PlayerInfo(), PlayerInfo()],
        [PlayerInfo(), PlayerInfo()],
        [PlayerInfo(), PlayerInfo()],
        [PlayerInfo(), PlayerInfo()],
        [PlayerInfo(), PlayerInfo()]
    ]

    def sum_tiers(teams):
        total_radiant, total_dire = 0, 0
        print(teams)
        for a in range(len(teams)):
            total_radiant += teams[a][0].tier
            total_dire += teams[a][1].tier
        print(total_radiant)
        print(total_dire)
        return total_radiant, total_dire

    i = 0
    while i < len(players):
        if len(players[i].roles) == 1:  # Assigns players with 1 role selected
            for j in range(len(lobby)):
                if j + 1 in players[i].roles:
                    if lobby[j][0].is_empty():
                        lobby[j][0] = players[i]
                        del players[i]
                        i -= 1
                        break
                    elif lobby[j][1].is_empty() and lobby[j][0].tier == players[i].tier:
                        lobby[j][1] = players[i]
                        del players[i]
                        i -= 1
                        break
        i += 1

    i = 0
    while i < len(players):
        if len(players[i].roles) <= 3:  # Assigns players with 2-3 roles selected
            for j in range(len(lobby)):
                if j + 1 in players[i].roles:
                    if lobby[j][0].is_empty():
                        lobby[j][0] = players[i]
                        del players[i]
                        i -= 1
                        break
                    elif lobby[j][1].is_empty() and lobby[j][0].tier == players[i].tier:
                        lobby[j][1] = players[i]
                        del players[i]
                        i -= 1
                        break
        i += 1

    i = 0
    while i < len(players):
        if len(players[i].roles) > 3:  # Assigns players with 3+ roles selected
            for j in range(len(lobby)):
                if j + 1 in players[i].roles:
                    if lobby[j][0].is_empty():
                        lobby[j][0] = players[i]
                        del players[i]
                        i -= 1
                        break
                    elif lobby[j][1].is_empty() and lobby[j][0].tier == players[i].tier:
                        lobby[j][1] = players[i]
                        del players[i]
                        i -= 1
                        break
        i += 1

    i = 0
    while i < len(players):
        for j in range(len(lobby)):  # Assigns players, ignoring tier
            if j + 1 in players[i].roles:
                if lobby[j][0].is_empty():
                    lobby[j][0] = players[i]
                    del players[i]
                    i -= 1
                    break
                elif lobby[j][1].is_empty():
                    lobby[j][1] = players[i]
                    del players[i]
                    i -= 1
                    break
        i += 1

    i = 0
    while i < len(players):
        for j in range(len(lobby)):  # Assigns players, ignoring tier and role
            if lobby[j][0].is_empty():
                lobby[j][0] = players[i]
                del players[i]
                i -= 1
                break
            elif lobby[j][1].is_empty():
                lobby[j][1] = players[i]
                del players[i]
                i -= 1
                break
        i += 1
    del i

    radiant_tier, dire_tier, = sum_tiers(lobby)
    iters = 0
    while abs(radiant_tier - dire_tier) > 1:  # If one team is overall stronger
        if iters > 4:  # Fail-safe
            break
        if radiant_tier > dire_tier:
            for i in range(len(lobby)):
                if lobby[i][0].tier > lobby[i][1].tier:  # If radiant tier is higher, swap teams for that role
                    temp = lobby[i][0]
                    lobby[i][0] = lobby[i][1]
                    lobby[i][1] = temp
                    del temp
                    break
        elif dire_tier > radiant_tier:
            for i in range(len(lobby)):
                if lobby[i][1].tier > lobby[i][0].tier:  # If dire tier is higher, swap teams for that role
                    temp = lobby[i][0]
                    lobby[i][0] = lobby[i][1]
                    lobby[i][1] = temp
                    del temp
                    break
        radiant_tier, dire_tier, = sum_tiers(lobby)
        iters += 1
    return lobby


def shuffle_lobby(lobby):
    for i in range(len(lobby)):
        if lobby[i][0].tier == lobby[i][1].tier:
            if randint(0, 1) == 1:
                temp = lobby[i][0]
                lobby[i][0] = lobby[i][1]
                lobby[i][1] = temp
                del temp
    return lobby


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    if is_command(message, prefix):
        guild = message.channel.guild
        args = []
        message_list = message.content.split(' ')  # Splits command into command and arguments
        cmd = message_list[0][1:].lower()
        if len(message_list) > 1:
            args = remove_blanks(message_list[1:])

        if cmd == 'balance':
            player_list = []
            for i in range(len(args)):
                player_list.append(
                    get_player_info(
                        get_mention_info(args[i], guild)
                    )
                )
            lobby_list = balance_lobby(player_list)
            lobby_list = shuffle_lobby(lobby_list)

            await message.channel.send('Test')