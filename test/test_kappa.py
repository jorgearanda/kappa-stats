import pytest
import numpy as np
import kappa

EPSILON = 0.0001


def test_sanity():
    assert True


def test_get_mode():
    assert kappa.get_mode({"--unweighted": True, "--squared": False}) == "unweighted"
    assert kappa.get_mode({"--unweighted": False, "--squared": True}) == "squared"
    assert kappa.get_mode({"--unweighted": False, "--squared": False}) == "linear"
    assert kappa.get_mode({"--linear": True}) == "linear"


def test_build_weight_matrix_unweighted():
    weighted = kappa.build_weight_matrix(3, "unweighted")
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
    weighted = kappa.build_weight_matrix(3, "squared")
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
    weighted = kappa.build_weight_matrix(3, "linear")
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
    observed = kappa.build_observed_matrix(2, 3, np.array([[0, 1], [1, 1], [0, 0]]))
    assert observed[0, 0] == 1.0 / 3
    assert observed[0, 1] == 1.0 / 3
    assert observed[1, 0] == 0
    assert observed[1, 1] == 1.0 / 3


def test_build_observed_matrix_longer():
    observed = kappa.build_observed_matrix(
        3, 5, np.array([[0, 1], [2, 2], [1, 1], [0, 2], [1, 1]])
    )
    assert observed[0, 0] == 0
    assert observed[0, 1] == 1.0 / 5
    assert observed[0, 2] == 1.0 / 5
    assert observed[1, 0] == 0
    assert observed[1, 1] == 2.0 / 5
    assert observed[1, 2] == 0
    assert observed[2, 0] == 0
    assert observed[2, 1] == 0
    assert observed[2, 2] == 1.0 / 5


def test_build_distributions_matrix_simple():
    distributions = kappa.build_distributions_matrix(
        2, 3, np.array([[0, 1], [1, 1], [0, 0]])
    )
    assert distributions[0, 0] == 2.0 / 3
    assert distributions[1, 0] == 1.0 / 3
    assert distributions[0, 1] == 1.0 / 3
    assert distributions[1, 1] == 2.0 / 3


def test_build_distributions_matrix_longer():
    distributions = kappa.build_distributions_matrix(
        3, 5, np.array([[0, 1], [2, 2], [1, 1], [0, 2], [1, 1]])
    )
    assert distributions[0, 0] == 2.0 / 5
    assert distributions[0, 1] == 0
    assert distributions[1, 0] == 2.0 / 5
    assert distributions[1, 1] == 3.0 / 5
    assert distributions[2, 0] == 1.0 / 5
    assert distributions[2, 1] == 2.0 / 5


def test_build_expected_matrix():
    expected = kappa.build_expected_matrix(
        3, np.array([[0.4, 0], [0.4, 0.6], [0.2, 0.4]])
    )
    assert abs(expected[0, 0] - 0) < EPSILON
    assert abs(expected[0, 1] - 0.24) < EPSILON
    assert abs(expected[0, 2] - 0.16) < EPSILON
    assert abs(expected[1, 0] - 0) < EPSILON
    assert abs(expected[1, 1] - 0.24) < EPSILON
    assert abs(expected[1, 2] - 0.16) < EPSILON
    assert abs(expected[2, 0] - 0) < EPSILON
    assert abs(expected[2, 1] - 0.12) < EPSILON
    assert abs(expected[2, 2] - 0.08) < EPSILON


def test_calculation_on_wikipedia_example_2():
    assert (
        abs(
            kappa.main({"--filename": "test/fixtures/wikipedia_example_2.txt"}) - 0.1304
        )
        < EPSILON
    )


def test_calculation_on_wikipedia_example_3():
    assert (
        abs(
            kappa.main({"--filename": "test/fixtures/wikipedia_example_3.txt"}) - 0.2593
        )
        < EPSILON
    )


def test_calculation_on_perfect_agreement():
    assert (
        abs(kappa.main({"--filename": "test/fixtures/perfect_agreement.txt"}) - 1.0)
        < EPSILON
    )


def test_calculation_with_csvs():
    assert (
        abs(
            kappa.main(
                {"--csv": True, "--filename": "test/fixtures/comma_separated.txt"}
            )
            - 0.16
        )
        < EPSILON
    )


def test_verbose_does_not_break():
    assert (
        abs(
            kappa.main(
                {
                    "--verbose": True,
                    "--csv": True,
                    "--filename": "test/fixtures/comma_separated.txt",
                }
            )
            - 0.16
        )
        < EPSILON
    )


def test_all_zeroes_does_not_break():
    assert (
        abs(kappa.main({"--filename": "test/fixtures/all_zeroes.txt"}) - 1.0) < EPSILON
    )


def test_bad_filenames_exit():
    with pytest.raises(SystemExit):
        kappa.main({"--filename": "does_not_exist.txt"})


def test_bad_input_exits():
    with pytest.raises(IndexError):
        kappa.main({"--filename": "test/fixtures/invalid_data.txt"})

    with pytest.raises(SystemExit):
        kappa.main({"--filename": "test/fixtures/missing_data.txt"})
