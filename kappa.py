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

def get_mode(args):
    if args.get('--unweighted'):
        return 'unweighted'
    elif args.get('--squared'):
        return 'squared'
    else:
        return 'linear'

def read_ratings(csv, filename):
    if csv:
        return np.genfromtxt(filename, delimiter=',')
    else:
        return np.genfromtxt(filename)

def build_weight_matrix(categories, mode):
    weighted = np.empty((categories, categories))
    for i in range(categories):
        for j in range(categories):
            if args.get('--unweighted'):
                weighted[i, j] = (i != j)
                mode = 'unweighted'
            elif args.get('--squared'):
                weighted[i, j] = abs(i - j) ** 2
                mode = 'squared'
            else:  #linear
                weighted[i, j] = abs(i - j)
                mode = 'equal weights'

    return weighted

def build_observed_matrix(categories, subjects, ratings):
    observed = np.zeros((categories, categories))
    distributions = np.zeros((categories, 2))
    for k in range(subjects):
        observed[ratings[k, 0], ratings[k, 1]] += 1
        distributions[ratings[k, 0], 0] += 1
        distributions[ratings[k, 1], 1] += 1

    observed = observed / subjects
    distributions = distributions / subjects

    return observed, distributions

def build_expected_matrix(categories, distributions):
    expected = np.empty((categories, categories))
    for i in range(categories):
        for j in range(categories):
            expected[i, j] = distributions[i, 0] * distributions[j, 1]

    return expected

def calculate_kappa(weighted, observed, expected):
    return 1.0 - (sum(sum(weighted * observed)) / sum(sum(weighted * expected)))

def main(args):
    mode = get_mode(args)
    ratings = read_ratings(args.get('--csv'), args.get('--filename'))
    categories = int(np.amax(ratings)) + 1
    subjects = ratings.size / 2
    weighted = build_weight_matrix(categories, mode)
    observed, distributions = build_observed_matrix(categories, subjects, ratings)
    expected = build_expected_matrix(categories, distributions)
    kappa = calculate_kappa(weighted, observed, expected)

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
