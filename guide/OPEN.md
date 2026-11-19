**English | [Русский](OPEN.ru.md)**

[← Hyperbolic Field Agricultural Study](../README.md) · [Guide index](README.md)

<div align="center">

# Open questions

</div>

## What needs the owner or the researcher

These are gaps and inconsistencies found while restructuring. Source files were **not** changed to fix them.

1. **The protocol text is not here.** Protocol v8.3 is called complete, but its text is not in the repository (only the exp29 protocol is). The goal ranges and the <!--n:seeds_total-->15,600<!--/n-->-seed design cannot be traced to it. (`README.md:58`)
2. **Status header lags the work.** The previous README is dated July 2026 and reads "Protocol Complete, Equipment Setup Pending", while exp29, the microscopy reports and the radish panel are already in the repository; the emitter hardware is not described anywhere. (`README.md:362`)
3. **"No quantitative results" versus reports with numbers.** The README says none exist, while three reports give numbers. They are pilot proxies, not RCT results, but the README does not mention the reports; the git history shows analytics were removed from the README on purpose on 2026-06-15 for an appearance-only scope. (`README.md:60`)
4. **Microscopy frame count.** The 2026-07-02 report says <!--n:micro_report_frames-->8<!--/n--> frames (3 control, 5 treated), but `blind_key.tsv` has <!--n:micro_key_rows-->9<!--/n--> rows (<!--n:micro_key_control-->3<!--/n--> control, <!--n:micro_key_treated-->6<!--/n--> treated), and the incoming notes say the report used 9. (`reports/2026-07-02_microscopy-cell-structure/blind_key.tsv`)
5. **The radish frame is not in the photo manifest.** The frame is named `microgreens_2026-05-11.jpg` and sits in the report folder; the <!--n:photos-->23<!--/n-->-photo manifest covers <!--n:photo_first-->2026-05-02<!--/n--> to <!--n:photo_last-->2026-06-10<!--/n--> and has no radish entry. (`reports/2026-06-16_llm-blind-photo/charts/microgreens_2026-05-11.jpg`)
6. **Exp29 and an "experiment 17".** The exp29 set-up report mentions a separate sowing mixed into the same photo set, with no protocol in the repository; the macro photos carry three group-coding systems. (`reports/2026-06-29_exp29-setup-observation/report_ru.md:25`)
7. **Which crystal?** The crystal arm (G7) does not say which crystal is used, nor whether it is the DAAT crystal of the sibling study. (`README.md:121`)
8. **Patent status.** The previous README says "substantive examination"; the repository has no independent confirmation, and it names no applicants (see [IP, team and ecosystem](ECOSYSTEM.md#patent-connection)). (`README.md:241`)
9. **Hot-linked diagrams.** The old front page loaded its three diagrams from an older public repository name; the showcase points to the committed files instead. (`README.md:129`)
10. **Which folders are on which security level.** The 4-level classification is stated, but no folder is assigned a level. (`README.md:303`)
11. **Planned versus real schedule.** Phase issues #4 to #8 are open with Q2-Q3 2026 due dates and the plan diagram expects the main experiment to start in June 2026; the repository records no main experiment. (`README.md:100`)
12. **Percipient layer.** Whether participants consented to being referred to in this (public) repository is not recorded here; the files are not described on these pages. (`reports/percipient_reports/`)
13. **GitHub issues.** The issue table was copied from the previous README; the issues were not re-read.

## Not verified by the showcase

The 52-frame result was recomputed from the committed `per_frame_metrics.json` only (medians); no analysis script was run. Images other than the three plan diagrams and one handwritten protocol photo were not inspected one by one. The 20 MB first-day video is git-ignored and absent. External tools named in the reports (a vision model, DINOv2, Cellpose, LeafNet) were not re-run.
