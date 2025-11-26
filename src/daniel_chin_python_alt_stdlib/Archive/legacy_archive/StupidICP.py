import sys

def calc_average(score1, score2, score3, score4, score5):
    # Complete this function
    return sum([score1, score2, score3, score4, score5])/5


def determine_grade(score):
    dict={0:'F',1:'F',2:'F',3:'F',4:'F',5:'F',6:'D',0:'C',0:'B',0:'A',0:'A'}
    return dict[score//10]
    # Complete this function

def main():
    score1 = float(input().strip())
    score2 = float(input().strip())
    score3 = float(input().strip())
    score4 = float(input().strip())
    score5 = float(input().strip())
    # # This function should accept 5 test scores as arguments and return the average of the scores.
    average = calc_average(score1, score2, score3, score4, score5)
    print(determine_grade(score1),score1)
    print(determine_grade(score2),score2)
    print(determine_grade(score3),score3)
    print(determine_grade(score4),score4)
    print(determine_grade(score5),score5)
    print(determine_grade(average),average)
    #  Complete the program
main()
print('eee')
