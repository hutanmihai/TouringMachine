import copy


def get_part(name, lista):
    templist = []
    valid = False

    for line in lista:

        if line == name + ':':
            valid = True
            continue
        if line == 'end':
            valid = False

        if valid:
            templist.append(line)

    return templist


def validation_and_load(fisier):
    templist = []
    if len(fisier) > 1:
        file = open(fisier, 'r')
    else:
        print("Fisierul nu exista!")
        return 1, 1, 1, 1, 1, 1

    for line in file:
        line = line.strip().lower()

        if len(line) > 0:
            templist.append(line)

    tempstates = get_part('states', templist)
    sigma = get_part('sigma', templist)
    gamma = get_part('gamma', templist)
    transitions = get_part('transitions', templist)

    if len(tempstates) == 0 or len(sigma) == 0 or len(gamma) == 0 or len(transitions) == 0:
        print('Invalid!')
        return 1, 1, 1, 1, 1, 1

    start_state = []
    final_states = []
    states = []

    for state in tempstates:
        state = state.split()
        if len(state) > 1:
            if state[1] == 'final':
                final_states.append(state[0])
            elif state[1] == 'start':
                start_state.append(state[0])
        states.append(state[0])

    if len(start_state) == 0 or len(final_states) == 0:
        print('Nu exista stare de start sau final!')
        return 1, 1, 1, 1, 1, 1

    bool_transitions = True

    for transition in transitions:
        temptrans = transition.split()

        if (temptrans[0] not in states) or (temptrans[1] not in gamma) or (temptrans[2] not in states) or (temptrans[3]
                                                                                                           not in gamma) or (
                temptrans[4] not in ['l', 'r']):
            bool_transitions = False
            print('Tranzitiile nu sunt corecte!')
            return 1, 1, 1, 1, 1, 1

    if bool_transitions:
        return states, sigma, gamma, transitions, start_state, final_states


def simulator(user_input, start_state, final_states, transitions):
    accept = final_states[0]
    reject = final_states[1]
    current = start_state[0]
    tape1 = [x for x in user_input]
    tape1.append('_')
    tape2 = copy.deepcopy(tape1)

    for x in user_input:
        if x not in sigma:
            print('Input gresit! Caractere care nu sunt in Sigma!')
            return

    if tape1.count('#') == 0:
        print('Rejected!')
        return
    i = 0

    while (current != accept) and (current != reject):
        for transition in transitions:
            transition = transition.split()
            if transition[0] == current:
                if tape1[i] == transition[1]:
                    current = transition[2]
                    tape1[i] = transition[3]
                    tape2[i] = transition[3]
                    if transition[4] == 'l' and i != 0:
                        i -= 1
                    elif transition[4] == 'r' and i < len(tape1):
                        i += 1

    if tape1 != tape2:
        print('Error occured!')
    else:
        if current == accept:
            print('Accepted!')
            return
        elif current == reject:
            print('Rejected')
            return


# main

states, sigma, gamma, transitions, start_state, final_states = validation_and_load('config_file_2.txt')
if [states, sigma, gamma, transitions, start_state, final_states] != [1, 1, 1, 1, 1, 1]:
    user_input = input("INPUT: ")
    simulator(user_input, start_state, final_states, transitions)

# valid {0,1} -> w#w
# invalid input din afara alf

# TODO adaugam 2 tapes, check for integrity of tapes (if they are identical)
