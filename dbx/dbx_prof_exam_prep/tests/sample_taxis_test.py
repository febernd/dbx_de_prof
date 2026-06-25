"""Tests for the taxis module."""
from dbx_prof_exam_prep import taxis


def test_find_all_taxis():
    """Test the find_all_taxis function."""
    results = taxis.find_all_taxis()
    assert results.count() > 5
