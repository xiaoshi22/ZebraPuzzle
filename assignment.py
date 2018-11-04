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
