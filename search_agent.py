from assignment import *
from collections import deque


class SearchAgent:
    PAIN_BACKTRACKING = 0
    FORWARD_CHECKING = 1
    AC_3 = 2

    def __init__(self, csp, algorithm):
        self.csp = csp
        self.alg = algorithm

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
            if self.is_consistent_with(assignment, var, value):
                res = self.backtrack(assignment)
                if res is not None:
                    return res
            assignment.reparo(var)
            self.csp.domains = prev_domains
        return None

    def is_consistent_with(self, assignment, var, value):
        assignment.assign(var, value)
        self.csp.set_domain(var, [value])

        if self.alg == self.PAIN_BACKTRACKING or self.alg == self.FORWARD_CHECKING:
            for cons in self.csp.constrains[var]:
                if not cons[1](var, cons[2], self.alg):
                    return False
            return True

        elif self.alg == self.AC_3:
            queue = deque(self.csp.constrains[var])
            while queue:
                cons = queue.popleft()
                ret = cons[1](cons[0], cons[2], self.alg)
                if ret:
                    if ret is not True:
                        for cons2 in self.csp.constrains[ret]:
                            if cons2[2] != cons[0]:
                                queue.append(cons2)
                else:
                    return False
            return True
