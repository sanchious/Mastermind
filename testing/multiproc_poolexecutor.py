import functools
import itertools
import multiprocessing
import time
from concurrent.futures import ProcessPoolExecutor


def compare_response(my_guess, possible_solution):
    response_score = [0, 0]
    for x, y in zip(my_guess, possible_solution):
        if x == y:
            response_score[0] += 1
            response_score[1] += 1
        elif y in my_guess:
            response_score[0] += 1
    return response_score


# Function to filter only the possible combinations to be used in next guess
def curated(args):
    guess, score, attack_list = args
    curated_list = []
    for i in range(len(attack_list)):
        if compare_response(guess, attack_list[i]) == score:
            curated_list.append(attack_list[i])
    return curated_list


def multi_proc(num_cores, attack_list, guess, response):
    print("Starting multiprocessing...")
    print(f"The length of the list being processed is: {len(attack_list):_}")
    print(
        f"The length of the sublists being processed is: {len(attack_list[0]):_}")

    with ProcessPoolExecutor(max_workers=num_cores) as executor:
        curated_args = [(guess, response, sublist) for sublist in attack_list]
        result = executor.map(curated, curated_args)

    unified_list = [s for sublist in result for s in sublist]  # flatten list

    print(f"Flattened list length: {len(unified_list):_}")
    return unified_list


if __name__ == '__main__':

    ###########################################################################
    # # Test 1 with fewer attack combinations
    # num_Gladiators = 4
    # num_Weapons = 6

    # Test 2 with many attack combinations (cpu intensive - slow)
    num_Gladiators = 6
    num_Weapons = 25

    # num_cores = multiprocessing.cpu_count()
    num_cores = 5
    divide_factor = 5

    # weapons_list = list(range(num_Weapons))
    print("The list of weapons: ", list(range(num_Weapons)))

    # Generate all unique combinations of the attack guesses
    print("Creating attack combinations with the number of Gladiators = %s and the number of Weapons = %s. Based on the level response." %
          (num_Gladiators, num_Weapons))
    attack_combinations = list(
        itertools.permutations(list(range(num_Weapons)), num_Gladiators))

    # print("Available attack combinations are: ", attack_combinations)
    print(f"Number of possible attacks: {len(attack_combinations):_}")

    # # Test 1 with fewer attack combinations
    # my_guess = [0, 4, 5, 3]
    # actual_solution = (0, 5, 2, 7)

    # Test 2 with many attack combinations (cpu intensive - slow)
    my_guess = [0, 4, 5, 3, 10, 20]
    actual_solution = (0, 5, 2, 7, 15, 19)

    print(
        f"The response would be: {compare_response(my_guess, actual_solution)}")
    response = compare_response(my_guess, actual_solution)

    # Divide the attack_combinations list into a number of sublist based on the number of cores available
    divided_attack_combinations = [list(attack_combinations)[i::num_cores]
                                   for i in range(num_cores)]

    print(
        f"The length of the divided list is: {len(divided_attack_combinations)}")
    print(f"The lenght of sublist is: {len(divided_attack_combinations[0]):_}")
    # print(divided_attack_combinations)

###########################################################################

    # master_list = []
    # start_time = time.time()
    # result = multi_proc(
    #     num_cores, divided_attack_combinations, my_guess, response)
    # master_list.append(result)
    # end_time = time.time()
    # total_time = end_time - start_time
    # master_list = [s for sublist in master_list for s in sublist]
    # print(f"It took {total_time:.2f} seconds to finish multiprocessing.")
    # print(f"Flattened master list lenght: {len(master_list):_}")

###########################################################################
    master_list = []
    for x in range(num_cores):
        print(f"Starting iteration {x+1}/{num_cores}")
        print(f"Creating more_divided_attack_combinations...")
        start_time = time.time()
        more_divided_attack_combinations = [list(divided_attack_combinations[x])[
            i::divide_factor]for i in range(divide_factor)]

        result = multi_proc(
            num_cores, more_divided_attack_combinations, my_guess, response)
        master_list.append(result)

        end_time = time.time()
        total_time = end_time - start_time
        print(
            f"It took {total_time:.2f} seconds to finish iteration {x+1}/{num_cores}")
    master_list = [s for sublist in master_list for s in sublist]
    print(f"Flattened master list lenght: {len(master_list):_}")
    # print(master_list)


# Number of possible attacks: 127_512_000
# Flattened master list lenght: 11_162_880
