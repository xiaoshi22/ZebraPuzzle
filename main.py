from csp import *
from search_agent import *
import time


def main():
    csp = CSP('constrains.txt')
    print '''
************************************
* ZEBRA PUZZLE  PROBLEM DEFINITION *
************************************
'''
    print 'Variables: ', \
        '\nCOLORS: ', ', '.join(csp.COLORS), \
        '\nNATIONALITIES: ', ', '.join(csp.NATIONALITIES), \
        '\nCANDIES: ', ', '.join(csp.CANDIES), \
        '\nDRINKS: ', ', '.join(csp.DRINKS), \
        '\nPETS: ', ', '.join(csp.PETS)

    print '\nDomains: ' \
          '\nD_i = {1, 2, 3, 4, 5} for every variables. '

    print '\nConstrains: '
    with open("constrains.txt") as f:
        print f.read()

    resp1 = raw_input('See the Solution? (yes/no)')
    while True:
        if resp1 == 'no':
            return
        elif resp1 == 'yes':
            resp2 = raw_input('With forward checking? (yes/no)')
            while True:
                start = time.time()
                if resp2 == 'no':
                    search_agent = SearchAgent(csp, False)
                elif resp2 == 'yes':
                    search_agent = SearchAgent(csp, True)
                else:
                    resp2 = raw_input('Please enter yes or no. ')
                    continue
                solution = search_agent.backtracking_search()
                exe_time = time.time() - start
                ans = [['1'], ['2'], ['3'], ['4'], ['5']]
                for name, num in solution.items():
                    ans[num-1].append(name)
                print '''
    ************
    * SOLUTION *
    ************
    '''
                for i in xrange(6):
                    print('{:<15s} {:<15s} {:<15s} {:<15s} {:<15s}'.format(ans[0][i], ans[1][i], ans[2][i], ans[3][i],
                                                                           ans[4][i]))
                print '\nExecution time: ', exe_time, 's'
                return
        else:
            resp1 = raw_input('Please enter yes or no. ')


if __name__ == '__main__':
    main()
