**English | [Русский](NAVIGATION.ru.md)**

[← Hyperbolic Field Agricultural Study](../README.md) · [Guide index](README.md)

<div align="center">

# Navigation and structure

</div>

## Where things are

| You want | Go to |
|---|---|
| What the study is and plans | [The study](STUDY.md), [The plan](DESIGN.md) |
| The raw observations | `data/photos/` (<!--n:photos-->23<!--/n--> photos, `manifest.json`), `data/exp29-setup/` |
| What was analysed | `reports/` (<!--n:reports_dated-->4<!--/n--> dated analyses; EN and RU pairs except one Russian-only report), `results/llm_blind/` |
| The one protocol that exists as a file | `protocols/2026-06-29_exp29-irradiated-germination.md` (Russian only) |
| The code | `scripts/llm_analysis/run_blind_panel.py` and the `scripts/` folders inside the reports (<!--n:analysis_scripts-->10<!--/n--> Python files in total) |
| Plan diagrams | `charts/mermaid/root_1.png` to `root_3.png` |
| The previous README | `archive/README_2026-11-19_pre-showcase.md` |

## Data structure

The folder layout of the data hub is two layers: a flat `photos/` set that is the canonical raw record, and <!--n:rct_bins-->13<!--/n--> protocol-aligned bins that are an analytical projection, empty until the researcher attributes photos to treatments. The layout below is the one given by the previous README.

```
Hyperbolic_Field_Agricultural_Study/
|
|-- README.md
|
|-- data/
|   |-- README.md                      # Data hub
|   |-- photos/                        # Flat photo set + manifest
|   |   |-- README.md
|   |   |-- manifest.json
|   |   |-- original/                  # HEIC originals / HEIC-оригиналы
|   |   `-- jpg/                       # JPEG previews
|   |-- control/                       # Control group C0
|   |   `-- photos/
|   |-- ch17-direct/                   # Channel 17 direct exposure
|   |   `-- photos/
|   |-- ch17-water/                    # Channel 17 water treatment
|   |   `-- photos/
|   |-- ch17-crystal/                  # Channel 17 crystal treatment
|   |   `-- photos/
|   |-- ch17-combined/                 # Channel 17 combined
|   |   `-- photos/
|   |-- ch19-direct/                   # Channel 19 direct
|   |   `-- photos/
|   |-- ch19-water/
|   |   `-- photos/
|   |-- ch19-crystal/
|   |   `-- photos/
|   |-- ch19-combined/
|   |   `-- photos/
|   |-- ch21-direct/                   # Channel 21 direct
|   |   `-- photos/
|   |-- ch21-water/
|   |   `-- photos/
|   |-- ch21-crystal/
|   |   `-- photos/
|   |-- ch21-combined/
|   |   `-- photos/
|   |-- exp29-setup/                   # Exp29 setup photos + handwritten protocol
|   `-- incoming/                      # Newly arrived batches under review
|       `-- 2026-07-08_earlier-samples/
|
|-- charts/                            # Mermaid diagrams (root_1..3.png)
|-- protocols/                         # Experiment protocols (v8.3)
|-- reports/                           # Dated analysis reports (EN+RU pairs)
|-- results/                           # Derived results (e.g. llm_blind)
`-- scripts/                           # Analysis code (llm_analysis)
```

See **[data/README.md](../data/README.md)**, the data hub indexing the flat photo set in `data/photos/` and the RCT-aligned channel/mode bins.

## The folder tree today

The tree below is generated from the real file list (`tools/tree.py`), so it cannot drift from the repository.

<!-- tree -->
```
ASRP_Hyperbolic_Field_Agricultural_Study/
├── README.md                                   # front page (English)
├── README.ru.md                                # front page (Russian)
├── guide/                                      # detail pages X.md + X.ru.md; assets/ = generated SVG
├── archive/                                    # the previous README, kept byte for byte
├── tools/                                      # showcase tooling: facts, visuals, excerpts, no-loss check
├── tests/                                      # regression gate for the showcase
├── charts/                                     # 3 Mermaid diagrams of the plan (root_1..3.png)
│   └── mermaid/                                # groups, timeline, patent link
├── data/                                       # photos, set-up photos, incoming batch, 13 empty RCT bins
│   ├── README.md                               # data hub: layers and what it does not claim
│   ├── photos/                                 # 23 photos (18 JPEG, 5 HEIC) + manifest.json
│   ├── exp29-setup/                            # 17 exp29 set-up files, incl. the handwritten protocol
│   ├── incoming/                               # batch of 2026-07-08 under review (media are git-ignored)
│   └── control/                                # RCT bins control, ch17/ch19/ch21 x 4 modes: placeholders
├── protocols/                                  # exp29 protocol (Russian only)
├── reports/                                    # 4 dated analyses (EN+RU) and a percipient layer
│   ├── 2026-06-16_llm-blind-photo/             # radish: blind model panel on one frame
│   ├── 2026-06-29_exp29-setup-observation/     # exp29 set-up observation (Russian only)
│   ├── 2026-07-02_microscopy-cell-structure/   # microscopy pilot, colour and cell shape
│   ├── 2026-07-03_pattern-embedding-analysis/  # 52 frames: embeddings, nuclei, patterns
│   └── percipient_reports/                     # subjective percipient layer (private; participant folders not described)
├── results/                                    # llm_blind: 10 runs and their key
└── scripts/                                    # llm_analysis: the blind-panel script
```
<!-- /tree -->

## House rules of the showcase

- Only `README.md` was rewritten; `README.ru.md`, `guide/`, `tools/`, `tests/` and `archive/` were added. No existing file was moved, edited or deleted; Git LFS files were not touched.
- Numbers on these pages are computed from the repository by `tools/build_facts.py` (invisible markers in the Markdown source).
- Diagrams come from `tools/build_visuals.py`; every picture has an English and a Russian twin.
- `python3 tools/verify_no_loss.py` checks the new pages against the archived README; `python3 -m unittest discover -s tests` runs the regression gate.
