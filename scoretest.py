
import csv
import cmd
import numpy as np

# true_answers = 'ccedebcacebbbeaaaddb'
# num_questions =
#test_name = 'BioG1140_Quiz2'


class TestScorer(cmd.Cmd):
    intro='Enter student\'s name then answers as strings'
    scores = {}
    true_answers = []
    num_questions = 1
    test_name = 'test'

    prompt = '(scorer)'

    def do_set_answers(self, i):
        'Set the default answers for the test'
        self.true_answers = i
        self.num_questions = len(self.true_answers)
        return

    def do_set_name(self, i):
        'Set the output file name'
        self.test_name = i
        return

    def do_score(self, s):
        'Enter student identifiers and answers'
        l = s.split()
        # missing name and scores
        if len(l) != 2:
            print
            "*** invalid number of arguments"
            return
        # check args are strings
        try:
            l = [str(i) for i in l]
        except ValueError:
            print
            "*** arguments should be numbers"
            return

        student_answers = l[1]
        student_name = l[0]
        # bool array of scores
        scored_answers = []
        for i in range(0, self.num_questions):
            scored_answers.append(int(student_answers[i] is self.true_answers[i]))
        self.scores[student_name] = scored_answers
        return

    def do_summarize(self, arg):
        'Sum across students and questions to summarize test results'
        total_per_q = np.zeros((self.num_questions))
        for key, val in self.scores.items():
            # personal total
            self.scores[key].append(sum(val))
            # sum totals per question
            for i in range(0, self.num_questions):
                total_per_q[i] += val[i]
        self.scores['q_totals'] = total_per_q
        return

    def do_save_scores(self, arg):
        # row headers
        header = ['Student_name']
        for i in range(0, 20):
            header.append('Q' + str(i + 1))
        header.append('student_total')
        'Output data to a csv file'
        with open(self.test_name+".csv", "wt") as outfile:
            w = csv.writer(outfile)
            w.writerow(h for h in header)
            for key, val in self.scores.items():
                print([key, *val])
                w.writerow([key, *[str(i) for i in val]])
        return



    def do_exit(self, arg):
        'Exit the scorer'
        return True

if __name__ == '__main__':
    TestScorer().cmdloop()