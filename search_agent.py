from assignment import *


class SearchAgent:
    def __init__(self, csp, with_forward_checking):
        self.csp = csp
        self.with_fc = with_forward_checking

    def backtracking_search(self):
        self.node_consistency()
        assignment = Assignment(self.csp)
        return self.backtrack(assignment)

    def node_consistency(self):
        for constraint in self.csp.unary_constrains:
            self.csp.located_in(constraint[0], constraint[2])

    def backtrack(self, assignment):
        if assignment.is_complete():
            return assignment.solution
        var = assignment.select_unassigned_variables()
        for value in self.csp.domains[self.csp.get_index(var)]:
            prev_domains = [i[:] for i in self.csp.domains]
            assignment.assign(var, value)
            self.csp.set_domain(var, [value])
            if self.is_consistent_with(var):
                res = self.backtrack(assignment)
                if res is not None:
                    return res
            assignment.reparo(var)
            self.csp.domains = prev_domains
        return None

    def is_consistent_with(self, var):
        if not self.csp.all_diff(var):
            return False
        for cons in self.csp.constrains[var]:
            if not cons[0](var, cons[1], self.with_fc):
                return False
        return True
