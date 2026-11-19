#!/usr/bin/env python3
"""Folder tree for guide/NAVIGATION*.md, built from the real tree and the computed facts.

`render(lang, F)` walks the files git knows about (tracked or not ignored), checks that every path of the
spec exists, and aborts when a tracked top-level entry is missing from the spec, so the printed tree
cannot drift from the repository. Comments are in `en` / `ru`; `{key}` placeholders are facts.
"""
import os
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# (path, English comment, Russian comment, children)
SPEC = [
    ("README.md", "front page (English)", "главная страница (английская)"),
    ("README.ru.md", "front page (Russian)", "главная страница (русская)"),
    ("guide/", "detail pages X.md + X.ru.md; assets/ = generated SVG", "страницы-детали X.md + X.ru.md; assets/ = сгенерированные SVG"),
    ("archive/", "the previous README, kept byte for byte", "прежний README, сохранён байт в байт"),
    ("tools/", "showcase tooling: facts, visuals, excerpts, no-loss check", "инструменты витрины: факты, визуалы, выдержки, проверка без потерь"),
    ("tests/", "regression gate for the showcase", "регрессионный гейт витрины"),
    ("charts/", "{mermaid_charts} Mermaid diagrams of the plan (root_1..3.png)", "{mermaid_charts} диаграммы Mermaid плана (root_1..3.png)", [
        ("charts/mermaid/", "groups, timeline, patent link", "группы, хронология, связь с патентом"),
    ]),
    ("data/", "photos, set-up photos, incoming batch, {rct_bins} empty RCT bins", "фото, фото закладки, входящая партия, {rct_bins} пустых корзин RCT", [
        ("data/README.md", "data hub: layers and what it does not claim", "хаб данных: слои и чего он не утверждает"),
        ("data/photos/", "{photos} photos ({photos_jpeg} JPEG, {photos_heic} HEIC) + manifest.json", "{photos} фото ({photos_jpeg} JPEG, {photos_heic} HEIC) + manifest.json"),
        ("data/exp29-setup/", "{exp29_setup_files} exp29 set-up files, incl. the handwritten protocol", "{exp29_setup_files} файла закладки exp29, вкл. рукописный протокол"),
        ("data/incoming/", "batch of 2026-07-08 under review (media are git-ignored)", "партия 2026-07-08 на рассмотрении (медиа в .gitignore)"),
        ("data/control/", "RCT bins control, ch17/ch19/ch21 x 4 modes: placeholders", "корзины RCT control, ch17/ch19/ch21 x 4 режима: плейсхолдеры"),
    ]),
    ("protocols/", "exp29 protocol (Russian only)", "протокол exp29 (только на русском)"),
    ("reports/", "{reports_dated} dated analyses (EN+RU) and a percipient layer", "{reports_dated} датированных анализа (EN+RU) и перципиентный слой", [
        ("reports/2026-06-16_llm-blind-photo/", "radish: blind model panel on one frame", "редис: слепая панель моделей по одному кадру"),
        ("reports/2026-06-29_exp29-setup-observation/", "exp29 set-up observation (Russian only)", "наблюдение закладки exp29 (только на русском)"),
        ("reports/2026-07-02_microscopy-cell-structure/", "microscopy pilot, colour and cell shape", "микроскопия, пилот: цвет и форма клеток"),
        ("reports/2026-07-03_pattern-embedding-analysis/", "{frames_total} frames: embeddings, nuclei, patterns", "{frames_total} кадра: эмбеддинги, ядра, паттерны"),
        ("reports/percipient_reports/", "subjective percipient layer (participant folders not described)", "субъективный перципиентный слой (папки участников не описаны)"),
    ]),
    ("results/", "llm_blind: {llm_runs} runs and their key", "llm_blind: {llm_runs} прогонов и ключ"),
    ("scripts/", "llm_analysis: the blind-panel script", "llm_analysis: скрипт слепой панели"),
]
IGNORED_TOP = {".git", ".gitignore", ".gitattributes", ".DS_Store"}


def tracked():
    out = subprocess.run(["git", "ls-files", "-co", "--exclude-standard"], capture_output=True, text=True,
                         cwd=ROOT).stdout.split("\n")
    return [x for x in out if x]


def render(lang, F):
    files = tracked()
    tops = {x.split("/")[0] for x in files}
    spec_tops = {e[0].rstrip("/").split("/")[0] for e in SPEC}
    missing = sorted(t for t in tops - spec_tops if t not in IGNORED_TOP)
    if missing:
        raise SystemExit("tools/tree.py: tracked top-level entries missing from SPEC: %s" % missing)
    col = 1 if lang == "en" else 2
    rows = []

    def exists(path):
        q = path.rstrip("/")
        return any(f == q or f.startswith(q + "/") for f in files) or os.path.exists(os.path.join(ROOT, q))

    def emit(entries, prefix, top):
        for i, e in enumerate(entries):
            last = i == len(entries) - 1
            if not exists(e[0]):
                raise SystemExit("tools/tree.py: path in SPEC does not exist: %s" % e[0])
            name = e[0] if top else e[0].rstrip("/").split("/")[-1] + ("/" if e[0].endswith("/") else "")
            rows.append((prefix + ("└── " if last else "├── "), name, e[col].format(**F)))
            if len(e) > 3 and e[3]:
                emit(e[3], prefix + ("    " if last else "│   "), False)

    rows.append(("", "ASRP_Hyperbolic_Field_Agricultural_Study/", ""))
    emit(SPEC, "", True)
    width = max(len(a) + len(b) for a, b, c in rows if c) + 2
    out = []
    for a, b, c in rows:
        out.append((a + b).ljust(width) + "# " + c if c else a + b)
    return "\n".join(out)
