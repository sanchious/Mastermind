# SuperFastPython.com
# example of multiple arguments with pool.apply_async
import time
from random import random
import multiprocessing
import itertools

# task function executed in a child worker process


def task(arg1, arg2, arg3):
    # block for a moment
    time.sleep(random())
    # report values
    print(f'Task {arg1}, {arg2}, {arg3}.', flush=True)
    # return a result
    return arg1 + arg2 + arg3


def compare_response(my_guess, possible_solution):
    response_score = [0, 0]
    for x, y in zip(my_guess, possible_solution):
        if x == y:
            response_score[0] += 1
            response_score[1] += 1
        elif y in my_guess:
            response_score[0] += 1
    return response_score


def curated(attack_list, guess, score):
    curated_list = []
    for i in range(len(attack_list)):
        if compare_response(guess, attack_list[i]) == score:
            curated_list.append(attack_list[i])
    return curated_list
    # q.put(curated_list)


def curated_sublist(attack_list_of_lists, guess, score):
    curated_list = []
    for i in range(len(attack_list_of_lists)):
        for j in range(len(attack_list_of_lists[i])):
            if compare_response(guess, attack_list_of_lists[i][j]) == score:
                curated_list.append(attack_list_of_lists[i][j])
    return curated_list


# protect the entry point
if __name__ == '__main__':
    ###########################################################################
    num_Gladiators = 6
    num_Weapons = 25
    # num_cores = multiprocessing.cpu_count()
    num_cores = 10

    # weapons_list = list(range(num_Weapons))
    print("The list of weapons: ", list(range(num_Weapons)))

    # Generate all unique combinations of the attack guesses
    print("Creating attack combinations with the number of Gladiators = %s and the number of Weapons = %s. Based on the level response." %
          (num_Gladiators, num_Weapons))
    attack_combinations = list(
        itertools.permutations(list(range(num_Weapons)), num_Gladiators))

    # print("Available attack combinations are: ", attack_combinations)
    print(f"Number of possible attacks: {len(attack_combinations):_}")

    my_guess = [0, 4, 5, 3, 10, 20]
    actual_solution = (0, 5, 2, 7, 15, 19)
    response = [2, 1]

    # my_guess = [0, 4, 5, 3]
    # actual_solution = (0, 5, 2, 7)
    # response = [2, 1]

    print(compare_response(my_guess, actual_solution))

    # Divide the attack_combinations list into a number of sublist based on the number of cores available
    divided_attack_combinations = []
    for i in range(num_cores):
        sublist = list(attack_combinations)[i::num_cores]
        divided_attack_combinations.append(sublist)

    print(len(divided_attack_combinations))


###########################################################################
    start_time = time.monotonic()
    # create the process pool
    with multiprocessing.Pool() as pool:
        # issue multiple tasks each with multiple arguments
        async_results = [pool.apply_async(
            curated, args=(divided_attack_combinations[i], my_guess, response)) for i in range(num_cores)]
        # retrieve the return value results
        results = [ar.get() for ar in async_results]

    print(len(results))
    end_time = time.monotonic()
    print(f"Completed in {(end_time - start_time):.2f} seconds.")

    flat_list = []
    for i in results:
        for j in i:
            flat_list.append(i)

    print(f"Flatten list lenght: {len(flat_list):_}")
