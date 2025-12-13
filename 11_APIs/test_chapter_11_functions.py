"""Tests for Chapter 11 business logic functions."""

import pytest
import pandas as pd
from chapter_11_functions import fit_trendline, process_sdg_data, country_trendline


def test_fit_trendline_perfect_linear():
    """Test fit_trendline with perfectly linear data."""
    timestamps = [2000, 2001, 2002, 2003, 2004]
    data = [10.0, 12.0, 14.0, 16.0, 18.0]

    slope, r_squared = fit_trendline(timestamps, data)

    assert slope == 2.0  # Slope should be exactly 2.0
    assert r_squared == 1.0  # Perfect fit should have R² = 1.0


def test_fit_trendline_positive_trend():
    """Test fit_trendline with positive trend."""
    timestamps = [2000, 2001, 2002, 2003, 2004]
    data = [10.0, 11.5, 14.5, 15.0, 18.0]

    slope, r_squared = fit_trendline(timestamps, data)

    assert slope > 0  # Should have positive slope
    assert 0 <= r_squared <= 1  # R² should be between 0 and 1
    assert isinstance(slope, float)
    assert isinstance(r_squared, float)


def test_fit_trendline_negative_trend():
    """Test fit_trendline with negative trend."""
    timestamps = [2000, 2001, 2002, 2003, 2004]
    data = [18.0, 16.0, 14.0, 12.0, 10.0]

    slope, r_squared = fit_trendline(timestamps, data)

    assert slope == -2.0  # Slope should be exactly -2.0
    assert r_squared == 1.0  # Perfect fit


def test_fit_trendline_flat_trend():
    """Test fit_trendline with flat/no trend."""
    timestamps = [2000, 2001, 2002, 2003, 2004]
    data = [15.0, 15.0, 15.0, 15.0, 15.0]

    slope, r_squared = fit_trendline(timestamps, data)

    assert slope == 0.0  # No trend
    # Note: R² is undefined for constant data, scipy handles this


def test_fit_trendline_rounding():
    """Test that fit_trendline properly rounds results to 3 decimal places."""
    timestamps = [2000, 2001, 2002, 2003, 2004, 2005, 2006]
    data = [10.123, 12.456, 14.789, 16.012, 18.345, 20.678, 22.901]

    slope, r_squared = fit_trendline(timestamps, data)

    # Check that values are rounded to 3 decimal places
    assert len(str(slope).split('.')[-1]) <= 3
    assert len(str(r_squared).split('.')[-1]) <= 3


def test_process_sdg_data():
    """Test process_sdg_data with the actual Excel file."""
    input_file = "../data/SG_GEN_PARL.xlsx"
    columns_to_drop = [
        "Goal",
        "Target",
        "Indicator",
        "SeriesCode",
        "SeriesDescription",
        "GeoAreaCode",
        "Reporting Type",
        "Sex",
        "Units",
    ]

    df = process_sdg_data(input_file, columns_to_drop)

    # Check that result is a DataFrame
    assert isinstance(df, pd.DataFrame)

    # Check that dropped columns are not in the result
    for col in columns_to_drop:
        assert col not in df.columns

    # Check that the index was transposed (years should be in index)
    assert all(isinstance(idx, str) for idx in df.index)

    # Check that DataFrame is not empty
    assert not df.empty


def test_process_sdg_data_structure():
    """Test that process_sdg_data returns properly structured data."""
    input_file = "../data/SG_GEN_PARL.xlsx"
    columns_to_drop = [
        "Goal",
        "Target",
        "Indicator",
        "SeriesCode",
        "SeriesDescription",
        "GeoAreaCode",
        "Reporting Type",
        "Sex",
        "Units",
    ]

    df = process_sdg_data(input_file, columns_to_drop)

    # After transpose, countries should be column names
    assert "Australia" in df.columns
    assert "Canada" in df.columns

    # Check that we have multiple years of data
    assert len(df.index) > 1


