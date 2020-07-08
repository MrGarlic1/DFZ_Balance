import discord
from dotenv import load_dotenv
from os import getenv

load_dotenv()
token = getenv('TOKEN')
tier1 = getenv('tier1')
tier2 = getenv('tier2')
tier3 = getenv('tier3')
tier4 = getenv('tier4')
client = discord.Client()


class PlayerInfo:  # Player object, contains name, tier, and their selected roles
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


class PlayerLobby:  # Lobby object, contains a list of players on radiant and dire
    def __init__(self):
        self.dire = [PlayerInfo(), PlayerInfo(), PlayerInfo(), PlayerInfo(), PlayerInfo()]
        self.radiant = [PlayerInfo(), PlayerInfo(), PlayerInfo(), PlayerInfo(), PlayerInfo()]
        self.lobby_num = 0

    def __repr__(self):
        return '<lobby_num=%s radiant=%s dire=%s>' % (self.lobby_num, self.radiant, self.dire)

    def __str__(self):  # Lobby print function for debugging purposes
        from termcolor import colored
        radiant_team = ''
        dire_team = ''
        for i in range(5):
            radiant_team += (
                            '        Position ' + str(i + 1) + ': ' +
                            colored(self.radiant[i].name + ', Tier ' +
                                    str(self.radiant[i].tier) + '\n', 'cyan')
                            )

            dire_team += (
                         '        Position ' + str(i + 1) + ': ' +
                         colored(self.dire[i].name + ', Tier ' +
                                 str(self.dire[i].tier) + '\n', 'cyan')
                         )
        return (
                'Lobby ' + str(self.lobby_num) + ':\n' +
                colored('    Radiant - \n', 'green') +
                radiant_team +
                colored('    Dire - \n', 'red') +
                dire_team
                )


def get_player_info(mention_list):
    def has_role(user, role_id):
        if role_id in [y.id for y in user.roles]:
            return True
        else:
            return False

    players = []

    for i in mention_list:
        # Adds player's name
        players.append(PlayerInfo())
        players.name = i

        # Grabs user object, adds the player's tier
        user_info = i[2:-1]
        if user_info[0] == '!':
            user_info = int(user_info[1:])
        user_info = client.get_user(user_info)
        if has_role(user_info, tier1):
            players[-1].tier = 1
        elif has_role(user_info, tier2):
            players[-1].tier = 2
        elif has_role(user_info, tier3):
            players[-1].tier = 3
        elif has_role(user_info, tier4):
            players[-1].tier = 4

        '''
        To-Do: Grab roles based on reactions to the signup message
        '''

    return players  # Returns list of PlayerInfo objects


def balance_lobby(players):
    def sum_tiers(teams):  # Collects sum of tiers on each team for balancing purposes
        total_radiant, total_dire = 0, 0
        for a in range(5):
            total_radiant += teams.radiant[a].tier
            total_dire += teams.radiant[a].tier
        return total_radiant, total_dire

    lobby_players = []
    out_games = []

    while len(players) > 0:
        if len(players) >= 10:
            lobby_players.append(players[0:10])
            del players[0:10]
        else:
            lobby_players.append(players[:])
            del players[:]
        print(players)
        out_games.append(PlayerLobby())
    del players
    for h in range(len(out_games)):  # For each lobby it will balance
        out_games[h].lobby_num = h + 1
        i = 0

        for max_roles in [1, 3, 5]:
            while i < len(lobby_players[h]):
                if len(lobby_players[h][i].roles) <= max_roles:  # Assigns players with <=1, then <=3, then <=5 roles selected
                    for j in range(5):
                        if j + 1 in lobby_players[h][i].roles:
                            if out_games[h].radiant[j].is_empty():
                                out_games[h].radiant[j] = lobby_players[h][i]
                                del lobby_players[h][i]
                                i -= 1
                                break
                            elif (out_games[h].dire[j].is_empty() and
                                    out_games[h].radiant[j].tier == lobby_players[h][i].tier):
                                out_games[h].dire[j] = lobby_players[h][i]
                                del lobby_players[h][i]
                                i -= 1
                                break
                i += 1

        i = 0
        while i < len(lobby_players[h]):  # Assigns players, ignoring tier
            for j in range(5):
                if j + 1 in lobby_players[h][i].roles:
                    if out_games[h].radiant[j].is_empty():
                        out_games[h].radiant[j] = lobby_players[h][i]
                        del lobby_players[h][i]
                        i -= 1
                        break
                    elif out_games[h].dire[j].is_empty():
                        out_games[h].dire[j] = lobby_players[h][i]
                        del lobby_players[h][i]
                        i -= 1
                        break
            i += 1

        i = 0
        while i < len(lobby_players[h]):  # Assigns players, ignoring tier and roles
            for j in range(5):
                if out_games[h].radiant[j].is_empty():
                    out_games[h].radiant[j] = lobby_players[h][i]
                    del lobby_players[h][i]
                    i -= 1
                    break
                elif out_games[h].dire[j].is_empty():
                    out_games[h].dire[j] = lobby_players[h][i]
                    del lobby_players[h][i]
                    i -= 1
                    break
            i += 1

        radiant_tier, dire_tier, = sum_tiers(out_games[h])
        i = 0
        while abs(radiant_tier - dire_tier) > 1:  # If one team is overall stronger
            if i > 4:  # Fail-safe
                break
            if radiant_tier > dire_tier:
                for i in range(5):
                    # If radiant tier is higher, swap teams for that role
                    if out_games[h].radiant[i].tier > out_games[h].dire[i].tier:
                        temp = out_games[h].radiant[i]
                        out_games[h].radiant[i] = out_games[h].dire[i]
                        out_games[h].dire[i] = temp
                        del temp
                        break
            elif dire_tier > radiant_tier:
                for i in range(5):
                    # If radiant tier is higher, swap teams for that role
                    if out_games[h].dire[i].tier > out_games[h].radiant[i].tier:
                        temp = out_games[h].radiant[i]
                        out_games[h].radiant[i] = out_games[h].dire[i]
                        out_games[h].dire[i] = temp
                        del temp
                        break
            radiant_tier, dire_tier, = sum_tiers(out_games[h])
            i += 1

    return out_games  # Returns list of lobby objects


'''
To-Do: Make function return only player mention strings in correct positions
'''
