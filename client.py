import socket
import os

jeu_id = ''


def cls():
    os.system('cls')


def demander_nom():
    nom = ''
    while nom == '':
        nom = input('Veuillez entrer votre nom: ')
    return nom.encode()


def attendre(nom):
    print(f'À {nom} de jouer...')


def demander_colonne():
    colonne = ''
    colonne_int = -1
    while colonne == '':
        colonne = input('Veuillez entrer la colonne: ')
        if colonne.isdigit():
            colonne_int = int(colonne)
        if colonne_int < 0 or colonne_int > 7:
            colonne = ''
    return str(colonne_int - 1).encode()


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client.connect(('127.0.0.1', 26102))
client.connect(('49.12.199.72', 26102))
client.sendall(demander_nom())
while True:
    data = client.recv(1024)
    for l in data.decode().split('|'):
        if l != '':
            eval(l)
