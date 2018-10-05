'''
A script that can rapidly grade multiple choice questions for exams

'''
import sys

true_answers = 'cdbecbadeccbcbdaceda'
student_answers = sys.argv[1]

wrong_answers = [ i for i in range(0, len(student_answers)) if student_answers[i] is not true_answers[i]]

num_corrrect = len(true_answers) - len(wrong_answers)

print('They got '+str(num_corrrect)+' correct')
print('They missed: ')

if len(wrong_answers) > 0:
    for i in range(0, len(wrong_answers)):
        print("Q" + str(wrong_answers[i]+1) + ' their answer: '
              +str(student_answers[wrong_answers[i]]) + ' \n correct answer: '+str(true_answers[wrong_answers[i]]))


