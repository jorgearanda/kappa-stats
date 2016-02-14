import numpy as np
import kappa

def test_sanity():
    assert True

def test_get_mode():
    assert kappa.get_mode({'--unweighted': True, '--squared': False}) == 'unweighted'
    assert kappa.get_mode({'--unweighted': False, '--squared': True}) == 'squared'
    assert kappa.get_mode({'--unweighted': False, '--squared': False}) == 'linear'
    assert kappa.get_mode({'--linear': True}) == 'linear'

def test_build_weight_matrix_unweighted():
    weighted = kappa.build_weight_matrix(3, 'unweighted')
    assert weighted.size == 9
    assert weighted[0][0] == 0
    assert weighted[0][1] == 1
    assert weighted[0][2] == 1
    assert weighted[1][0] == 1
    assert weighted[1][1] == 0
    assert weighted[1][2] == 1
    assert weighted[2][0] == 1
    assert weighted[2][1] == 1
    assert weighted[2][2] == 0

def test_build_weight_matrix_squared():
    weighted = kappa.build_weight_matrix(3, 'squared')
    assert weighted.size == 9
    assert weighted[0][0] == 0
    assert weighted[0][1] == 1
    assert weighted[0][2] == 4
    assert weighted[1][0] == 1
    assert weighted[1][1] == 0
    assert weighted[1][2] == 1
    assert weighted[2][0] == 4
    assert weighted[2][1] == 1
    assert weighted[2][2] == 0

def test_build_weight_matrix_linear():
    weighted = kappa.build_weight_matrix(3, 'linear')
    assert weighted.size == 9
    assert weighted[0][0] == 0
    assert weighted[0][1] == 1
    assert weighted[0][2] == 2
    assert weighted[1][0] == 1
    assert weighted[1][1] == 0
    assert weighted[1][2] == 1
    assert weighted[2][0] == 2
    assert weighted[2][1] == 1
    assert weighted[2][2] == 0

def test_build_observed_matrix_simple():
    observed, distributions = kappa.build_observed_matrix(2, 3, np.array([[0, 1], [1, 1], [0, 0]]))
    assert observed[0, 0] == 1.0 / 3
    assert observed[0, 1] == 1.0 / 3
    assert observed[1, 0] == 0
    assert observed[1, 1] == 1.0 / 3
    assert distributions[0, 0] == 2.0 / 3
    assert distributions[1, 0] == 1.0 / 3
    assert distributions[0, 1] == 1.0 / 3
    assert distributions[1, 1] == 2.0 / 3

def test_build_observed_matrix_longer():
    observed, distributions = kappa.build_observed_matrix(3, 5, np.array([[0, 1], [2, 2], [1, 1], [0, 2], [1, 1]]))
    assert observed[0, 0] == 0
    assert observed[0, 1] == 1.0 / 5
    assert observed[0, 2] == 1.0 / 5
    assert observed[1, 0] == 0
    assert observed[1, 1] == 2.0 / 5
    assert observed[1, 2] == 0
    assert observed[2, 0] == 0
    assert observed[2, 1] == 0
    assert observed[2, 2] == 1.0 / 5
    assert distributions[0, 0] == 2.0 / 5
    assert distributions[0, 1] == 0
    assert distributions[1, 0] == 2.0 / 5
    assert distributions[1, 1] == 3.0 / 5
    assert distributions[2, 0] == 1.0 / 5
    assert distributions[2, 1] == 2.0 / 5
