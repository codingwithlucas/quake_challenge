# Candidato: Lucas Fernando de Souza Soares
# Data de nascimento: 23/09/1999
# E-mail: lucasgc55@yahoo.com
# Telefone: (43) 9 9695-7144
# Desafio Quake
# Pragma - estágio em desenvolvimento de sistemas (Gupy)
# Reposta construída com a linguagem Python.
# No final do script um arquivo .json é criado
# e as suas informações são exibidas na tela.

from os.path import exists
from json import dumps, load
from copy import deepcopy

games = []
game = {
          "game": 0,
          "status": {
             "total_kills": 0,
             "players": []
          }
        }
player = {
             "id": 0,
             "name": "",
             "kills": 0,
             "old_names": []
          }

data = {"game_id": 0, "names": [], "kills": []}
file_name = "Quake.txt"
mode = "r" 
file = open(file_name, mode)

def get_id(i, line):
    client_id = ""
    for letter in line[i:]:
        try:
            int(letter)
            client_id += letter
        except:
            break
    return int(client_id)


def get_name(i, line):
    user_name = ""
    for letter in line[i:]:
        if letter != "\\":
            user_name += letter
        else:
            break
    return user_name


for line in file.readlines():
    if "InitGame" in line:
        data["game_id"] += 1
    elif "ClientConnect" in line:
        # Getting client id and creating the parameters "names" and "kills" for him
        # Identificando o id do jogador e criando os parâmetros "names" e "kills" para ele
        client_id = get_id(22, line)
        ids = []
        c = 0
        while c < len(data["names"]):
            ids.append(data["names"][c][0])
            c += 1
        if client_id not in ids:
            data["names"].append([client_id])
            data["kills"].append([client_id, 0])
    elif "ClientUserinfoChanged" in line:
        # Getting user name and verifying whether he changed his name during the game
        # Coletando o nome do usuário e também verificando se ele mudou de nome ao longo do jogo
        client_id = get_id(30, line)
        user_name = get_name(34, line)
        c = 0
        while c < len(data["names"]):
            if (data["names"][c][0] == client_id):
                if user_name not in data["names"][c]:
                    data["names"][c].append(user_name)
            c += 1
    elif "Kill" in line:
        # Another name for <word> is 1022
        # <word> também pode ser chamado de 1022
        if "1022" in line:
            user_id = get_id(18, line)
            c = 0
            while c < len(data["kills"]):
                if data["kills"][c][0] == user_id:
                    data["kills"][c][1] -= 1
                    break
                c += 1
        else:
            sentence = ""
            for letter in line[12:]:
                if letter != ":":
                    sentence += letter
                else:
                    break
            players = sentence.split()
            player1 = int(players[0])
            c = 0
            while c < len(data["kills"]):
                if data["kills"][c][0] == player1:
                    data["kills"][c][1] += 1
                    break
                c += 1
    elif "ShutdownGame" in line:
        # Closing a game
        # Finalizando um jogo
        c = 0
        total_kills = 0
        while c < len(data["names"]):
            player["id"] = data["names"][c][0]
            player["name"] = data["names"][c][-1]
            player["kills"] = data["kills"][c][1]
            total_kills += player["kills"]
            if len(data["names"][c]) > 2:
                for n in data["names"][c][1:-1]:
                    player["old_names"].append(n)
            game["status"]["players"].append(player.copy())
            player["old_names"] = []
            c += 1
        game["game"] = data["game_id"]
        game["status"]["total_kills"] = total_kills
        games.append(deepcopy(game))
        game["game"] = 0
        game["status"]["total_kills"] = 0
        game["status"]["players"] = []
        data["names"] = []
        data["kills"] = []
file.close()

# Some games have negative total_kills because every time <word>, also known as 1022, kills somebody
# the person loses one "kill".
# Alguns jogos ficaram com total_kills negativo porque toda vez que <word>, também chamado de 1022, mata alguém
# uma "kill" é removida do jogador.
if not(exists("quake_data.json")):
    with open("quake_data.json", "w") as new_file:
        new_file.write(dumps(games, indent = 4))
        new_file.close()
    
with open("quake_data.json", "r") as json_file:
    quake_data = load(json_file)
    json_file.close()
    
print(dumps(quake_data, indent = 4))