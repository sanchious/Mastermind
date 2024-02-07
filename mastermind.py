import requests
import json
import sys
import itertools
import functools
import multiprocessing
import time
import random


# Compare all attack combinations against a "guess" which returns a response score
def compare_response(my_guess, possible_solution):
    response_score = [0, 0]
    for x, y in zip(my_guess, possible_solution):
        if x == y:
            response_score[0] += 1
            response_score[1] += 1
        elif y in my_guess:
            response_score[0] += 1
    return response_score


# Loop through the attack list and return filtered list of possible solutions for the next guess
def curated(guess, score, attack_list):
    curated_list = []
    for i in range(len(attack_list)):
        if compare_response(guess, attack_list[i]) == score:
            curated_list.append(attack_list[i])
    return curated_list


# Partial function to be used for multiprocessing, takes only static arguments (except the iterable argument)
def partial_function(input_function, first_arg, second_arg):
    partial_function = functools.partial(input_function, first_arg, second_arg)
    return partial_function


def multi_proc(num_cores, attack_list):
    # print(f"Starting multiprocessing...")
    print(
        f"The length of the list being processed is: {len(attack_list):_}")
    print(
        f"The length of the sublists being processed is: {len(attack_list[0]):_}")
    pool = multiprocessing.Pool(processes=num_cores)
    # start_time = time.time()
    result = pool.map_async(partial_function(
        curated, my_guess, score), attack_list)
    result = result.get(30)
    pool.close()
    pool.join()

    # end_time = time.time()
    # run_time = end_time - start_time
    # print(f"Multiprocessing finished in {run_time:.2f} seconds")

    unified_list = [s for sublist in result for s in sublist]

    print(f"Unified list lenght: {len(unified_list):_}")
    # print(f"Unified_list list: \n {unified_list}")
    return unified_list


