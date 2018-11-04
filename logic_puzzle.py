colors = ["red", "green", "yellow", "blue", "ivory"]
nationalities = ["Englishman", "Spaniard", 'Norwegian', "Ukrainian", "Japanese"]
candies = ["Hershey bars", "Kit Kats", "Smarties", "Snickers", "Milky Ways"]
drinks = ["orange juice", "tea", "coffee", "milk", "water"]
pets = ["dog", "fox", "snails", "horse", "zebra"]


def main():
    csp = CSP("constrains.txt")
    for name, cons in csp.constrains.items():
        print name, cons
    for cons in csp.unary_constrains:
        print cons
    asgmt = csp.backtracking_search()
    print "Solution:"
    for ans, ans2 in asgmt.solution.items():
        print ans, ans2
    print "DONE"


class CSP:
    def __init__(self, constrains_file):
        self.variables = {}
        self.unary_constrains = []
        self.constrains = {}
        for i in xrange(5):
            self.variables[colors[i]] = Variable('colors', colors[i], [1, 2, 3, 4, 5])
            self.variables[nationalities[i]] = Variable('nationalities', colors[i], [1, 2, 3, 4, 5])
            self.variables[candies[i]] = Variable('candies', colors[i], [1, 2, 3, 4, 5])
            self.variables[drinks[i]] = Variable('drinks', colors[i], [1, 2, 3, 4, 5])
            self.variables[pets[i]] = Variable('pets', colors[i], [1, 2, 3, 4, 5])

        for var in self.variables.keys():
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

    def located_in(self, var, value):
        self.variables[var].domain = [value]

    def all_diff(self, var_name):
        var = self.variables[var_name]
        for var2_name, var2 in self.variables.items():
            if (var2.kind == var.kind) and (var2_name != var_name) and (len(var2.domain) == 1) and (var2.domain[0] == var.domain[0]):
                return False
        return True

    def in_the_same_house(self, left_var, right_var):
        for left_value in self.variables[left_var].domain:
            for right_value in self.variables[right_var].domain:
                if right_value == left_value:
                    return True
        return False

    def next_to(self, left_var, right_var):
        for left_value in self.variables[left_var].domain:
            for right_value in self.variables[right_var].domain:
                if (right_value == left_value-1) or (right_value == left_value+1):
                    return True
        return False

    def to_the_left_of(self, left_var, right_var):
        for left_value in self.variables[left_var].domain:
            for right_value in self.variables[right_var].domain:
                if right_value == left_value+1:
                    return True
        return False

    def to_the_right_of(self, left_var, right_var):
        for left_value in self.variables[left_var].domain:
            for right_value in self.variables[right_var].domain:
                if right_value == left_value-1:
                    return True
        return False

    def node_consistency(self):
        for constraint in self.unary_constrains:
            self.located_in(constraint[0], constraint[2])

    def backtracking_search(self):
        self.node_consistency()
        assignment = Assignment(self)
        return self.backtrack(assignment)

    def backtrack(self, assignment):
        if assignment.is_complete():
            return assignment
        var = assignment.select_unassigned_variables()
        for value in self.variables[var].domain:
            prev_domain = self.variables[var].domain
            assignment.assign(var, value)
            self.variables[var].domain = [value]
            if assignment.is_consistent_with(var):
                res = self.backtrack(assignment)
                if res is not None:
                    return res
            assignment.reparo(var)
            self.variables[var].domain = prev_domain
        return None


class Variable:
    def __init__(self, kind, name, domain):
        self.kind = kind
        self.name = name
        self.domain = domain


class Assignment:
    def __init__(self, csp):
        self.csp = csp
        self.solution = {}
        for var, obj in self.csp.variables.items():
            if len(obj.domain) <= 0:
                print "Invalid domain"
            elif len(obj.domain) == 1:
                self.solution[var] = obj.domain[0]

    def is_complete(self):
        return len(self.solution) == 25

    def assign(self, var, value):
        self.solution[var] = value

    def reparo(self, var):
        del self.solution[var]

    def select_unassigned_variables(self):
        unassigned = list(set(self.csp.variables.keys()) - set(self.solution.keys()))
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
