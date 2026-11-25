"""Simulate 800+ genomic variants with ACMG-relevant evidence attributes and
a hidden true classification generated independently of the curation
engine, plus links to 14 clinical phenotype categories."""
import random

PHENOTYPE_CATEGORIES = [
    "cardiomyopathy", "hereditary_cancer", "neurodevelopmental_disorder", "epilepsy",
    "retinal_dystrophy", "hearing_loss", "skeletal_dysplasia", "immunodeficiency",
    "metabolic_disorder", "renal_disease", "connective_tissue_disorder", "mitochondrial_disease",
    "coagulation_disorder", "neuromuscular_disease",
]
assert len(PHENOTYPE_CATEGORIES) == 14

GENES_BY_PHENOTYPE = {p: [f"{p[:4].upper()}{i}" for i in range(1, 4)] for p in PHENOTYPE_CATEGORIES}


def simulate_variants(n_variants: int = 820, seed: int = 41):
    rng = random.Random(seed)
    variants = []
    for i in range(n_variants):
        phenotype = rng.choice(PHENOTYPE_CATEGORIES)
        gene = rng.choice(GENES_BY_PHENOTYPE[phenotype])

        # ACMG-relevant evidence attributes (independent ground-truth generation)
        pvs1 = rng.random() < 0.1   # null variant in LOF gene
        ps1 = rng.random() < 0.08   # same amino acid change as established pathogenic
        pm2 = rng.random() < 0.3    # absent/rare in population databases
        pp3 = rng.random() < 0.35   # computational evidence supports deleterious
        ba1 = rng.random() < 0.15   # high population frequency (benign)
        bp4 = rng.random() < 0.2    # computational evidence suggests benign

        # true classification driven by a simplified ACMG-style rule, independent of curation engine
        if pvs1 and (ps1 or pm2):
            true_class = "Pathogenic"
        elif ba1:
            true_class = "Benign"
        elif ps1 or (pm2 and pp3):
            true_class = "Likely_pathogenic"
        elif bp4 and not pm2:
            true_class = "Likely_benign"
        else:
            true_class = "VUS"

        variants.append({
            "variant_id": i, "gene": gene, "phenotype_category": phenotype,
            "PVS1": pvs1, "PS1": ps1, "PM2": pm2, "PP3": pp3, "BA1": ba1, "BP4": bp4,
            "true_class": true_class,
        })
    return variants
