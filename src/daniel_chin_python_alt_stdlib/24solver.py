'''
Do you know the 24 card game?  
'''
from itertools import permutations, combinations

def solve(numbers):
    '''Recursive. '''
    if len(numbers) == 1:
        if abs(numbers[0] - 24) < .00001:
            return True, [24]
        return False, []
    for operations, iterPolicies in (
        ('+*', combinations), ('-/', permutations)
    ):
        for a, b in iterPolicies(numbers, 2):
            for operation in operations:
                numbers_copy = numbers.copy()
                [numbers_copy.remove(x) for x in (a, b)]
                expression = f'{a}{operation}{b}'
                try:
                    new_number = eval(expression)
                    new_number = tryRounding(new_number)
                except ZeroDivisionError:
                    continue
                except ValueError:
                    pass
                if new_number >= 0:
                    can_do, solution = solve(numbers_copy + [new_number])
                    did_it = False
                    if can_do:
                        new_solution = []
                        for token in solution:
                            if not did_it and type(token) in (int, float) and abs(token - new_number) < .0001:
                                new_solution.extend(['(', a, operation, b, ')'])
                                did_it = True
                            else:
                                new_solution.append(token)
                        return True, new_solution
    return False, []

def tryRounding(x):
    rounded = round(x)
    if abs(rounded - x) < .0001:
        return rounded
    raise ValueError

def main():
    while True:
        try:
            op = input('Four numbers, seperated by space: ')
        except (EOFError, KeyboardInterrupt):
            break
        numbers = [int(x.strip()) for x in op.strip().split(' ')]
        can_do, path = solve(numbers)
        if can_do:
            print('There is solution. ')
            input('Press ENTER to see it...')
            print(''.join([str(x) for x in path]).replace('*', '×').replace('/', '÷'))
        else:
            print('No solution.')
        print()

if __name__ == "__main__":
    main()
