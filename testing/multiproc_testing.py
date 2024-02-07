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


def worker(result_queue, attack_list, guess, score, start, end):
    local_result = []
    for i in range(start, end):
        if compare_response(guess, attack_list[i]) == score:
            local_result.append(attack_list[i])
    result_queue.put(local_result)


def curated_parallel(attack_list, guess, score):
    result_queue = multiprocessing.Queue()
    processes = []
    chunk_size = len(attack_list) // num_cores
    for i in range(num_cores):
        start = i * chunk_size
        end = (i + 1) * chunk_size if i != num_cores - 1 else len(attack_list)
        process = multiprocessing.Process(target=worker, args=(
            result_queue, attack_list, guess, score, start, end))
        processes.append(process)

    for process in processes:
        process.start()

    for process in processes:
        process.join()

    curated_list = []
    for _ in range(num_cores):
        curated_list.extend(result_queue.get())

    return curated_list


if __name__ == '__main__':

    ###########################################################################
    num_Gladiators = 6
    num_Weapons = 25
    num_cores = multiprocessing.cpu_count()

    # weapons_list = list(range(num_Weapons))
    print("The list of weapons: ", list(range(num_Weapons)))

    # Generate all unique combinations of the attack guesses
    print("Creating attack combinations with the number of Gladiators = %s and the number of Weapons = %s. Based on the level response." %
          (num_Gladiators, num_Weapons))
    attack_combinations = list(
        itertools.permutations(list(range(num_Weapons)), num_Gladiators))

    # print("Available attack combinations are: ", attack_combinations)
    print(f"Number of possible attacks: {len(attack_combinations)}")

    my_guess = [0, 4, 5, 3, 10, 20]
    actual_solution = (0, 5, 2, 7, 15, 19)
    response = [2, 1]

    result_parallel = curated_parallel(attack_combinations, my_guess, response)

    print(len(result_parallel))
