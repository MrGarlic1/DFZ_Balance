from termcolor import colored
from random import randint
from colorama import init
init()

ver = '1.2.3'


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


def name_input(prompt):
    return input(prompt)


def tier_input(prompt):
    tier = input(prompt)
    try:
        tier = int(tier)
        if not 1 <= tier <= 4:
            print(colored('Invalid tier entered. Tiers must be an integer from 1-4.', 'red'))
            tier = tier_input(prompt)
    except ValueError:
        print(colored('Invalid tier entered. Tiers must be an integer from 1-4.', 'red'))
        tier = tier_input(prompt)
    return tier


def roles_input(prompt):
    roles = input(prompt)
    if ',' in roles:
        roles = roles.split(',')
    else:
        roles = roles.split(' ')
        i = 0
        while i < len(roles):
            if roles[i] == '':
                del roles[i]
                i -= 1
            i += 1
    try:
        roles = [int(i) for i in roles]
    except ValueError:
        print(colored('Invalid roles entered. Please try again.', 'red'))
        roles = roles_input(prompt)

    if min(roles) < 1 or max(roles) > 5:
        print(colored('Invalid roles entered. Please try again.', 'red'))
        roles = roles_input(prompt)
    if len(roles) > 5:
        roles = roles[0:5]
    return roles


player_list = []

while True:
    player_count = len(player_list) + 1
    player = PlayerInfo()
    player.name = name_input('\nPlayer ' + str(player_count) + ' Name: ')
    if not player.name:
        break

    player.tier = tier_input('Player ' + str(player_count) + ' Tier: ')
    player.roles = roles_input('Player ' + str(player_count) + ' Roles: ')
    player_list.append(player)

print(player_list)

if len(player_list) >= 20:
    player_list_2 = player_list[10:20]
    player_list = player_list[0:10]
elif 10 < len(player_list) < 20:
    player_list = player_list[0:10]

lobby_list = balance_lobby(player_list)
lobby_list = shuffle_lobby(lobby_list)

print(colored('Radiant: ', 'green'))
for pos in range(len(lobby_list)):
    print(
        '    Position ' + str(pos + 1) + ': ' +
        colored(lobby_list[pos][0].name + ', Tier ' + str(lobby_list[pos][0].tier), 'cyan')
        )

print(colored('\n' + 'Dire: ', 'red'))
for pos in range(len(lobby_list)):
    print(
        '    Position ' + str(pos + 1) + ': ' +
        colored(lobby_list[pos][1].name + ', Tier ' + str(lobby_list[pos][1].tier), 'cyan')
        )