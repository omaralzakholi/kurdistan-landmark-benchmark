# Kurdistan Landmark Benchmark

Replication package for the manuscript *"Invisible Landscapes: AI as a Failed Cultural Broker for
Kurdistan and Its Transnational Communities"* (under review, *Discourses on Culture*; author details
will be added upon acceptance).

The study audits how vision-language models (CLIP ViT-L/14, SigLIP so400m, Qwen2.5-VL 7B/3B)
recognize 39 natural and cultural landmarks of the Kurdistan Region of Iraq, each matched to a
Western landmark of the same physical type and evaluated under an identical protocol.

## Contents

| Path | What it is |
|---|---|
| `data/sites_kurdistan.csv` | The 39 Kurdish sites: type category, accepted name aliases, approximate coordinates |
| `data/pairs.csv` | The 39 matched Kurdish-Western landmark pairs and control countries |
| `data/aliases.json` | Alias lists used by the fuzzy scoring (both regions) |
| `data/prompts.md` | Verbatim prompts, scoring rules, decoding settings |
| `results/` | All model outputs and scored results: closed-set (CLIP/SigLIP), generative responses (7B and 3B), country-hint condition, evaluation manifest, Wikipedia prominence, summary table |
| `code/geo_bias_vlm_study.ipynb` | Full pipeline: control-set collection, evaluation, scoring, statistics, figures |
| `code/dataset_builder.ipynb` | Benchmark image collection and curation pipeline (search, dedup, CLIP filter, watermark screening) |
| `code/paired_bootstrap.py` | Independent and paired cluster-bootstrap confidence intervals (reproduces Table 2 and the robustness check) |
| `code/make_map_figure.py` | Builds the site/reassignment map (Figure 3) |
| `figures/` | The manuscript figures |

## Photographs are not included

The evaluation photographs were collected by web image search and are not ours to redistribute.
This repository therefore shares the benchmark as **reproducible metadata**: the site list, aliases,
search pipeline (`code/dataset_builder.ipynb`), curation rules, and the per-image evaluation
manifest. Running the builder notebook reconstructs a comparable image set; all numbers in the
paper can be regenerated from the released response logs in `results/` without any images.

## Reproducing the paper's numbers

```bash
pip install -r code/requirements.txt
cd code
python paired_bootstrap.py      # Table 2 point estimates + independent & paired bootstrap CIs
python make_map_figure.py       # Figure 3 map
```

The notebook `geo_bias_vlm_study.ipynb` reruns the full evaluation (requires a GPU; models are
loaded with 4-bit NF4 quantization and greedy decoding; all runs are resumable and seeded).

## Licenses

- Code: MIT (see `LICENSE`).
- Metadata, prompts, and result files: CC BY 4.0.
- `code/countries.geo.json`: country boundaries derived from Natural Earth (public domain).
- Site coordinates are approximate and for orientation only.
