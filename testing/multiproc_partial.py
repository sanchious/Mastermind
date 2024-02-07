import functools
import itertools
import multiprocessing
import time


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
def curated(guess, score, attack_list):
    curated_list = []
    for i in range(len(attack_list)):
        if compare_response(guess, attack_list[i]) == score:
            # print(
            #     f"Comparing guess: {guess} with attack_list index {attack_list[i]}. Compare_response = {compare_response(guess, attack_list[i])} and score = {score}")
            curated_list.append(attack_list[i])
    return curated_list


# Alternative curated function - delete from the whole list approach (slow)
def curated_alt(guess, score, attack_list, tries=10000000):
    curated_list = list(attack_list)
    counter = 0
    index = 0
    for i in range(len(attack_list)):
        counter += 1
        if compare_response(guess, attack_list[i]) != score:
            del curated_list[index]
            index -= 1
        if counter > tries:
            break
        index += 1
    return curated_list


def curated_alt_wrapper(guess, score, attack_list, tries):
    return curated_alt(guess, score, tries, attack_list)


def partial_function(input_function, first_arg, second_arg):
    partial_function = functools.partial(input_function, first_arg, second_arg)
    return partial_function


def multi_proc(num_cores, attack_list):
    print(f"Starting multiprocessing...")
    print(
        f"The length of the list being processed is: {len(attack_list):_}")
    print(
        f"The length of the sublists being processed is: {len(attack_list[0]):_}")
    pool = multiprocessing.Pool(processes=num_cores)
    start_time = time.time()
    result = pool.map_async(partial_function(
        curated, my_guess, response), attack_list)
    result = result.get(10)
    pool.close()
    pool.join()

    end_time = time.time()
    run_time = end_time - start_time
    print(f"Multiprocessing finished in {run_time:.2f} seconds")

    unified_list = [s for sublist in result for s in sublist]  # flatten list

    print(f"Flattened list lenght: {len(unified_list):_}")
    # print(f"Unified_list list: \n {flat_list}")
    return unified_list


if __name__ == '__main__':

    ###########################################################################
    # Test 1 with fewer attack combinations
    num_Gladiators = 4
    num_Weapons = 6

    # # Test 2 with many attack combinations (cpu intensive - slow)
    # num_Gladiators = 6
    # num_Weapons = 25

    num_cores = multiprocessing.cpu_count()
    # num_cores = 10
    # division_factor = 8

    # weapons_list = list(range(num_Weapons))
    print("The list of weapons: ", list(range(num_Weapons)))

    # Generate all unique combinations of the attack guesses
    print("Creating attack combinations with the number of Gladiators = %s and the number of Weapons = %s. Based on the level response." %
          (num_Gladiators, num_Weapons))
    attack_combinations = list(
        itertools.permutations(list(range(num_Weapons)), num_Gladiators))

    # print("Available attack combinations are: ", attack_combinations)
    print(f"Number of possible attacks: {len(attack_combinations):_}")

    # Test 1 with fewer attack combinations
    my_guess = [0, 4, 5, 3]
    actual_solution = (0, 5, 2, 7)

    # # Test 2 with many attack combinations (cpu intensive - slow)
    # my_guess = [0, 4, 5, 3, 10, 20]
    # actual_solution = (0, 5, 2, 7, 15, 19)

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

    # partial_function = functools.partial(
    #     curated, my_guess, response)

    # print(f"Starting multiprocessing...")
    # pool = multiprocessing.Pool(processes=num_cores)
    # start_time = time.time()
    # result = pool.map_async(partial_function(
    #     curated, my_guess, response), divided_attack_combinations)
    # result = result.get(300)
    # pool.close()
    # pool.join()

    # end_time = time.time()
    # run_time = end_time - start_time
    # print(f"Multiprocessing finished in {run_time:.2f} seconds")

    # flat_list = [s for sublist in result for s in sublist]  # flatten list

    # print(f"Flatten list lenght: {len(flat_list):_}")
    # # print(f"Flatten list: \n {flat_list}")

    master_list = []
    for x in range(num_cores):
        print(f"Starting iteration {x+1}/{num_cores}")
        print(f"Creating more_divided_attack_combinations...")
        start_time = time.time()
        more_divided_attack_combinations = [list(divided_attack_combinations[x])[
            i::num_cores]for i in range(num_cores)]

        result = multi_proc(num_cores, more_divided_attack_combinations)
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
