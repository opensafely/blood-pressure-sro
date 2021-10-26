import pandas
import pytest
from analysis import utilities
from pandas import testing
import numpy as np
from unittest.mock import patch

@pytest.fixture
def imd_measure_table_from_csv():
    """
    Returns a measure table that could have been read from a CSV file.
    """
    return pandas.DataFrame(
        {
            "imd": pandas.Series([1, 2, 3, 4, 5, 1, 2, 3, 4, 5]),
            "event": pandas.Series([0, 1, 1, 0, 1, 0, 1, 1, 0, 1]),
            "population": pandas.Series([1, 1, 1, 1, 1, 1, 1, 1, 1, 1]),
            "value": pandas.Series([0, 1, 1, 0, 1, 0, 1, 1, 0, 1]),
            "date": pandas.to_datetime(pandas.Series(
                [
                    "2019-01-01",
                    "2019-01-01",
                    "2019-01-01",
                    "2019-01-01",
                    "2019-01-01",
                    "2019-02-01",
                    "2019-02-01",
                    "2019-02-01",
                    "2019-02-01",
                    "2019-02-01",
                ]
            )),
        }
    )

@pytest.fixture
def measure_table():
    """Returns a measure table."""
    mt = pandas.DataFrame(
        {   
            "event_code": pandas.Series([1, 1, 2, 1]),
            "practice": pandas.Series([1, 2, 3, 4]),
            "group": pandas.Categorical(['A', 'B', 'A', 'B']),
            "event": pandas.Series([0, 6, 3, 7]),
            "population": pandas.Series([10, 10, 10, 10]),
            "value": pandas.Series([0/10, 6/10, 3/10, 7/10]),
            "date": pandas.Series(["2019-01-01", "2019-01-01", "2019-02-01", "2019-02-01"]),
        }
    )
    mt["date"] = pandas.to_datetime(mt["date"])
    return mt

@pytest.fixture
def codelist_table_from_csv():
    """Returns a codelist table the could have been read from a CSV file."""
    return pandas.DataFrame(
        {
            "code": pandas.Series([1, 2]),
            "term": pandas.Series(["Code 1", "Code 2"]),
        }
    )

@pytest.fixture
def practice_count_table():
    """
    Returns a practice count table that could have been read from a CSV file.
    """
    return pandas.DataFrame(
        {
            "practice": pandas.Series([1, 2, 3, 4, 5]),
            "patient_id": pandas.Series([1, 2, 3, 4, 5]),
        }
    ) 

def test_calculate_imd_group(imd_measure_table_from_csv):


    obs = utilities.calculate_imd_group(imd_measure_table_from_csv, 'event', 'value')
    
    exp = pandas.DataFrame(
        {
            "imd": pandas.Categorical(['Most deprived', '2', '3', '4', 'Least deprived', 'Most deprived', '2', '3', '4', 'Least deprived'], ordered=True).reorder_categories(['Most deprived', '2', '3', '4', 'Least deprived']),
            "event": pandas.Series([0, 1, 1, 0, 1, 0, 1, 1, 0, 1]),
            "population": pandas.Series([1, 1, 1, 1, 1, 1, 1, 1, 1, 1]),
            "value": pandas.Series([0, 1, 1, 0, 1, 0, 1, 1, 0, 1]),
            "date": pandas.to_datetime(pandas.Series(
                [
                    "2019-01-01",
                    "2019-01-01",
                    "2019-01-01",
                    "2019-01-01",
                    "2019-01-01",
                    "2019-02-01",
                    "2019-02-01",
                    "2019-02-01",
                    "2019-02-01",
                    "2019-02-01",
                ]
            )),
        }
    )
    testing.assert_frame_equal(obs, exp)

def test_redact_small_numbers(measure_table):
    obs = utilities.redact_small_numbers(measure_table, 5, 'event', 'population', 'value')
    
    exp = pandas.DataFrame(
        {   
            "event_code": pandas.Series([1, 1, 2, 1]),
            "practice": pandas.Series([1, 2, 3, 4]),
            "group": pandas.Categorical(['A', 'B', 'A', 'B']),
            "event": pandas.Series([np.nan, np.nan, np.nan, 7]),
            "population": pandas.Series([10, 10, 10, 10]),
            "value": pandas.Series([np.nan, np.nan, np.nan, 0.7]),
            "date": pandas.to_datetime(pandas.Series(
                [
                    "2019-01-01",
                    "2019-01-01",
                    "2019-02-01",
                    "2019-02-01",
                ]
            )),
        }
    )
    
    testing.assert_frame_equal(obs, exp)

class TestDropIrrelevantPractices:
    def test_irrelevant_practices_dropped(self, measure_table):
        obs = utilities.drop_irrelevant_practices(measure_table, 'practice')
        
        # Practice ID #1, which is irrelevant, has been dropped from
        # the measure table.
        assert all(obs.practice.values == [2, 3, 4])

    def test_return_copy(self, measure_table):
        obs = utilities.drop_irrelevant_practices(measure_table, 'practice')
        assert id(obs) != id(measure_table)


def test_create_child_table(measure_table, codelist_table_from_csv):
    obs = utilities.create_child_table(
        measure_table,
        codelist_table_from_csv,
        "code",
        "term",
    )

   
    exp = pandas.DataFrame(
        [
            {
                "code": 1,
                "Events": 13,
                "Events (thousands)": 0.013,
                "Description": "Code 1",
            },
            {
                "code": 2,
                "Events": 3,
                "Events (thousands)": 0.003,
                "Description": "Code 2",
            },
        ],
    )

   
    testing.assert_frame_equal(obs, exp)

def test_get_number_practices(measure_table):
    assert utilities.get_number_practices(measure_table) == 4

def test_get_percentage_practices(tmp_path, practice_count_table, measure_table):
        with patch.object(utilities, "OUTPUT_DIR", tmp_path):
            
            f_name = f"input_practice_count_2021-01-01.csv"
            practice_count_table.to_csv(utilities.OUTPUT_DIR / f_name)

            obs = utilities.get_percentage_practices(measure_table)
            
            assert obs == 80