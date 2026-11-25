# VariantCurationTool

A variant curation tool classifying 820 simulated genomic variants with a
real simplified ACMG-style evidence-tracking engine, plus a gene-disease
correlation module linking variants to 14 clinical phenotype categories.

> Built variant curation tool classifying 800+ genomic variants using
> ACMG criteria with evidence tracking. Implemented gene-disease
> correlation module linking variants to 14 clinical phenotype categories.

## What's real vs. synthetic — read this first

**Real:** `src/acmg_engine.py` implements a genuine simplified ACMG
rule-combination engine (PVS1/PS1/PM2/PP3/BA1/BP4 evidence codes ->
Pathogenic/Likely_pathogenic/VUS/Likely_benign/Benign) with explicit
evidence tracking per variant. `src/gene_disease_correlation.py` computes
real per-phenotype pathogenic-variant enrichment rates across all 14
phenotype categories.

**Synthetic:** there is no real curated variant database (e.g. ClinVar) in
this environment. `src/simulate_variants.py` generates 820 variants with
randomly assigned ACMG evidence attributes and phenotype categories, and
computes a true classification from the same rule logic independently of
the curation engine, to validate that the engine correctly implements the
intended rule combination.

**Honest note on the accuracy metric:** because this is a rule-engine
*implementation-correctness* task rather than a statistical-inference
task, the simulation's "true" label and the engine's output use the same
underlying ACMG combination logic — so near-100% agreement demonstrates the
engine is correctly implemented, not that it predicts an independently-
generated biological outcome. This is disclosed rather than presented as
predictive accuracy.

## Results (real, from `run_all.py`)

```
820 variants, 14 phenotype categories
Classification accuracy (engine vs. rule-matched ground truth): 100%
Gene-disease correlation computed across all 14 phenotype categories
(per-category pathogenic-like rate ranges ~10%-25%)
```

`docs/acmg_reference.R` is an authored-but-not-executed R reference (no R
runtime is available in this environment); the real, executed methodology
is the Python mirror in `src/acmg_engine.py`.

`tests/test_pipeline.py` (5 tests, all passing) checks variant count
>=800, 14 phenotype categories, classification accuracy, evidence
tracking, and full phenotype coverage in the correlation report.

## Usage

```bash
pip install -r requirements.txt
python3 run_all.py
python3 -m pytest tests/ -v
```

## Project structure

```
src/
  simulate_variants.py          # 820-variant simulation with ACMG evidence + phenotype links
  acmg_engine.py                   # real simplified ACMG classification engine
  gene_disease_correlation.py        # per-phenotype pathogenic-variant enrichment
docs/acmg_reference.R                   # authored-but-unexecuted R reference
run_all.py
tests/test_pipeline.py
```

## Tech stack

Python 3.9+, pytest. R listed in the resume is not available in this
environment; see the disclosed reference file above.

## Limitations

- No real ClinVar/curated-variant dataset is used.
- The ACMG rule combination here is a deliberately simplified subset of
  the full ACMG/AMP 28-criteria framework.
