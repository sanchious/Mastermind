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


def curated(attack_list, guess, score, q):
    curated_list = []
    for i in range(len(attack_list)):
        if compare_response(guess, attack_list[i]) == score:
            curated_list.append(attack_list[i])
    # return curated_list
    q.put(curated_list)


def curated_sublist(attack_list_of_lists, guess, score):
    curated_list = []
    for i in range(len(attack_list_of_lists)):
        for j in range(len(attack_list_of_lists[i])):
            if compare_response(guess, attack_list_of_lists[i][j]) == score:
                curated_list.append(attack_list_of_lists[i][j])
    return curated_list


def sqr(x, y, z, q):
    q.put(x * y * z)


if __name__ == '__main__':
    ###########################################################################
    num_Gladiators = 6
    num_Weapons = 25
    # num_cores = multiprocessing.cpu_count()
    num_cores = 1

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

    q = multiprocessing.Queue()
    # y = 2
    # z = 3
    processes = [multiprocessing.Process(target=curated, args=(divided_attack_combinations[i], my_guess, response, q))
                 for i in range(num_cores)]

    for p in processes:
        p.start()

    time.sleep(1)

    for p in processes:
        p.join()

    result = [q.get() for p in processes]

    # print(result)
    print(len(result))

    flat_list = []
    for i in result:
        for j in i:
            flat_list.append(i)

    print(f"Flatten list lenght: {len(flat_list):_}")
