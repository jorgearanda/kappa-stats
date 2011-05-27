import sys
import numpy as np

def main(args):
	# Read options
	unweighted = squared = linear = verbose = csv = False
	if "-u" in args or "--unweighted" in args:
		unweighted = True
	elif "-s" in args or "--squared" in args:
		squared = True
	else:
		linear = True
	if "-v" in args or "--verbose" in args:
		verbose = True
	if "-c" in args or "--csv" in args:
		csv = True
		
	# Read ratings. Last argument is the filename
	if csv:
		ratings = np.genfromtxt(args[-1], delimiter=",")
	else:
		ratings = np.genfromtxt(args[-1])
	
	categories = int(np.amax(ratings)) + 1
	subjects = ratings.size / 2
	
	# Build weight matrix
	weighted = np.empty((categories, categories))
	for i in range(categories):
		for j in range(categories):
			if unweighted:
				weighted[i, j] = (i != j)
			elif squared:
				weighted[i, j] = abs(i - j) ** 2
			else: #linear
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
	
	if verbose:
		print "Kappa",
		if unweighted:
			print "(unweighted):",
		elif squared:
			print "(squared):",
		else:
			print "(equal weights):",
		print kappa
		print "Categories: " + str(categories)
		print "Subjects: " + str(subjects)
	else:
		print kappa


def usage():
	print "usage: python kappa.py {[-l]|-u|-s} [-v] [-c] FILENAME"
	print
	print "Calculates Weighted Kappa and Cohen's Kappa for interrater agreement"
	print "(two raters, any number of ordinal categories)"
	print "See http://en.wikipedia.org/wiki/Cohen's_kappa for more information"
	print
	print "FILENAME must be a text file with a pair of integers in each line."
	print "The values in each pair correspond to the rating that each of the"
	print "two reviewers gave to a particular subject."
	print "The pairs must be whitespaced-separated (or comma-separated, with the -c flag)."
	print
	print "Options:"
	print "--------"
	print
	print "-l --linear:     Linear weights for disagreements (default)"
	print "-u --unweighted: Cohen's Kappa (unweighted agreement/disagreement)"
	print "-s --squared:    Squared weights for disagreements"
	print "-v --verbose:    Includes number of categories and subjects in the output"
	print "-c --csv:        For text files with comma-separated values"


if __name__ == "__main__":
	if len(sys.argv) == 1 or "--help" in sys.argv:
		usage()
	else:
		main(sys.argv[1:])
	