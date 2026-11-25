"""Real gene-disease correlation module: links classified variants to their
clinical phenotype category and reports per-phenotype pathogenic-variant
enrichment statistics."""
from collections import defaultdict

from .simulate_variants import PHENOTYPE_CATEGORIES


def correlate(variants: list, classifications: list) -> dict:
    class_by_id = {c["variant_id"]: c["classification"] for c in classifications}
    by_phenotype = defaultdict(lambda: {"total": 0, "pathogenic_like": 0})

    for v in variants:
        p = v["phenotype_category"]
        by_phenotype[p]["total"] += 1
        if class_by_id[v["variant_id"]] in {"Pathogenic", "Likely_pathogenic"}:
            by_phenotype[p]["pathogenic_like"] += 1

    report = {}
    for p in PHENOTYPE_CATEGORIES:
        total = by_phenotype[p]["total"]
        path = by_phenotype[p]["pathogenic_like"]
        report[p] = {"total_variants": total, "pathogenic_like_count": path,
                      "pathogenic_like_rate": round(path / total, 4) if total else 0.0}
    return report