def test_country_trendline_australia():
    """Test country_trendline for Australia."""
    slope, r_squared = country_trendline("Australia")

    assert isinstance(slope, float)
    assert isinstance(r_squared, float)
    assert 0 <= r_squared <= 1  # R² should be between 0 and 1


def test_country_trendline_canada():
    """Test country_trendline for Canada."""
    slope, r_squared = country_trendline("Canada")

    assert isinstance(slope, float)
    assert isinstance(r_squared, float)
    assert 0 <= r_squared <= 1


def test_country_trendline_germany():
    """Test country_trendline for Germany."""
    slope, r_squared = country_trendline("Germany")

    assert isinstance(slope, float)
    assert isinstance(r_squared, float)
    assert 0 <= r_squared <= 1


def test_country_trendline_different_countries():
    """Test that different countries return different trendlines."""
    aus_slope, aus_r2 = country_trendline("Australia")
    can_slope, can_r2 = country_trendline("Canada")

    # Different countries should (likely) have different trends
    # At least one of slope or r_squared should differ
    assert (aus_slope != can_slope) or (aus_r2 != can_r2)


def test_country_trendline_invalid_country():
    """Test country_trendline with a country that doesn't exist in the data."""
    with pytest.raises(KeyError):
        country_trendline("NonexistentCountry")


# Edge Case Tests


def test_fit_trendline_two_points_minimum():
    """Test fit_trendline with minimum valid input (2 points)."""
    timestamps = [2000, 2001]
    data = [10.0, 15.0]

    slope, r_squared = fit_trendline(timestamps, data)

    assert slope == 5.0
    assert r_squared == 1.0  # Perfect fit with only 2 points


def test_fit_trendline_single_point():
    """Test fit_trendline with single data point (returns NaN)."""
    timestamps = [2000]
    data = [10.0]

    # scipy.stats.linregress doesn't raise error with 1 point, returns NaN
    slope, r_squared = fit_trendline(timestamps, data)

    # With single point, results are NaN which round to 'nan'
    assert isinstance(slope, (float, type(None))) or str(slope) == 'nan'
    assert isinstance(r_squared, (float, type(None))) or str(r_squared) == 'nan'


def test_fit_trendline_empty_lists():
    """Test fit_trendline with empty lists (should fail)."""
    timestamps = []
    data = []

    with pytest.raises(ValueError):
        fit_trendline(timestamps, data)


def test_fit_trendline_mismatched_lengths():
    """Test fit_trendline with mismatched array lengths."""
    timestamps = [2000, 2001, 2002]
    data = [10.0, 12.0]  # One fewer

    # scipy.stats.linregress should raise ValueError
    with pytest.raises(ValueError):
        fit_trendline(timestamps, data)


def test_fit_trendline_all_negative():
    """Test fit_trendline with all negative values."""
    timestamps = [2000, 2001, 2002, 2003]
    data = [-10.0, -8.0, -6.0, -4.0]

    slope, r_squared = fit_trendline(timestamps, data)

    assert slope == 2.0  # Should work correctly
    assert r_squared == 1.0


def test_fit_trendline_mixed_signs():
    """Test fit_trendline with data crossing zero."""
    timestamps = [2000, 2001, 2002, 2003, 2004]
    data = [-10.0, -5.0, 0.0, 5.0, 10.0]

    slope, r_squared = fit_trendline(timestamps, data)

    assert slope == 5.0
    assert r_squared == 1.0


def test_fit_trendline_negative_timestamps():
    """Test fit_trendline with negative timestamps."""
    timestamps = [-5, -3, -1, 1, 3]
    data = [10.0, 12.0, 14.0, 16.0, 18.0]

    slope, r_squared = fit_trendline(timestamps, data)

    assert slope == 1.0  # Slope per unit time
    assert r_squared == 1.0


