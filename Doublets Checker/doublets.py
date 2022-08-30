'''
Jason Ketterer

Usage: User can supply a word pairs csv file as a command line argument
or the program will use 'doublets.csv' located in default directory
'''

import sys
import random
import enchant
import string

'''Calculate edit distance (number of operations to 
 convert str1 to str2) between str 1 and str2 assuming
 only replacement operations.
 Assumes len(str1) = len(str2)'''
def edit_dist(str1, str2):
    '''Optimization: In the full dynamic programming version of this
    function, you normally calculate a 2-d matrix representing all of the
    subproblem results for the 3 possible operations to transform one string into
    another: insertion, deletion, replacement.  For this problem, we need only
    consider replacement operations and therefore only need to calculate the
    diagonal of this matrix.  Hence, we only need a 1-d list to hold the results.'''
    dp = [0 for i in range(0,len(str1)+1)]

    for i in range(1,len(dp)):
        if str1[i-1] == str2[i-1]:
            dp[i] = dp[i-1]
        else:
            dp[i] = dp[i-1] + 1

    return dp[len(str1)]


'''Builds the tree out breadth-first as a dictionary while searching for the end word. 
    k:v = node:parent'''
def find_solution(start_word, end_word, d):
    bfs_tree = dict()
    used = []
    search_q = []

    solutionFound = False
    search_q.append((start_word,"root"))
    used.append(start_word)
    solution_node = ""
    while not solutionFound and search_q:
        node,parent = search_q.pop(0)
        bfs_tree[node] = parent
        # find all valid words with edit distance of 1 from node and that haven't already been looked at
        for i in range(0,len(node)):
            for c in string.ascii_lowercase:
                w = node[:i] + c + node[i+1:]
                if d.check(w) and w not in used:
                    search_q.append((w, node))
                    used.append(w)
                    if w == end_word:
                        solutionFound = True
                        solution_node = node

    solution = []
    # find bottom-up solution path through tree
    if solutionFound:
        cur_key = solution_node
        solution.append(cur_key)
        while bfs_tree[cur_key] != "root":
            cur_key = bfs_tree[cur_key]
            solution.append(cur_key)
        solution.reverse()
        solution.append(end_word)

    return solution


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "Doublets.csv"

    try:
        f = open(filename, "r")
    except:
        print("Cannot open file " + filename + " for reading.")
        exit()

    # read in all word pairs from csv file
    wordpairs = []
    for line in f:
        line = line.strip()
        w1, w2 = line.split(',')
        wordpairs.append(list([w1.strip(),w2.strip()]))

    # randomly select a pair
    pair = wordpairs[random.randrange(len(wordpairs))]
    start_word, end_word = pair[0],pair[1]
    # start_word, end_word = "grass", "green"

    # find shortest word chain between words in pair
    dict_lookup = enchant.Dict("en_US")
    solution = find_solution(start_word, end_word, dict_lookup)

    if not solution:
        print("No solution for this word pair.")
        exit()

    # start game
    print("Welcome to the Doublet Game!")
    print("Today's word pair is : " + start_word + " -> " + end_word)
    print("Please enter your word chain (not including the start and end words.)")
    print("Enter 'q' when you're done")

    # get user input
    user_input = []
    word = input()
    while word != 'q':
        user_input.append(word)
        word = input()

    # check if all the words are valid
    for w in user_input:
        if not dict_lookup.check(w):
            print("\n\"" + w + "\" is not a word in the dictionary. You lose.")
            exit()
    print("All the entered words are in the dictionary.")

    # check if the words satisfy the constraint
    constraint_satisfied = True
    for i in range(0,len(user_input)-1):
        if edit_dist(user_input[i], user_input[i+1]) != 1:
            constraint_satisfied = False

    if constraint_satisfied:
        print("All words follow the one letter constraint.")
    else:
        print("You have violated the one letter change constraint. You lose.")
        exit()

    # check if the problem is solved
    if edit_dist(user_input.pop(), end_word) == 1:
        print("You have successfully solved the problem.")

        # check if solution is optimal
        if len(user_input) <= len(solution)-2:
            print("Congratulations! You have also solved the problem with the smallest number of words.")
        else:
            print("There is a shorter solution:")
            s = ""
            for w in solution:
                s += w + " -> "
            print(s.rstrip(" -> "))
    else:
        print("You did not solve the problem.")
        print("Here is one solution:")
        s = ""
        for w in solution:
            s += w + " -> "
        print(s.rstrip(" -> "))







