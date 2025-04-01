import numpy as np


def open_file(path):
    test = []

    with open(path, "r") as f:
        lignes = f.readlines()
        for i in range(0, len(lignes), 2):
            m, n = lignes[i].split()
            taille = [int(m), int(n)]

            figures = lignes[i + 1].split()
            liste = [taille]
            for i in range(0, len(figures), 2):
                coordonnees = [int(figures[i]) + 1, int(figures[i + 1]) + 1]
                liste.append(coordonnees)

            test.append(liste)

        return test


def checkpoints(taille):
    etapes = []
    for i in range(1, 4, 1):
        etapes.append(i * taille[0] * taille[1] // 4)
    return etapes


def new_matrice(taille):
    matrice = np.empty((taille[0] + 2, taille[1] + 2))
    for i in range(0, taille[0] + 2, 1):
        for j in range(0, taille[1] + 2, 1):
            if (i == 0 or j == 0 or i == taille[0] + 1 or j == taille[1] + 1) or (
                i == 1 and j == 1
            ):
                matrice[i][j] = 1
            else:
                matrice[i][j] = 0
    return matrice


def verif_manhatan_dist(coord, point, etape, etape_point):
    dist = abs(coord[0] - int(point[0])) + abs(coord[1] - int(point[1]))
    # print("dist", dist)
    # print("nb_etapes-restantes", int(etape_point)-etape)
    if dist > (int(etape_point) - etape):
        return False
    else:
        return True


def verification_entoure(matrice):
    ##on regarde en fonction de la case 1, il doit toujours avoir la possibilité de ralier la case un en plus

    first = True
    visite = np.zeros_like(matrice)
    voisins = [(1, 0), (0, -1), (0, 1), (-1, 0)]
    nouveaux_voisins = []

    for i, j in voisins:
        case_x = 1 + i
        case_y = 1 + j
        if matrice[case_x][case_y] == 0:
            nouveaux_voisins.append((case_x, case_y))
            visite[case_x][case_y] = 2
    ##print("nouveaux_voisins_premiere_fois", nouveaux_voisins)

    if not nouveaux_voisins:
        return False

    while nouveaux_voisins:
        x, y = nouveaux_voisins.pop(0)
        for i, j in voisins:
            case_x = x + i
            case_y = y + j
            if matrice[case_x, case_y] == 0 and visite[case_x, case_y] != 2:
                visite[case_x, case_y] = 2
                nouveaux_voisins.append((case_x, case_y))
        ##print("nouveaux_voisins", nouveaux_voisins)

    ##print(matrice)
    ##print("visite",visite)
    for i in range(1, matrice.shape[0] - 1, 1):
        for j in range(1, matrice.shape[1] - 1):
            if matrice[i][j] == 0:
                if visite[i][j] != 2:
                    return False

    return True


def creation_matrice_marquee(matrice, coor):
    new_matrice = np.empty((matrice.shape[0], matrice.shape[1]))
    for i in range(0, matrice.shape[0], 1):
        for j in range(0, matrice.shape[1], 1):
            if i == coor[0] and j == coor[1]:
                new_matrice[i][j] = 1
            else:
                new_matrice[i][j] = matrice[i][j]
    return new_matrice


def parcourir_voisins(liste_solution, liste_retour, etape, checkpoint, etape_actuelle):
    voisins = [(1, 0), (0, -1), (0, 1), (-1, 0)]
    nouvelle_liste_solutions = []
    # print("solution_d'entree_dans_parcourir_voisin",liste_solution)

    # voir comment mettre à jour
    coordonnees = liste_solution[len(liste_solution) - 2]
    # print("coord",coordonnees)
    matrice = liste_solution[len(liste_solution) - 1]
    ##print("matrice_au_debut", matrice)

    for i in range(0, len(voisins)):
        case_x = voisins[i][0] + coordonnees[0]
        ##print("x:",case_x)

        case_y = voisins[i][1] + coordonnees[1]
        ##print("y:",case_y)
        if matrice[case_x][case_y] == 0:
            if case_x == int(etape[0]) and case_y == int(etape[1]):
                if etape_actuelle == checkpoint:
                    # print("je suis au checkpoint")
                    new_matrice = creation_matrice_marquee(matrice, (case_x, case_y))
                    ##print(new_matrice)

                    if verification_entoure(new_matrice):
                        ##print("il n'y a pas de point bloqué")
                        ##print("avant",liste_solution)
                        liste_nouvelle_solution = liste_solution.copy()
                        liste_nouvelle_solution.pop(len(liste_solution) - 1)
                        liste_nouvelle_solution.append((case_x, case_y))
                        liste_nouvelle_solution.append(new_matrice)
                        ##print("apres",liste_nouvelle_solution)
                        liste_retour.append(liste_nouvelle_solution)
                    # else:
                    ##print("je suis bloqué")

                # else:
                ##print("je suis trop tot au checkpoint")

            else:
                if verif_manhatan_dist(
                    (case_x, case_y), etape, etape_actuelle, checkpoint
                ):
                    new_matrice = creation_matrice_marquee(matrice, (case_x, case_y))
                    ##print(new_matrice)
                    ##print("c'est encore possible pour moi")

                    if verification_entoure(matrice):
                        ##print("il n'y a pas de point bloqué")
                        ##print("avant",liste_solution)
                        liste_nouvelle_solution = liste_solution.copy()
                        liste_nouvelle_solution.pop(len(liste_solution) - 1)
                        liste_nouvelle_solution.append((case_x, case_y))
                        liste_nouvelle_solution.append(new_matrice)
                        ##print("apres",liste_nouvelle_solution)
                        liste_retour.append(liste_nouvelle_solution)
                # else:
                ##print("je suis bloqué")

                # else:
                ##print("ce n'est plus possible pour moi")

        # else:
        ##print("la case est déjà parcourue")
    ##print("fin de voisins: nouvelle_liste",liste_retour)

    return liste_retour


def chemins_possibles(liste_solutions, etapes, checkpoint, parcourir):

    indice = 0
    # print(" checkpoint, etape", checkpoint[indice],etapes[indice])
    nouvelle_liste = []
    if checkpoint[0] == 1:
        if etapes[0] != [1, 1]:
            return []
        else:
            etapes.pop(0)
            checkpoint.pop(0)
    ##on parcours en nombre d'étape
    ## quand on arrive au checkpoint on change d'étape à atteindre.
    for i in range(2, parcourir + 1):
        # print(checkpoint)
        # print("i et checkpoint, etape",i, checkpoint[indice],etapes[indice])
        if i > checkpoint[indice]:

            indice += 1
        # print("etape_chemins_possibles", i)

        nouvelle_liste = []
        for solution in liste_solutions:
            # print("solution", solution)
            new_sol = parcourir_voisins(
                solution, nouvelle_liste, etapes[indice], checkpoint[indice], i
            )
            if new_sol:
                nouvelle_liste = new_sol
        # print("nouvelle liste",nouvelle_liste)
        if not nouvelle_liste:
            return []
        liste_solutions = nouvelle_liste

        # print("liste_sol_fin_de_chemin",nouvelle_liste)

    return nouvelle_liste


def comparaison(liste_un, liste_deux):
    solutions = []

    for solution_un in liste_un:
        solution_un_copy = solution_un[:-1]
        start, end = solution_un_copy[0], solution_un_copy[-1]

        for solution_deux in liste_deux:
            solution_deux_copy = solution_deux[:-1]

            nouvelle_solution = solution_un_copy.copy()
            for element in reversed(solution_deux_copy[1:-1]):
                if element in solution_un_copy:
                    break
                nouvelle_solution.append(element)

            else:
                solutions.append(nouvelle_solution)

    return solutions


def programme_final(chemin, sortie):

    donnees = open_file(chemin)
    with open(sortie, "w") as f:
        f.close()

    print("donnees:", donnees)
    for i in range(len(donnees)):

        taille = donnees[i][0]
        ##print(taille)
        matrice = new_matrice(taille)
        ##print(matrice)
        parcourir = taille[0] * taille[1]

        etapes = donnees[i][1 : len(donnees[i])]
        checkpoint = checkpoints(taille)

        ##verifier si elle doit être modifiée
        liste_solutions = [[(1, 1), matrice]]

        checkpoint_first = checkpoint[0:2]
        print("checkpoint_first", checkpoint_first)
        checkpoint_second = [
            (parcourir - checkpoint[2] + 2),
            (parcourir - checkpoint[1] + 2),
        ]
        print("checkpoint", checkpoint_second)
        etapes_first = etapes[0:2]
        etapes_second = [etapes[2], etapes[1]]

        print("sol_first *********************")
        solution_first = chemins_possibles(
            liste_solutions, etapes_first, checkpoint_first, checkpoint_first[-1]
        )
        print("sol_sec *********************")
        solution_second = chemins_possibles(
            liste_solutions, etapes_second, checkpoint_second, checkpoint_second[-1]
        )

        solution = comparaison(solution_first, solution_second)

        print("********************solution***********************")

        nombre_sol = len(solution)

        print("return", nombre_sol, solution)
        print("fini****************************")
        with open(sortie, "a") as f:
            f.write(f"{nombre_sol} \n")


if __name__ == "__main__":
    chemin = "test.txt"
    sortie = "resultats2.txt"
    programme_final(chemin, sortie)
