import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.simulate_variants import simulate_variants, PHENOTYPE_CATEGORIES
from src.acmg_engine import classify_all, validate_classifications
from src.gene_disease_correlation import correlate


def test_at_least_800_variants():
    assert len(simulate_variants(n_variants=820)) >= 800


def test_14_phenotype_categories():
    assert len(PHENOTYPE_CATEGORIES) == 14


def test_classification_accuracy_high():
    variants = simulate_variants(n_variants=820)
    classifications = classify_all(variants)
    validation = validate_classifications(classifications, variants)
    assert validation["accuracy"] >= 0.95


def test_evidence_tracking_present():
    variants = simulate_variants(n_variants=50, seed=2)
    classifications = classify_all(variants)
    assert all("evidence_applied" in c for c in classifications)


def test_correlation_covers_all_phenotypes():
    variants = simulate_variants(n_variants=820)
    classifications = classify_all(variants)
    report = correlate(variants, classifications)
    assert set(report.keys()) == set(PHENOTYPE_CATEGORIES)
