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