def test_fit_trendline_very_large_numbers():
    """Test fit_trendline with very large numbers."""
    timestamps = [2000, 2001, 2002, 2003, 2004]
    data = [1e6, 2e6, 3e6, 4e6, 5e6]

    slope, r_squared = fit_trendline(timestamps, data)

    assert slope == 1000000.0
    assert r_squared == 1.0


def test_fit_trendline_very_small_numbers():
    """Test fit_trendline with very small numbers."""
    timestamps = [2000, 2001, 2002, 2003, 2004]
    data = [1e-6, 2e-6, 3e-6, 4e-6, 5e-6]

    slope, r_squared = fit_trendline(timestamps, data)

    # Should be rounded to 3 decimal places, might be 0.0
    assert isinstance(slope, float)
    assert r_squared == 1.0


def test_fit_trendline_all_zeros():
    """Test fit_trendline with all zero data points."""
    timestamps = [2000, 2001, 2002, 2003]
    data = [0.0, 0.0, 0.0, 0.0]

    slope, r_squared = fit_trendline(timestamps, data)

    assert slope == 0.0


def test_fit_trendline_duplicate_timestamps():
    """Test fit_trendline with duplicate timestamps."""
    timestamps = [2000, 2000, 2001, 2001]
    data = [10.0, 12.0, 14.0, 16.0]

    # Should still work - regression handles duplicates
    slope, r_squared = fit_trendline(timestamps, data)

    assert isinstance(slope, float)
    assert isinstance(r_squared, float)


def test_fit_trendline_unsorted_timestamps():
    """Test fit_trendline with unsorted timestamps."""
    timestamps = [2004, 2001, 2003, 2000, 2002]
    data = [18.0, 12.0, 16.0, 10.0, 14.0]

    slope, r_squared = fit_trendline(timestamps, data)

    # Linear regression doesn't require sorted data
    assert slope == 2.0
    assert r_squared == 1.0


def test_fit_trendline_high_variance():
    """Test fit_trendline with high variance data."""
    timestamps = [2000, 2001, 2002, 2003, 2004]
    data = [10.0, 25.0, 8.0, 30.0, 12.0]

    slope, r_squared = fit_trendline(timestamps, data)

    # Should have low R² due to high variance
    assert isinstance(slope, float)
    assert 0 <= r_squared <= 1
    assert r_squared < 0.5  # Poor fit expected


def test_process_sdg_data_empty_columns_to_drop():
    """Test process_sdg_data with empty columns_to_drop list."""
    input_file = "../data/SG_GEN_PARL.xlsx"
    columns_to_drop = []

    df = process_sdg_data(input_file, columns_to_drop)

    # Should work but retain all columns
    assert isinstance(df, pd.DataFrame)
    assert not df.empty


def test_process_sdg_data_invalid_file():
    """Test process_sdg_data with non-existent file."""
    input_file = "../data/nonexistent_file.xlsx"
    columns_to_drop = ["Goal"]

    with pytest.raises(FileNotFoundError):
        process_sdg_data(input_file, columns_to_drop)


def test_process_sdg_data_nonexistent_column():
    """Test process_sdg_data trying to drop a column that doesn't exist."""
    input_file = "../data/SG_GEN_PARL.xlsx"
    columns_to_drop = ["NonexistentColumn"]

    # pandas.drop with axis=1 will raise KeyError if column doesn't exist
    with pytest.raises(KeyError):
        process_sdg_data(input_file, columns_to_drop)


def test_country_trendline_with_spaces():
    """Test country_trendline with country name containing spaces."""
    slope, r_squared = country_trendline("New Zealand")

    assert isinstance(slope, float)
    assert isinstance(r_squared, float)
    assert 0 <= r_squared <= 1


def test_country_trendline_case_sensitivity():
    """Test that country_trendline is case-sensitive."""
    # This should fail if case doesn't match exactly
    with pytest.raises(KeyError):
        country_trendline("australia")  # lowercase


def test_country_trendline_empty_string():
    """Test country_trendline with empty string."""
    with pytest.raises(KeyError):
        country_trendline("")
