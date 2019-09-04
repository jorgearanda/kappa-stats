# Kappa Stats

This is a little Python script to generate Cohen's Kappa and Weighted Kappa measures for inter-rater reliability (or inter-rater agreement).

Cohen's Kappa is used to find the agreement between two raters and two categories. Weighted Kappa can be used for two raters and any number of ordinal categories.

A good source to understand these measures:
http://en.wikipedia.org/wiki/Cohen%27s_kappa

## Requirements
* Python 3.x
* NumPy
* docopt

## Usage

### Example
For a quick example you can run kappa.py with one of the fixture files, e.g.

    python kappa.py -cv -f test/fixtures/comma_separated.txt -u

### Command line Options

    kappa.py [--help] [--linear|--unweighted|--squared] [--verbose] [--csv] --filename <filename>

    -h, --help                            Show this
    -l, --linear                          Linear weights for disagreements (default)
    -u, --unweighted                      Cohen's Kappa (unweighted agreement/disagreement)
    -s, --squared                         Squared weights for disagreements
    -v, --verbose                         Include number of categories and subjects in the output
    -c, --csv                             For text files with comma-separated values
    -f <filename>, --filename <filename>  The filename to process, with pairs of integers on each line. The values in each pair correspond to the rating that each of the two reviewers gave to a particular subject. The pairs must be whitespaced-separated (or comma-separated, with the -c flag).

## Running the Tests

From the command line, use the following command to run the test cases
    
    python -m pytest 
