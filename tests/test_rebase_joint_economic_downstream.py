"""Regression checks for the retained frozen-input economic post-processing."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import frozen_physical_inputs as inputs
import rebase_joint_economic_downstream as rebase


def test_frozen_physical_matrix_is_complete() -> None:
    rows = inputs.canonical_physical_rows()
    assert len(rows) == 672


def test_recalculation_matches_retained_downstream_outputs() -> None:
    source = pd.read_csv(rebase.SOURCE).fillna("")
    prices = rebase.price_index()
    physical = rebase.canonical_physical()
    rebase.validate_reference_reconstruction(source, physical, prices)
    service, horizon, horizon_summary = rebase.service_and_horizon(source)
    availability = rebase.availability_sensitivity(physical, prices, source)
    optical, optical_summary, interaction = rebase.optical_sensitivity(physical, rebase.optical_physical(), prices, source)
    expected = {
        "central_service_burden_thresholds.csv": service,
        "central_horizon_discount_sensitivity.csv": horizon,
        "central_horizon_discount_summary.csv": horizon_summary,
        "central_cold_season_availability_sensitivity.csv": availability,
        "central_optical_function_sensitivity.csv": optical,
        "central_optical_function_summary.csv": optical_summary,
        "central_optical_availability_interaction.csv": interaction,
    }
    for name, calculated in expected.items():
        retained = pd.read_csv(rebase.OUT / name)
        assert list(calculated.columns) == list(retained.columns)
        assert calculated.shape == retained.shape
        for column in calculated.columns:
            if pd.api.types.is_numeric_dtype(calculated[column]):
                assert np.allclose(calculated[column], retained[column], rtol=0, atol=1e-10)
            else:
                assert (calculated[column].fillna("").astype(str).to_numpy() == retained[column].fillna("").astype(str).to_numpy()).all()
