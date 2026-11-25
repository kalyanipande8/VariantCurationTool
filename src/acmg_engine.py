"""Real simplified ACMG-style variant classification engine with evidence
tracking (the real curation logic under test, kept separate from the
simulation's independent ground-truth generator)."""


def classify_variant(variant: dict) -> dict:
    evidence_applied = [code for code in ["PVS1", "PS1", "PM2", "PP3", "BA1", "BP4"] if variant.get(code)]

    if variant.get("PVS1") and (variant.get("PS1") or variant.get("PM2")):
        classification = "Pathogenic"
    elif variant.get("BA1"):
        classification = "Benign"
    elif variant.get("PS1") or (variant.get("PM2") and variant.get("PP3")):
        classification = "Likely_pathogenic"
    elif variant.get("BP4") and not variant.get("PM2"):
        classification = "Likely_benign"
    else:
        classification = "VUS"

    return {"variant_id": variant["variant_id"], "classification": classification,
            "evidence_applied": evidence_applied}


def classify_all(variants: list) -> list:
    return [classify_variant(v) for v in variants]


def validate_classifications(classifications: list, variants: list) -> dict:
    truth_by_id = {v["variant_id"]: v["true_class"] for v in variants}
    correct = sum(1 for c in classifications if c["classification"] == truth_by_id[c["variant_id"]])
    return {"n_variants": len(classifications), "n_correct": correct,
            "accuracy": round(correct / len(classifications), 4)}
