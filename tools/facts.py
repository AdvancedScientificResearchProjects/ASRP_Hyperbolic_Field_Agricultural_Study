#!/usr/bin/env python3
"""Every number on the showcase pages and diagrams is computed here, from the repository itself.

    python3 tools/facts.py            # print all facts

`facts()` returns a flat dict of strings. tools/build_facts.py writes them into the pages
(markers `<!--n:key-->value<!--/n-->`); tools/build_visuals.py draws the diagrams from the same dict.
Nothing is copied from older prose: counts come from the file tree, `data/photos/manifest.json`,
`results/llm_blind/runs.json`, `reports/*/data/per_frame_metrics.json` and a few anchored regular
expressions on the archived README (the build fails if a sentence they read has changed).
Standard library only.
"""
import glob
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AS_OF = "2026-11-19"  # date of this showcase restructuring
ARCHIVE = "archive/README_2026-11-19_pre-showcase.md"


def p(*a):
    return os.path.join(ROOT, *a)


def read(rel):
    return open(p(rel), encoding="utf-8").read()


def must(pattern, text, what, flags=0):
    m = re.search(pattern, text, flags)
    if not m:
        raise SystemExit("facts.py: cannot find %s (pattern %r) - the source sentence changed" % (what, pattern))
    return m


def ru_plural(n, one, few, many):
    n = abs(int(n))
    if n % 10 == 1 and n % 100 != 11:
        return one
    if 2 <= n % 10 <= 4 and not 12 <= n % 100 <= 14:
        return few
    return many


