import numpy as np

# Lire les données depuis le fichier data3.txt
def lire_donnees(fichier):
    with open(fichier, 'r') as f:
        lignes = f.readlines()
    
    nb_localisations = int(lignes[0].split()[1])
    nb_ressources = int(lignes[1].split()[1])
    nb_machines = int(lignes[2].split()[1])
    nb_processus = int(lignes[3].split()[1])
    nb_services = int(lignes[4].split()[1])

    machines = []
    index = 7
    for _ in range(nb_machines):
        machines.append(list(map(int, lignes[index].split()[1:])))
        index += 1

    services = list(map(int, lignes[index:index + nb_services]))
    index += nb_services + 1

    processus = []
    for _ in range(nb_processus):
        processus.append(list(map(int, lignes[index].split()[1:])))
        index += 1
    
    return nb_localisations, nb_ressources, nb_machines, nb_processus, nb_services, machines, services, processus

# Fonction d'affectation initiale
def affectation_initiale(machines, processus, nb_processus, nb_machines):
    affectations = np.full(nb_processus, -1)
    for p in range(nb_processus):
        for m in range(nb_machines):
            if np.all(machines[m] >= processus[p, 1:]):  # Vérification des capacités
                affectations[p] = m
                machines[m] -= processus[p, 1:]
                break
    return affectations

# Calcul du score
def calculer_score(machines, processus, affectations, nb_machines, nb_ressources):
    score = 0
    for m in range(nb_machines):
        utilisation = np.zeros(nb_ressources)
        for p in range(len(affectations)):
            if affectations[p] == m:
                utilisation += processus[p, 1:]
        dépassement = np.maximum(utilisation - machines[m], 0)
        score += np.sum(dépassement)
    return score

# Optimisation par recherche locale
def recherche_locale(machines, processus, affectations, nb_machines, nb_ressources):
    meilleur_score = calculer_score(machines, processus, affectations, nb_machines, nb_ressources)
    meilleure_affectation = affectations.copy()
    
    amelioration = True
    while amelioration:
        amelioration = False
        for p in range(len(affectations)):
            machine_origine = affectations[p]
            for m in range(nb_machines):
                if m != machine_origine and np.all(machines[m] >= processus[p, 1:]):
                    nouvelle_affectation = affectations.copy()
                    nouvelle_affectation[p] = m
                    nouveau_score = calculer_score(machines, processus, nouvelle_affectation, nb_machines, nb_ressources)
                    if nouveau_score < meilleur_score:
                        meilleur_score = nouveau_score
                        meilleure_affectation = nouvelle_affectation
                        amelioration = True
                        break
            if amelioration:
                break
    
    return meilleure_affectation, meilleur_score

# Main function
def main():
    fichier = 'data3.txt'
    nb_localisations, nb_ressources, nb_machines, nb_processus, nb_services, machines, services, processus = lire_donnees(fichier)
    
    # Affection initiale
    affectations = affectation_initiale(machines.copy(), processus, nb_processus, nb_machines)
    
    # Optimisation
    meilleure_affectation, meilleur_score = recherche_locale(machines.copy(), processus, affectations, nb_machines, nb_ressources)
    
    print(f"Score initial: {calculer_score(machines.copy(), processus, affectations, nb_machines, nb_ressources)}")
    print(f"Meilleur score après optimisation: {meilleur_score}")
    if meilleur_score < 13000:
        print("Objectif atteint avec succès.")
    else:
        print("Objectif non atteint, essayez d'autres méthodes d'optimisation.")

main()
