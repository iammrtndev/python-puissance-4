import socket
import threading


ROUGE = '\033[31m'
BLEU = '\033[36m'
JAUNE = '\033[33m'
BLANC = '\033[0m'


def colorier(couleur, str):
    return f'{couleur}{str}{BLANC}'


def encode(eval: str):
    return f'{eval}|'.encode()


def deborde(x, y):
    return (0 <= y < 6 and 0 <= x < 7) == False


class Joueur:
    def __init__(self, nom: str, soc: socket):
        self.nom = nom
        self.soc = soc
        self.jeton = ''


class Puissance4Jeu:
    def __init__(self, joueur1: Joueur, joueur2: Joueur):
        joueur1.jeton = colorier(BLEU, 'O')
        joueur2.jeton = colorier(ROUGE, 'O')
        self.joueur1 = joueur1
        self.joueur2 = joueur2
        self.grille_jeu = [['.']*7 for _ in range(6)]
        threading.Thread(target=self.commencer).start()

    def commencer(self):
        self.cls_aux_joueurs()
        tour = 0
        while True:
            try:
                self.affiche_grille_aux_joueurs()
                placeur = self.joueur2 if tour % 2 else self.joueur1
                attend = self.joueur1 if tour % 2 else self.joueur2
                attend.soc.sendall(encode(f'attendre("{placeur.nom}")'))
                placeur.soc.sendall(
                    encode(f'client.sendall(demander_colonne())'))
                colonne = int(placeur.soc.recv(1024).decode())
                pos = self.placer_jeton(colonne, placeur.jeton)
                self.cls_aux_joueurs()
                if self.verif_egalite():
                    self.fin_jeu_egalite()
                elif self.verif_vertical(pos):
                    self.fin_jeu(placeur)
                elif self.verif_horizontal(pos):
                    self.fin_jeu(placeur)
                elif self.verif_diagonale_slash(pos):
                    self.fin_jeu(placeur)
                elif self.verif_diagonale_antislash(pos):
                    self.fin_jeu(placeur)
                tour += 1
            except:
                self.joueur1.soc.close()
                self.joueur2.soc.close()
                return

    def affiche_grille_aux_joueurs(self):
        data = '1 2 3 4 5 6 7\\n'
        for ligne in reversed(self.grille_jeu):
            data += f"{' '.join(ligne)}\\n"
        eval = encode(f"print('{data}')")
        self.joueur1.soc.sendall(eval)
        self.joueur2.soc.sendall(eval)

    def cls_aux_joueurs(self):
        self.joueur1.soc.sendall(encode('cls()'))
        self.joueur2.soc.sendall(encode('cls()'))

    def print_aux_joueurs(self, s):
        self.joueur1.soc.sendall(encode(f'print("{s}")'))
        self.joueur2.soc.sendall(encode(f'print("{s}")'))

    def input_aux_joueurs(self, s):
        self.joueur1.soc.sendall(encode(f'input("{s}")'))
        self.joueur2.soc.sendall(encode(f'input("{s}")'))

    def placer_jeton(self, colonne, jeton):
        for y in range(6):
            if self.grille_jeu[y][colonne] == '.':
                self.grille_jeu[y][colonne] = jeton
                return [y, colonne]

    def verif_egalite(self):
        return ('.' in sum(self.grille_jeu, [])) == False

    def fin_jeu_egalite(self):
        self.affiche_grille_aux_joueurs()
        self.grille_jeu = [['.']*7 for _ in range(6)]
        self.print_aux_joueurs('\\n')
        self.print_aux_joueurs(colorier(JAUNE, 'Égalité!'))
        self.input_aux_joueurs('Appuyez sur entrée pour continuer...')
        self.cls_aux_joueurs()

    def compter_combo(self, pos, direction):
        y, x = pos[0], pos[1]
        dy, dx = direction[0], direction[1]
        gj = self.grille_jeu
        combo = 0
        for i in range(1, 4):
            ny, nx = y + i*dy, x + i*dx
            if deborde(nx, ny) or gj[ny - dy][nx - dx] != gj[ny][nx] or gj[ny][nx] == '.':
                break
            combo += 1
        return combo

    def verif_vertical(self, pos):
        return self.compter_combo(pos, [-1, 0]) >= 3

    def verif_horizontal(self, pos):
        return self.compter_combo(pos, [0, 1]) + self.compter_combo(pos, [0, -1]) >= 3

    def verif_diagonale_slash(self, pos):
        return self.compter_combo(pos, [1, 1]) + self.compter_combo(pos, [-1, -1]) >= 3

    def verif_diagonale_antislash(self, pos):
        return self.compter_combo(pos, [1, -1]) + self.compter_combo(pos, [-1, 1]) >= 3

    def fin_jeu(self, gagnant):
        self.affiche_grille_aux_joueurs()
        self.grille_jeu = [['.']*7 for _ in range(6)]
        self.print_aux_joueurs(f'\\n{gagnant.nom} a gagné!')
        self.input_aux_joueurs('Appuyez sur entrée pour continuer...')
        self.cls_aux_joueurs()


salle_attente = []


def recherche_adversaire():
    if len(salle_attente) == 0:
        return None

    while len(salle_attente) > 0:
        adversaire = salle_attente.pop()
        try:
            adversaire.soc.sendall(b'')
        except:
            continue
        else:
            return adversaire


serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serveur.bind(('127.0.0.1', 26102))
serveur.listen()
while True:
    soc, _ = serveur.accept()
    try:
        joueur_nom = soc.recv(1024).decode()
        if joueur_nom == '':
            raise

        joueur = Joueur(joueur_nom, soc)
        adversaire = recherche_adversaire()
        if adversaire is None:
            salle_attente.append(joueur)
            joueur.soc.sendall(b'cls()|')
            joueur.soc.sendall(b'print("En recherche d\'adversaire...")|')
            continue

        Puissance4Jeu(adversaire, joueur)
    except:
        soc.close()
