from random import randint


# description
# 
# given 3 numbers from 1 - 100, choose 2 options
# decide if the result is higher, lowers, or in-between
# if result is the same as any of the 2 choices = lose

def start():
    # starting numbers
    nums = {
        'a': randint(20, 80),
        'b': randint(20, 60),
        'c': randint(40, 80),
    }
    return nums

def end(num1, num2, choice): 
    response = None
    # new number
    compare = randint(0, 100)

    # input of choice
    choices = {
        "hi": (compare > max(num1, num2)),
        "mid": (compare > min(num1, num2) and compare < max(num1, num2)),
        "lo": (compare < min(num1, num2))
    }

    # automatic loss
    if compare == num1 or compare == num2:
        return 0, num1, num2, choice, compare
    elif choices[choice]:
        return 1, num1, num2, choice, compare
    else:
        return -1, num1, num2, choice, compare
    