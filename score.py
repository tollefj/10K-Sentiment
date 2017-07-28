class Score:
    def __init__(self, row):
        self.year, self.item, self.descr, \
            self.pos, self.neg, self.polar, self.subj = row

    def get(self):
        return str(self.year) + ":" + self.item

    def compare(self, other):
        def show(cmd, a, b):
            print(cmd + ': ' + self.get() + '(' + a + ')' +
                  '\t-\t' + other.get() + '(' + b + ')')
        show('Negativity', self.neg, other.neg)
        show('Positivity', self.pos, other.pos)
        show('Polarity', self.polar, other.polar)
        show('Subjectivity', self.subj, other.subj)
