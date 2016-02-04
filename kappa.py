#!/usr/bin/env python

from docopt import docopt
import numpy as np

usage = """Usage: kappa.py [--help] [--linear|--unweighted|--squared] [--verbose] [--csv] --filename <filename>

-h, --help                            Show this
-l, --linear                          Linear weights for disagreements (default)
-u, --unweighted                      Cohen's Kappa (unweighted agreement/disagreement)
-s, --squared                         Squared weights for disagreements
-v, --verbose                         Include number of categories and subjects in the output
-c, --csv                             For text files with comma-separated values
-f <filename>, --filename <filename>  The filename to process, with pairs of integers on each line. The values in each pair correspond to the rating that each of the two reviewers gave to a particular subject. The pairs must be whitespaced-separated (or comma-separated, with the -c flag).
"""

def main(args):
    if args.get('--unweighted'):
        mode = 'unweighted'
    elif args.get('--squared'):
        mode = 'squared'
    else:
        mode = 'linear'

    # Read ratings
    if args.get('--csv'):
        ratings = np.genfromtxt(args.get('--filename'), delimiter=',')
    else:
        ratings = np.genfromtxt(args.get('--filename'))

    categories = int(np.amax(ratings)) + 1
    subjects = ratings.size / 2

    # Build weight matrix
    weighted = np.empty((categories, categories))
    for i in range(categories):
        for j in range(categories):
            if mode == 'unweighted':
                weighted[i, j] = (i != j)
            elif mode == 'squared':
                weighted[i, j] = abs(i - j) ** 2
            else:  #linear
                weighted[i, j] = abs(i - j)

    # Build observed matrix
    observed = np.zeros((categories, categories))
    distributions = np.zeros((categories, 2))
    for k in range(subjects):
        observed[ratings[k, 0], ratings[k, 1]] += 1
        distributions[ratings[k, 0], 0] += 1
        distributions[ratings[k, 1], 1] += 1

    # Normalize observed and distribution arrays
    observed = observed / subjects
    distributions = distributions / subjects

    # Build expected array
    expected = np.empty((categories, categories))
    for i in range(categories):
        for j in range(categories):
            expected[i, j] = distributions[i, 0] * distributions[j, 1]

    # Calculate kappa
    kappa = 1.0 - (sum(sum(weighted * observed)) / sum(sum(weighted * expected)))

    if args.get('--verbose'):
        print('Kappa (' + mode + '):')
        print(kappa)
        print('Categories: ' + str(categories))
        print('Subjects: ' + str(subjects))
    else:
        print(kappa)


if __name__ == "__main__":
    args = docopt(usage, argv=None, help=True, version=None, options_first=False)
    main(args)
