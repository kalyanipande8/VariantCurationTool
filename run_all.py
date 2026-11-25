import json
import os

from src.simulate_variants import simulate_variants, PHENOTYPE_CATEGORIES
from src.acmg_engine import classify_all, validate_classifications
from src.gene_disease_correlation import correlate


def main():
    variants = simulate_variants(n_variants=820)
    classifications = classify_all(variants)
    validation = validate_classifications(classifications, variants)
    correlation_report = correlate(variants, classifications)

    os.makedirs("results", exist_ok=True)
    summary = {"n_variants": len(variants), "n_phenotype_categories": len(PHENOTYPE_CATEGORIES),
               "classification_accuracy": validation, "gene_disease_correlation": correlation_report}
    with open("results/summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
