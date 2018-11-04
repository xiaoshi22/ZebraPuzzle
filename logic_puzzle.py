def main():
    csp = CSP('constrains.txt')
    print 'PROBLEM DEFINITION\n'
    print 'Variables: '
    print 'COLORS: ', csp.COLORS
    print 'NATIONALITIES', csp.NATIONALITIES
    print 'CANDIES', csp.CANDIES
    print 'DRINKS', csp.DRINKS
    print 'PETS', csp.PETS

    print '\nConstrains: '
    with open("constrains.txt") as f:
        print f.read()

    solution = csp.backtracking_search()
    while True:
        resp = raw_input('See the Solution? (y/n)')
        if resp == 'N' or resp == 'n':
            return
        elif resp == 'Y' or resp == 'y':
            ans = [['1'], ['2'], ['3'], ['4'], ['5']]
            for name, num in solution.items():
                ans[num-1].append(name)
            print '\nSOLUTION\n'
            for i in xrange(6):
                print('{:<15s} {:<15s} {:<15s} {:<15s} {:<15s}'.format(ans[0][i], ans[1][i], ans[2][i], ans[3][i], ans[4][i]))
            return


class CSP:
    COLORS = ["red", "green", "yellow", "blue", "ivory"]
    NATIONALITIES = ["Englishman", "Spaniard", 'Norwegian', "Ukrainian", "Japanese"]
    CANDIES = ["Hershey bars", "Kit Kats", "Smarties", "Snickers", "Milky Ways"]
    DRINKS = ["orange juice", "tea", "coffee", "milk", "water"]
    PETS = ["dog", "fox", "snails", "horse", "zebra"]

    def __init__(self, constrains_file):
        self.keys = {}
        self.values = []
        self.domains = []
        for i in xrange(25):
            if i < 5:
                self.keys[self.COLORS[i % 5]] = i
                self.values.append(self.COLORS[i % 5])
            elif i < 10:
                self.keys[self.NATIONALITIES[i % 5]] = i
                self.values.append(self.NATIONALITIES[i % 5])
            elif i < 15:
                self.keys[self.CANDIES[i % 5]] = i
                self.values.append(self.CANDIES[i % 5])
            elif i < 20:
                self.keys[self.DRINKS[i % 5]] = i
                self.values.append(self.DRINKS[i % 5])
            else:
                self.keys[self.PETS[i % 5]] = i
                self.values.append(self.PETS[i % 5])
            self.domains.append([1, 2, 3, 4, 5])

        self.unary_constrains = []
        self.constrains = {}
        for var in self.keys.keys():
            self.constrains[var] = []

        with open(constrains_file) as f:
            for line in f:
                line = line[:-1]
                temp = line.split(', ')
                if temp[1] == 'located in':
                    self.unary_constrains.append([temp[0], self.located_in, int(temp[2])])
                elif temp[1] == 'in the same house':
                    self.constrains[temp[0]].append([self.in_the_same_house, temp[2]])
                    self.constrains[temp[2]].append([self.in_the_same_house, temp[0]])
                elif temp[1] == 'next to':
                    self.constrains[temp[0]].append([self.next_to, temp[2]])
                    self.constrains[temp[2]].append([self.next_to, temp[0]])
                elif temp[1] == 'to the left of':
                    self.constrains[temp[0]].append([self.to_the_left_of, temp[2]])
                    self.constrains[temp[2]].append([self.to_the_right_of, temp[0]])
                elif temp[1] == 'to the right of':
                    self.constrains[temp[0]].append([self.to_the_right_of, temp[2]])
                    self.constrains[temp[2]].append([self.to_the_left_of, temp[0]])
                else:
                    print "Undefined constraint func in CSP.__init__"

    def backtracking_search(self):
        self.node_consistency()
        assignment = Assignment(self)
        return self.backtrack(assignment)

    def backtrack(self, assignment):
        if assignment.is_complete():
            return assignment.solution
        var = assignment.select_unassigned_variables()
        for value in self.domains[self.get_index(var)]:
            prev_domains = [i[:] for i in self.domains]
            assignment.assign(var, value)
            self.set_domain(var, [value])
            if assignment.is_consistent_with(var):
                res = self.backtrack(assignment)
                if res is not None:
                    return res
            assignment.reparo(var)
            self.domains = prev_domains
        return None

    def node_consistency(self):
        for constraint in self.unary_constrains:
            self.located_in(constraint[0], constraint[2])

    def get_index(self, var_name):
        return self.keys[var_name]

    def get_name(self, index):
        return self.values[index]

    def set_domain(self, var_name, values):
        self.domains[self.get_index(var_name)] = values

    def located_in(self, var, value):
        self.domains[self.get_index(var)] = [value]

    def all_diff(self, var_name):
        index = self.get_index(var_name)
        for i in xrange(len(self.domains)):
            if (i - i % 5 == index - index % 5) and (i != index) \
                    and (len(self.domains[i]) == 1) and (self.domains[i][0] == self.domains[index][0]):
                return False
        return True

    def in_the_same_house(self, l_var, r_var):
        l_value = self.domains[self.get_index(l_var)][0]
        r_index = self.get_index(r_var)
        if l_value in self.domains[r_index]:
            self.domains[r_index] = [l_value]
            return True
        else:
            return False

    def next_to(self, l_var, r_var):
        l_value = self.domains[self.get_index(l_var)][0]
        r_index = self.get_index(r_var)
        temp = []

        if l_value - 1 in self.domains[r_index]:
            temp.append(l_value - 1)
        if l_value + 1 in self.domains[r_index]:
            temp.append(l_value + 1)
        if temp:
            self.domains[r_index] = temp
            return True
        else:
            return False

    def to_the_left_of(self, l_var, r_var):
        l_value = self.domains[self.get_index(l_var)][0]
        r_index = self.get_index(r_var)

        if l_value + 1 in self.domains[r_index]:
            self.domains[r_index] =[l_value + 1]
            return True
        return False

    def to_the_right_of(self, l_var, r_var):
        l_value = self.domains[self.get_index(l_var)][0]
        r_index = self.get_index(r_var)

        if l_value - 1 in self.domains[r_index]:
            self.domains[r_index] = [l_value - 1]
            return True
        return False


class Assignment:
    def __init__(self, csp):
        self.csp = csp
        self.solution = {}

        domains = self.csp.domains
        for i in xrange(25):
            if len(domains[i]) <= 0:
                print "Invalid domain"
            elif len(domains[i]) == 1:
                self.solution[self.csp.get_name(i)] = domains[i][0]
        # self.conflict_set = {}
        # for name in self.csp.values:
        #     self.conflict_set[name] = []

    # def add_conflict(self, target_var, var):
    #     self.conflict_set[target_var].append(var)
    #
    # def pop_conflict(self, var):
    #     if self.conflict_set[var]:
    #         return self.conflict_set[var].[-1]

    def is_complete(self):
        return len(self.solution) == 25

    def assign(self, var, value):
        self.solution[var] = value

    def reparo(self, var):
        del self.solution[var]

    def select_unassigned_variables(self):
        unassigned = set(self.csp.keys.keys()) - set(self.solution.keys())
        return unassigned.pop()

    def is_consistent_with(self, var):
        if not self.csp.all_diff(var):
            return False
        for cons in self.csp.constrains[var]:
            if not cons[0](var, cons[1]):
                return False
        return True


if __name__ == '__main__':
    main()