def facts():
    f = {"as_of": AS_OF}
    f["repo_name"] = os.path.basename(ROOT)
    arch = read(ARCHIVE)

    # photo set
    man = json.load(open(p("data", "photos", "manifest.json"), encoding="utf-8"))
    f["photos"] = str(len(man))
    f["photos_jpeg"] = str(sum(1 for x in man if x["format"] == "JPEG"))
    f["photos_heic"] = str(sum(1 for x in man if x["format"] == "HEIC"))
    f["photo_first"] = min(x["date_observed"] for x in man)
    f["photo_last"] = max(x["date_observed"] for x in man)
    f["photos_labelled"] = str(sum(1 for x in man if x.get("group_label")))
    f["exp29_setup_files"] = str(len([x for x in glob.glob(p("data", "exp29-setup", "*")) if not x.endswith(".md")]))

    # RCT bins (placeholders)
    bins = [d for d in glob.glob(p("data", "*")) if os.path.isdir(d)
            and (os.path.basename(d) == "control" or re.match(r"ch\d+-(direct|water|crystal|combined)$", os.path.basename(d)))]
    f["rct_bins"] = str(len(bins))
    f["rct_bins_empty"] = str(sum(1 for d in bins if not [x for x in os.listdir(os.path.join(d, "photos")) if x != ".gitkeep"]))
    f["channels"] = str(len({re.match(r"ch(\d+)", os.path.basename(d)).group(1) for d in bins if os.path.basename(d) != "control"}))
    f["modes"] = str(len({os.path.basename(d).split("-")[1] for d in bins if os.path.basename(d) != "control"}))

    # design numbers: read from the archived README, cross-checked
    f["crops"] = must(r"across (\d+) crop varieties|на (\d+) видах культур", arch, "crops").group(1) or "6"
    f["substrates"] = str(len(re.findall(r"^\| \*\*S\d\*\*", arch, re.M)))
    f["goals"] = str(len(re.findall(r"^\| \*\*G\d\*\*", arch, re.M)))
    f["seeds_per_group"] = must(r"\*\*Seeds per Group[^|]*\| (\d+)", arch, "seeds per group").group(1)
    f["seeds_total"] = must(r"\*\*Total Seeds[^|]*\| ([\d,]+)", arch, "total seeds").group(1)
    if int(f["seeds_total"].replace(",", "")) != int(f["rct_bins"]) * int(f["seeds_per_group"]) * int(f["crops"]):
        raise SystemExit("facts.py: seeds total no longer equals groups x seeds x crops")
    f["protocol_version"] = must(r"\*\*Protocol Version[^|]*\| (v[\d.]+)", arch, "protocol version").group(1)
    f["issues_total"] = str(len(re.findall(r"^\| \[#\d+\]", arch, re.M)))
    f["issues_open"] = str(len(re.findall(r"^\| \[#\d+\].*Open / Открыто", arch, re.M)))
    f["issues_done"] = str(len(re.findall(r"^\| \[#\d+\].*Complete / Завершено", arch, re.M)))
    f["team_size"] = str(len(re.findall(r"^\| \*\*[^|]+ / [^|]+\*\* \| ", arch.split("## RESEARCH TEAM")[1].split("## ACTIVE")[0], re.M)))

    # reports
    dated = sorted(d for d in os.listdir(p("reports")) if re.match(r"\d{4}-\d{2}-\d{2}_", d))
    f["reports_dated"] = str(len(dated))
    f["reports_first"], f["reports_last"] = dated[0][:10], dated[-1][:10]
    f["report_files"] = str(len(glob.glob(p("reports", "20*", "report_*.md"))))
    f["analysis_scripts"] = str(len(glob.glob(p("reports", "*", "scripts", "*.py"))) + len(glob.glob(p("scripts", "*", "*.py"))))

    # one-frame blind LLM panel
    r = json.load(open(p("results", "llm_blind", "runs.json"), encoding="utf-8"))
    f["llm_runs"] = str(len(r["runs"]))
    f["llm_correct"] = str(sum(1 for x in r["runs"] if x["correct"]))
    f["llm_conf"] = str(round(sum(x["confidence"] for x in r["runs"]) / len(r["runs"])))
    f["llm_per_orientation"] = str(sum(1 for x in r["runs"] if x["orientation"] == "A"))
    f["llm_families"] = str(r["meta"]["model_families"])

    # 52-frame microscopy set
    m = json.load(open(p("reports", "2026-07-03_pattern-embedding-analysis", "data", "per_frame_metrics.json"), encoding="utf-8"))
    f["frames_control"], f["frames_treated"] = str(len(m["control"])), str(len(m["treated"]))
    f["frames_total"] = str(len(m["control"]) + len(m["treated"]))
    key = [ln for ln in read("reports/2026-07-02_microscopy-cell-structure/blind_key.tsv").split("\n")[1:] if ln.strip()]
    f["micro_key_rows"] = str(len(key))
    f["micro_key_control"] = str(sum(1 for k in key if k.endswith("control")))
    f["micro_key_treated"] = str(len(key) - int(f["micro_key_control"]))
    rep = read("reports/2026-07-02_microscopy-cell-structure/report_en.md")
    f["micro_report_frames"] = must(r"\*\*Dataset\*\*: (\d+) unique", rep, "microscopy frame count").group(1)
    pk = [ln for ln in read("reports/percipient_reports/BLIND_KEY_plant_round1.tsv").split("\n")[1:] if ln.strip()]
    f["plant_key_rows"] = str(len(pk))
    f["mermaid_charts"] = str(len(glob.glob(p("charts", "mermaid", "*.png"))))
    f["md_content_pages"] = str(len([x for x in glob.glob(p("**", "*.md"), recursive=True)
                                     if not re.match(r"(archive|guide|\.git)/", os.path.relpath(x, ROOT))
                                     and os.path.relpath(x, ROOT) not in ("README.md", "README.ru.md")]))
    for key_, forms in (("photos", ("фото", "фото", "фото")), ("llm_runs", ("прогон", "прогона", "прогонов")),
                        ("frames_total", ("кадр", "кадра", "кадров"))):
        f[key_ + "_ru"] = "%s %s" % (f[key_], ru_plural(f[key_], *forms))
    return f


def badges(lang, F):
    """Computed shields.io badges for the README header (the URL carries the numbers)."""
    from urllib.parse import quote
    names = {"en": ("RCT results", "pilot photos", "RCT bins empty"),
             "ru": ("результатов RCT", "пилотных фото", "пустых корзин RCT")}[lang]
    items = [(names[0], "0", "d9534f", "No RCT results"), (names[1], F["photos"], "1f6feb", "Photos"),
             (names[2], "%s of %s" % (F["rct_bins_empty"], F["rct_bins"]), "8957e5", "Empty RCT bins")]
    return "\n".join("![%s](https://img.shields.io/badge/%s-%s-%s?style=flat-square)"
                     % (alt, quote(label.replace("-", "--").replace(" ", "_"), safe="_-"),
                        quote(msg.replace("-", "--").replace(" ", "_"), safe="_-"), col)
                     for label, msg, col, alt in items)


if __name__ == "__main__":
    for k, v in facts().items():
        print("%-28s %s" % (k, v))
