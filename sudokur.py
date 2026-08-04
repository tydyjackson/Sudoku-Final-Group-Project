import random
import math
#Three conditions to be checked
#NUMBER DOES NOT REPEAT INSIDE THE BOX
#NUMBER DOES NOT REPEAT INSIDE THE ROW
#NUMBER DOES NOT REPEAT INSIDE THE COLUMN

#print(random.randint(1, 10))
#box ranges 0-2 ,3-5 ,6-8
import random


def is_valid(board, row, col, num):
    # Check row & column
    for i in range(9):
        #if there is a number in the row that is equal to the number or a number in the column that is equal to the number
        if board[row][i] == num or board[i][col] == num:
            return False

    #straighten out the numbers first!!! ,it gets weird if you don't
    box_row, box_col = 3 * (row // 3), 3 * (col // 3)
    for r in range(box_row, box_row + 3):
        for c in range(box_col, box_col + 3):
            #if there is a number in the row that does not work
            if board[r][c] == num:
                return False

    return True


def fill_board(board):
    for row in range(9):
        for col in range(9):
            #if there is an empty value that has not been given
            if board[row][col] == 0:
                #this is going to give you a list of a numbers that then will be shuffled randomly
                numbers = list(range(1, 10))
                random.shuffle(numbers) #this is a command that randomly organizes them in a sequence ,all unique numbers


                for num in numbers: #for all the numbers in the randomized list

                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        #checks if every single number provided works
                        if fill_board(board): #if you are done ,you are done
                            return True
                        board[row][col] = 0  # if you are not done ,start again
                return False #start againer
    return True #if you did all of this also ,then you also pass




def initialize_board(num_cols):
    secret_board = [[0 for _ in range(9)] for _ in range(9)]
    return secret_board
def print_board(board):
    for row in range(len(board)):
        for columm in range(len(board[0])):
            if columm == (len(board[0]))-1:
                print(board[row][columm] , end = "")
            else:
                print(board[row][columm] , end = " ")
        print()


board = initialize_board(9)

fill_board(board)