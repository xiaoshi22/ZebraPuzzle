from csp import *


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

    solution = csp.backtracking_search()
    while True:
        resp = raw_input('See the Solution? (y/n)')
        if resp == 'N' or resp == 'n':
            return
        elif resp == 'Y' or resp == 'y':
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
            return


if __name__ == '__main__':
    main()
