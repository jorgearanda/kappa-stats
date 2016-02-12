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
