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

    def is_complete(self):
        return len(self.solution) == 25

    def assign(self, var, value):
        self.solution[var] = value

    def reparo(self, var):
        del self.solution[var]

    def select_unassigned_variables(self):
        unassigned = set(self.csp.keys.keys()) - set(self.solution.keys())
        return unassigned.pop()