if __name__ == '__main__':

    if sys.version_info < (3, 0):
        sys.exit('Python version < 3.0 does not support modern TLS versions. You will have trouble connecting to our API using Python 2.X.')

    email = 'mastermind@praetorian.com'  # Change this!
    level = 1
    # num_cores = multiprocessing.cpu_count() + 1
    num_cores = 5
    # divide_factor = 10

    if level == 4:
        # Generate all unique combinations of the attack guesses for level 4 (hard coded)
        print("Creating attack combinations for level 4 with number of Gladiators = %s and number of Weapons = %s. Based on the level response." %
              (6, 25))
        attack_combinations4 = list(
            itertools.permutations(list(range(25)), 6))

        # Creating divided_attack_combination for level 4 (hard-coded)
        print("Creating the divided attack combination for level 4")
        divided_attack_combinations4 = [
            list(attack_combinations4)[i::num_cores]for i in range(num_cores)]
        print(
            f"The length of the divided list for level 4 is: {len(divided_attack_combinations4)}")
        print(
            f"The lenght of sublist for level 4 is: {len(divided_attack_combinations4[0]):_}")

    # Get the 'Auth-Token'
    req_auth = requests.post(
        'https://mastermind.praetorian.com/api-auth-token/', data={'email': email})
    print(req_auth.json())
    # > {'Auth-Token': 'AUTH_TOKEN'}

    headers = req_auth.json()
    headers['Content-Type'] = 'application/json'
    print(headers)

    # # Reseting the game
    req_reset = requests.post(
        'https://mastermind.praetorian.com/reset/', headers=headers)
    print(req_reset.json())

    # Interacting with the game. Get the level info
    req_level = requests.get(
        'https://mastermind.praetorian.com/level/{0}/'.format(level), headers=headers)
    print(f"This is level {level}")
    print(req_level.json())
    # > {'numGladiators': 4, 'numGuesses': 8, 'numRounds': 1, 'numWeapons': 6}
    num_Gladiators = req_level.json()['numGladiators']
    num_Weapons = req_level.json()['numWeapons']

    # weapons_list = list(range(num_Weapons))
    print("The list of weapons: ", list(range(num_Weapons)))

    # Generate all unique combinations of the attack guesses
    if level == 4:
        attack_combinations = attack_combinations4
        my_guess = random.choice(attack_combinations)
        divided_attack_combinations = divided_attack_combinations4
    else:
        print("Creating attack combinations with number of Gladiators = %s and number of Weapons = %s. Based on the level response." %
              (num_Gladiators, num_Weapons))
        attack_combinations = list(
            itertools.permutations(list(range(num_Weapons)), num_Gladiators))
        my_guess = random.choice(attack_combinations)

    # Convert "attack_combinations" tuples to a nested list
    # attack_combinations = [list(t) for t in attack_combinations]

    # print("Available attack combinations are: ", attack_combinations)
    # print(f"Number of possible attacks: {len(attack_combinations)}")

    curated_attack_combinations = []
    attack_counter = 1

    # Divide the attack_combinations list into a number of sublist based on the number of cores available
    # divided_attack_combinations = [list(attack_combinations)[i::num_cores]
    #                                for i in range(num_cores)]

    run = True

    while run:
        if len(attack_combinations) > 100_000_000:
            print(f"Possible attack combinations more than 100 mio...")
            master_list = []
            for x in range(num_cores):

                print(f'=====>Sending attack nr.{attack_counter}: {my_guess}')
                print(
                    f"Number of possible attacks: {len(divided_attack_combinations[x]):_}")
                req_attack = requests.post('https://mastermind.praetorian.com/level/{0}/'.format(level),
                                           data=json.dumps({'guess': my_guess}), headers=headers)
                req_response = req_attack.json()
                print(req_response)
                score = [0, 0]

                if req_response == {'error': 'Guess took too long, please restart game.'}:
                    print("Guess took too long, please restart game.")
                    run = False
                    break

                elif req_response == {'message': 'Onto the next level'}:
                    print(f"You got the correct combination {my_guess}")
                    break

                elif req_response == {'response': [0, 0]}:
                    attack_counter += 1
                    my_guess = random.choice(attack_combinations)
                    pass

                else:
                    score = req_response['response']
                    print(f"The score is: {score}")
                    # > {'response': [2, 1]}
                    print(
                        f"Starting multiprocessing iteration {x+1}/{num_cores}")
                    start_time = time.time()
                    more_divided_attack_combinations = [list(divided_attack_combinations[x])[
                        i::num_cores]for i in range(num_cores)]
                    result = multi_proc(
                        num_cores, more_divided_attack_combinations)
                    end_time = time.time()
                    total_time = end_time - start_time
                    master_list.append(result)
                    print(
                        f"Multiprocessing for iteration {x+1}/{num_cores} took {total_time:.2f} seconds.")
                    if score in [[1, 0], [2, 0], [2, 1]]:
                        my_guess = random.choice(master_list[-1])
                    print(f"The next guess is: {my_guess}")
                    attack_counter += 1
            if run == False:
                break
            master_list = [s for sublist in master_list for s in sublist]
            print(f"Unified Master list length: {len(master_list):_}")

            attack_combinations = master_list
            my_guess = random.choice(attack_combinations)
            print(f"Next guess will be: {my_guess}")
            curated_attack_combinations = []

        elif len(attack_combinations) > 3_000_000:
            print(f"Possible attack combinations more than 10 mio...")
            req_attack = requests.post('https://mastermind.praetorian.com/level/{0}/'.format(level),
                                       data=json.dumps({'guess': my_guess}), headers=headers)
            print(f'=====>Sending attack nr.{attack_counter}: {my_guess}')
            print(f"Number of possible attacks: {len(attack_combinations):_}")
            req_response = req_attack.json()
            print(req_response)
            score = [0, 0]
            if req_response == {'error': 'Guess took too long, please restart game.'}:
                print("Guess took too long, please restart game.")
                break

            elif req_response == {'message': 'Onto the next level'}:
                print(f"You got the correct combination {my_guess}")
                level += 1
                attack_counter = 0

                # Generate all unique combinations of the attack guesses
                if level == 4:
                    attack_combinations = attack_combinations4
                    my_guess = random.choice(attack_combinations)
                    divided_attack_combinations = divided_attack_combinations4
                else:
                    req_level = requests.get(
                        'https://mastermind.praetorian.com/level/{0}/'.format(level), headers=headers)
                    print(f"This is level {level}")
                    print(req_level.json())
                    # > {'numGladiators': 4, 'numGuesses': 8, 'numRounds': 1, 'numWeapons': 6}
                    num_Gladiators = req_level.json()['numGladiators']
                    num_Weapons = req_level.json()['numWeapons']

                    # weapons_list = list(range(num_Weapons))
                    print("The list of weapons: ", list(range(num_Weapons)))
                    print("Creating attack combinations with number of Gladiators = %s and number of Weapons = %s. Based on the level response." %
                          (num_Gladiators, num_Weapons))
                    attack_combinations = list(
                        itertools.permutations(list(range(num_Weapons)), num_Gladiators))
                    my_guess = random.choice(attack_combinations)

            elif req_response == {'response': [0, 0]}:
                attack_counter += 1
                my_guess = random.choice(attack_combinations)

            else:
                master_list = []
                score = req_response['response']
                print(f"The score is: {score}")
                # > {'response': [2, 1]}
                start_time = time.time()
                divided_attack_combinations = [list(attack_combinations)[
                    i::num_cores]for i in range(num_cores)]
                result = multi_proc(
                    num_cores, divided_attack_combinations)
                end_time = time.time()
                total_time = end_time - start_time
                master_list.append(result)
                print(
                    f"Multiprocessing for attack nr.{attack_counter} took {total_time:.2f} seconds.")
                my_guess = random.choice(attack_combinations)
                print(f"The next guess is: {my_guess}")
                attack_counter += 1
                master_list = [s for sublist in master_list for s in sublist]
                print(f"Unified Master list length: {len(master_list):_}")

                attack_combinations = master_list
                my_guess = random.choice(attack_combinations)
                print(f"Next guess will be: {my_guess}")
                curated_attack_combinations = []

        else:
            req_attack = requests.post('https://mastermind.praetorian.com/level/{0}/'.format(level),
                                       data=json.dumps({'guess': my_guess}), headers=headers)
            print(f'=====>Sending attack nr.{attack_counter}: {my_guess}')
            print(f"Number of possible attacks: {len(attack_combinations):_}")
            req_response = req_attack.json()
            print(req_response)
            score = [0, 0]
            if req_response == {'error': 'Guess took too long, please restart game.'}:
                print("Guess took too long, please restart game.")
                break

            elif req_response == {'message': 'Onto the next level'}:
                print(f"You got the correct combination {my_guess}")
                level += 1
                attack_counter = 0

                # Generate all unique combinations of the attack guesses
                if level == 4:
                    # Generate all unique combinations of the attack guesses for level 4 (hard coded)
                    print("Creating attack combinations for level 4 with number of Gladiators = %s and number of Weapons = %s. Based on the level response." %
                          (6, 25))
                    attack_combinations4 = list(
                        itertools.permutations(list(range(25)), 6))

                    # Creating divided_attack_combination for level 4 (hard-coded)
                    print("Creating the divided attack combination for level 4")
                    divided_attack_combinations4 = [
                        list(attack_combinations4)[i::num_cores]for i in range(num_cores)]
                    print(
                        f"The length of the divided list for level 4 is: {len(divided_attack_combinations4)}")
                    print(
                        f"The lenght of sublist for level 4 is: {len(divided_attack_combinations4[0]):_}")

                    attack_combinations = attack_combinations4
                    my_guess = random.choice(attack_combinations)
                    divided_attack_combinations = divided_attack_combinations4

                    req_level = requests.get(
                        'https://mastermind.praetorian.com/level/{0}/'.format(level), headers=headers)
                    print(f"This is level {level}")
                    print(req_level.json())
                    # > {'numGladiators': 4, 'numGuesses': 8, 'numRounds': 1, 'numWeapons': 6}
                    num_Gladiators = req_level.json()['numGladiators']
                    num_Weapons = req_level.json()['numWeapons']

                    # weapons_list = list(range(num_Weapons))
                    print("The list of weapons: ", list(range(num_Weapons)))

                else:
                    req_level = requests.get(
                        'https://mastermind.praetorian.com/level/{0}/'.format(level), headers=headers)
                    print(f"This is level {level}")
                    print(req_level.json())
                    # > {'numGladiators': 4, 'numGuesses': 8, 'numRounds': 1, 'numWeapons': 6}
                    num_Gladiators = req_level.json()['numGladiators']
                    num_Weapons = req_level.json()['numWeapons']

                    # weapons_list = list(range(num_Weapons))
                    print("The list of weapons: ", list(range(num_Weapons)))
                    print("Creating attack combinations with number of Gladiators = %s and number of Weapons = %s. Based on the level response." %
                          (num_Gladiators, num_Weapons))
                    attack_combinations = list(
                        itertools.permutations(list(range(num_Weapons)), num_Gladiators))
                    my_guess = random.choice(attack_combinations)

            elif req_response == {'response': [0, 0]}:
                attack_counter += 1
                my_guess = random.choice(attack_combinations)

            elif 'roundsLeft' in req_response:
                print(req_response)
                print("Need to restart the round...")
                req_level = requests.get(
                    'https://mastermind.praetorian.com/level/{0}/'.format(level), headers=headers)
                print(f"This is level {level}")
                print(req_level.json())
                # > {'numGladiators': 4, 'numGuesses': 8, 'numRounds': 1, 'numWeapons': 6}
                num_Gladiators = req_level.json()['numGladiators']
                num_Weapons = req_level.json()['numWeapons']
                print("Creating attack combinations with number of Gladiators = %s and number of Weapons = %s. Based on the level response." %
                      (num_Gladiators, num_Weapons))
                attack_combinations = list(
                    itertools.permutations(list(range(num_Weapons)), num_Gladiators))
                my_guess = random.choice(attack_combinations)

            elif 'hash' in req_response:
                print(req_response)
                req_hash = requests.get(
                    'https://mastermind.praetorian.com/hash/', headers=headers)
                print(req_hash)
                break

            else:
                score = req_response['response']
                print(f"The score is: {score}")
                # > {'response': [2, 1]}

                curated_attack_combinations = curated(
                    my_guess, score, attack_combinations)

                # for i in range(len(attack_combinations)):
                #     # print(
                #     #     f"comparing my_guess: {my_guess} against possible solution {attack_combinations[i]}")
                #     # if my_guess == attack_combinations[i]:
                #     #     pass
                #     if compare_response(my_guess, attack_combinations[i]) == score:
                #         # print(
                #         #     f"Looks like compare response: {compare_response(my_guess, attack_combinations[i])} is the same as initial response: {response}")
                #         curated_attack_combinations.append(attack_combinations[i])

                # print(curated_attack_combinations)
                attack_combinations = curated_attack_combinations
                my_guess = random.choice(curated_attack_combinations)
                curated_attack_combinations = []
                attack_counter += 1