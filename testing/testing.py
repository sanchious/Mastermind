import itertools
import multiprocessing
import time

###########################################################################
num_Gladiators = 6
num_Weapons = 25
num_cores = multiprocessing.cpu_count()

# weapons_list = list(range(num_Weapons))
print("The list of weapons: ", list(range(num_Weapons)))

# Generate all unique combinations of the attack guesses
print("Creating attack combinations with number of Gladiators = %s and number of Weapons = %s. Based on the level response." %
      (num_Gladiators, num_Weapons))
attack_combinations = list(
    itertools.permutations(list(range(num_Weapons)), num_Gladiators))


# Convert "attack_combinations" tuples to a nested list
# attack_combinations = [list(t) for t in attack_combinations]

# print("Available attack combinations are: ", attack_combinations)
print(f"Number of possible attacks: {len(attack_combinations):_}")

my_guess = [0, 4, 5, 3, 10, 20]
actual_solution = (0, 5, 2, 7, 15, 19)
response = [2, 1]

# my_guess = [0, 4, 5, 3]
# actual_solution = (0, 5, 2, 7)
# response = [2, 1]

curated_attack_combinations = []
curated_attack_combinations_test = []


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


def curated_sublist(attack_list_of_lists, guess, score):
    curated_list = []
    for i in range(len(attack_list_of_lists)):
        for j in range(len(attack_list_of_lists[i])):
            if compare_response(guess, attack_list_of_lists[i][j]) == score:
                curated_list.append(attack_list_of_lists[i][j])
    return curated_list


print(compare_response(my_guess, actual_solution))

# Divide the attack_combinations list into a number of sublist based on the number of cores available
divided_attack_combinations = []
for i in range(num_cores):
    sublist = list(attack_combinations)[i::num_cores]
    divided_attack_combinations.append(sublist)

print(
    f"Devided attack combination list lenght: {len(divided_attack_combinations)}")
# print(divided_attack_combinations)

# if __name__ == "__main__":
#     manager = multiprocessing.Manager()
#     return_list = manager.list()
#     jobs = []
#     for i in range(num_cores):
#         p = multiprocessing.Process(target=curated, args=(
#             divided_attack_combinations[i], my_guess, response))
#         jobs.append(p)
#         p.start()

#     for proc in jobs:
#         proc.join()
#     print('Testing: ', return_list)


# if __name__ == '__main__':
#     with multiprocessing.Pool as pool:
#         args = [(divided_attack_combinations[i], my_guess, response)
#                 for i in range(10)]

#         results = pool.map(curated, args)
#         print(len(results))


# ##############################
# print("Creating a DEVIDED curated attack list by 'comparing_response'")
# start_time = time.time()
# curated_devided_attack_combinations = curated_sublist(
#     divided_attack_combinations, my_guess, response)
# end_time = time.time()
# run_time = end_time - start_time
# print("Done comparing. DEVIDED curated list is completed.")
# print(f"Run time - {run_time}")

# print("checking if the solution ramained in the curated list")
# for i in range(len(curated_devided_attack_combinations)):
#     # print(
#     #     f"Checking {actual_solution} against {curated_attack_combinations[i]}")
#     if actual_solution == curated_devided_attack_combinations[i]:
#         print(
#             f"The solution is still in the DEVIDED currated list: {curated_devided_attack_combinations[i]}")
# print("Done")
# print(
#     f"Number of possible attacks from the DEVIDED curated attack list: {len(curated_devided_attack_combinations)}")
# ##############################


###########################################################################
print("Creating a curated attack list by 'comparing_response'")
start_time = time.time()
curated_attack_combinations = curated(
    attack_combinations, my_guess, response)
end_time = time.time()
run_time = end_time - start_time
print("Done comparing. Curated list is completed.")
print(f"Run time - {run_time}")
##########
# print(curated_attack_combinations)
print(f"{len(curated_attack_combinations):_}")
# print(curated_attack_combinations)

# # let's check if the solution is still in the curated list
# print("checking if the solution ramained in the curated list")
# for i in range(len(curated_attack_combinations)):
#     # print(
#     #     f"Checking {actual_solution} against {curated_attack_combinations[i]}")
#     if actual_solution == curated_attack_combinations[i]:
#         print(
#             f"The solution is still in the currated list: {curated_attack_combinations[i]}")
# print("Done")
# print(
#     f"Number of possible attacks from the curated list: {len(curated_attack_combinations)}")
# ###########################################################################

# 127512000

###########################################################################
# # Alternative funtion
# def compare_lists(my_guess, possible_solution):
#     set1 = set(my_guess)
#     set2 = set(possible_solution)

#     intersection = set1.intersection(set2)

#     num_common = len(intersection)

#     num_same_index = 0
#     for i in range(len(my_guess)):
#         # print(f"comparing list1[{i}] = {list1[i]} and list2[{i}] = {list2[i]}")
#         if my_guess[i] == possible_solution[i]:
#             num_same_index += 1
#             # print(f"num_same_index is {num_same_index}")

#     return [num_common, num_same_index]

# my_guess = [1, 0, 2, 5]
# possible_solution = [2, 3, 4, 5]

# result = compare_lists(my_guess, possible_solution)
# print(result)


# result1 = compare_response(my_guess, possible_solution)
# print(result1)
###########################################################################


# Number of possible attacks: 127_512_000
# [2, 1]
# Devided attack combination list lenght: 10
# Creating a curated attack list by 'comparing_response'
# Done comparing. Curated list is completed.
# Run time - 70.22822618484497
# 11_162_880
