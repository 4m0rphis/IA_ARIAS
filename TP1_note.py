def initial():
    return [1, 1, 1, 0, 0, 0, 0] # hard coded initial state for this specific instance of the problem (base case)

def final(state):
    return state == [0, 0, 0, 0, 1, 1, 1] # the final result we're supposed to get

def actions(): # we have 3 different actions for this problem
    return [glisser, sauterUne, sauterDeux]

def glisser(state):
    possibleActions = []
    for i in range(len(state) - 1):
        if state[i] == 0 or state[i + 1] == 0:
            nextState = list(state)
            nextState[i] = (state[i] + 1) % 2  # Case noire à blanche
            nextState[i + 1] = (state[i + 1] + 1) % 2  # Inverse
            possibleActions.append(nextState)
    return possibleActions

def sauterUne(state):
    possibleActions = []
    for i in range(len(state) - 2): # on regarde 2 case avant pour éviter out of bounds
        if state[i] == 0 or state[i + 2] == 0: 
            nextState = list(state)
            nextState[i] = (state[i] + 1) % 2
            nextState[i + 2] = (state[i + 2] + 1) % 2
            possibleActions.append(nextState)
    return possibleActions

def sauterDeux(state):
    possibleActions = []
    for i in range(len(state) - 3): # 3 cases
        if state[i] == 0 or state[i + 3] == 0:
            nextState = list(state)
            nextState[i] = (state[i] + 1) % 2
            nextState[i + 3] = (state[i + 3] + 1) % 2
            possibleActions.append(nextState)
    return possibleActions

def possibleActions(noeud): # génerer la liste des transitions en prenant compte de minimiser notre heurisitque
    ls = []
    for action in actions():
        listSuiv = action(get_state(noeud))
        for etatSuiv in listSuiv:
            if not deja_vu(etatSuiv, get_path(noeud)):
                chemSuiv = list(get_path(noeud))
                chemSuiv.append(noeud)
                # Determine the action cost
                if action == glisser:
                    cout_constant = 1
                elif action == sauterUne or action == sauterDeux:
                    cout_constant = 2
                # (etatSuiv, cheminSuiv, coût cumulatif, heuristique)
                ls.append((etatSuiv, chemSuiv, get_cost(noeud) + cout_constant, heuristic(etatSuiv)))
    return ls

def deja_vu(etat,chemin): # make sure we dont loop
    for noeud in chemin:
        if etat == get_state(noeud):
            return True
    return False

def afficher_sol(noeud): # printing the solution
    print("Solution :")
    chemin = get_path(noeud)
    for i in chemin:
        print(get_state(i))
    print(get_state(noeud))
    print("Longueur : "+str(len(chemin)+1))


class Node: # unused
    def __init__(self, state, path, cost, estimated_cost):
        self.state = state
        self.path = path
        self.cost = cost
        self.estimated_cost = estimated_cost

def get_state(node):
    return node[0]

def get_path(node):
    return node[1]

def get_cost(node):
    return node[2]

def get_estimated_cost(node):
    return node.estimated_cost

def heuristic(state): # cette heuristique calcule le nombre de 1 mal placées 
    #le nombre de 1 a gauche est exactement le nombre de transitions min a faire
    misplaced_count = 0
    n = len(state) # n = len(state) // 2 si on est sur d'avoir toujours le coté droit avec que des 0
    

    # Count how many `1`s are misplaced
    for i in range(n):
        if state[i] == 1:
            # count how many `1`s are in positions that should be `0`
            # in onther words until we reach the first `0`
            if i < n - state.count(1):  # Check if it's before the last `0` position
                misplaced_count += 1

    return misplaced_count

def astar(listeAtt):
    while listeAtt:
        # Sort the list based on total cost f(n) = g(n) + h(n)
        listeAtt.sort(key=lambda elt: elt[2] + elt[3])  # slow but simple
        noeud = listeAtt.pop(0)  # Take the first element
        if final(get_state(noeud)):
            afficher_sol(noeud)
            return True
        # Generate child nodes with their cost and heuristic
        listSuiv = possibleActions(noeud)
        # Add children to the waiting list
        listeAtt.extend(listSuiv)
    return False

# Start the A* algorithm
astar([([initial(),[],0,heuristic(initial())])])
