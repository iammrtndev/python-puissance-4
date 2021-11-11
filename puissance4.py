import os

ROUGE = '\033[31m'
BLEU = '\033[36m'
JAUNE = '\033[33m'
BLANC = '\033[0m'


def colorier(couleur, str):
    return f'{couleur}{str}{BLANC}'


def afficher_grille():
    print('1 2 3 4 5 6 7')
    for ligne in reversed(grille_jeu):
        print(' '.join(ligne))


def demander_colonne(n_joueur, jeton):
    colonne = input(
        f'\nÀ "{nom_joueurs[n_joueur]}" de placer {jeton} (1 à 7): ')
    if colonne.isnumeric() == False:
        raise Exception('Veuillez choisir un nombre de 1 à 7')

    colonne_int = int(colonne)
    if (colonne_int < 1) or (colonne_int > 7):
        raise Exception('Veuillez choisir de 1 à 7')

    return colonne_int - 1


def placer_jeton(colonne, jeton):
    for ligne in range(6):
        if grille_jeu[ligne][colonne] == '.':
            grille_jeu[ligne][colonne] = jeton
            return [ligne, colonne]

    raise Exception('Veuillez choisir une colonne non-remplie')


def verif_egalite():
    return ('.' in sum(grille_jeu, [])) == False


def fin_jeu_egalite():
    global grille_jeu
    afficher_grille()
    grille_jeu = [['.'] * 7 for _ in range(6)]
    print()
    input('Appuyez sur entrée pour continuer...')
    os.system('cls')


def deborde(x, y):
    return (0 <= y < 6 and 0 <= x < 7) == False


def compter_combo(pos, direction):
    y, x = pos[0], pos[1]
    dy, dx = direction[0], direction[1]
    gj = grille_jeu
    combo = 0
    for i in range(1, 4):
        ny, nx = y + i * dy, x + i * dx
        if deborde(
                nx,
                ny) or gj[ny - dy][nx - dx] != gj[ny][nx] or gj[ny][nx] == '.':
            break
        combo += 1
    return combo


def verif_vertical(pos):
    return compter_combo(pos, [-1, 0]) >= 3


def verif_horizontal(pos):
    return compter_combo(pos, [0, 1]) + compter_combo(pos, [0, -1]) >= 3


def verif_diagonale_slash(pos):
    return compter_combo(pos, [1, 1]) + compter_combo(pos, [-1, -1]) >= 3


def verif_diagonale_antislash(pos):
    return compter_combo(pos, [1, -1]) + compter_combo(pos, [-1, 1]) >= 3


def fin_jeu(s):
    global grille_jeu
    afficher_grille()
    grille_jeu = [['.'] * 7 for _ in range(6)]
    print(s)
    input('Appuyez sur entrée pour continuer...')
    os.system('cls')


grille_jeu = [['.'] * 7 for _ in range(6)]
tour = 0
nom_joueurs = [input('Nom du joueur 1: '), input('Nom du joueur 2: ')]

os.system('cls')  # Clear écran
while True:
    try:
        afficher_grille()
        n_joueur = tour % 2  # soit 0 soit 1
        couleur = ROUGE if n_joueur == 1 else BLEU
        jeton = colorier(couleur, 'O')
        colonne = demander_colonne(n_joueur, jeton)
        pos = placer_jeton(colonne, jeton)
        os.system('cls')

        fin_jeu_str = colorier(couleur,
                               f'\n"{nom_joueurs[n_joueur]}" a gagné!')
        if verif_egalite():
            fin_jeu(colorier(JAUNE, '\nÉgalité!'))
            fin_jeu_egalite()
        elif verif_vertical(pos):
            fin_jeu(fin_jeu_str)
        elif verif_horizontal(pos):
            fin_jeu(fin_jeu_str)
        elif verif_diagonale_slash(pos):
            fin_jeu(fin_jeu_str)
        elif verif_diagonale_antislash(pos):
            fin_jeu(fin_jeu_str)
        tour += 1
    except Exception as e:
        os.system('cls')
        print(colorier(JAUNE, f'{e}\n'))
