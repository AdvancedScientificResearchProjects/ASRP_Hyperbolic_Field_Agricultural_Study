#!/usr/bin/env python3
"""Generates the showcase visuals of the Hyperbolic Field Agricultural Study (never hand-edit the SVG
output; edit this file).

    python3 tools/build_visuals.py

Output (English and Russian twin for every picture)
    guide/assets/banner/hero-banner.{en,ru}.svg           generated illustration, not a screenshot
    guide/assets/diagrams/design-matrix.{en,ru}.svg       the 13 RCT groups and how many photos each holds (zero)
    guide/assets/diagrams/claimed-vs-shown.{en,ru}.svg    what the plan and README claim vs what the files show
    guide/assets/diagrams/timeline.{en,ru}.svg            planned schedule vs what actually happened
    guide/assets/diagrams/evidence-ladder.{en,ru}.svg     from plan to RCT result: which rungs exist
    guide/assets/diagrams/family-map.{en,ru}.svg          where the study sits in the hyperbolic-field family
    guide/assets/icons/*.svg                              navigation icons

Every number printed on a picture comes from tools/facts.py (computed from the repository at build time).
Every date on the timeline is checked against the repository text it is taken from, and the build aborts
when it is missing. Rules (ASRP visual standard): <title>, <desc>, viewBox on every SVG; text is measured
and must fit its container (the build aborts otherwise); a status is a word paired with a shape, never
colour alone; one token set (tools/svgkit.py).
"""
import glob
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svgkit import *  # noqa: E402,F401,F403  (tokens, text(), Canvas, write(), ...)
import facts as factsmod  # noqa: E402

F = factsmod.facts()


def fmt(s):
    return s.format(**F)


# a state is always a word paired with a shape (never colour alone)
STATE = {
    "en": {"plan": ("◇ PLANNED ONLY", VIOLET), "pilot": ("◧ PILOT ONLY", GOLD), "none": ("✕ NONE YET", AMBER),
           "obs": ("◧ OBSERVATION", GOLD), "weak": ("◧ NOT CONFIRMED", GOLD), "done": ("■ DONE", GREEN)},
    "ru": {"plan": ("◇ ТОЛЬКО ПЛАН", VIOLET), "pilot": ("◧ ТОЛЬКО ПИЛОТ", GOLD), "none": ("✕ ПОКА НЕТ", AMBER),
           "obs": ("◧ НАБЛЮДЕНИЕ", GOLD), "weak": ("◧ НЕ ПОДТВЕРЖДЕНО", GOLD), "done": ("■ СДЕЛАНО", GREEN)},
}


def foot(cv, parts, bottom, color=MUTED, weight=400):
    lines = []
    for p in ([parts] if isinstance(parts, str) else parts):
        lines += wrap(p, FS_SMALL, cv.w - 48, weight >= 600)
    y = bottom - 20 * (len(lines) - 1)
    for i, ln in enumerate(lines):
        cv.label(24, y + 20 * i, ln, FS_SMALL, color, weight=weight, box=cv.w - 48)


CHANNELS = ["17", "19", "21"]
MODES = {"en": ["direct", "water", "crystal", "combined"], "ru": ["прямой", "вода", "кристалл", "комбинир."]}


# --- hero banner -----------------------------------------------------------------------------
BANNER = {
    "en": {
        "title": "Hyperbolic Field on Plants",
        "kicker": "AGRICULTURAL STUDY",
        "tag": "PRIVATE · NO RCT RESULTS YET",
        "sub": ["A 13-group trial is planned in full;", "so far only a pilot layer exists"],
        "chips": ["{rct_bins} groups planned, {rct_bins_empty} without data", "{photos} pilot photos", "{llm_runs} runs on one frame"],
        "foot": "grid = the planned groups; every cell is still empty",
        "desc": ("Generated illustration, not a screenshot. A grid of the {rct_bins} planned RCT groups (control and three channels by four "
                 "modes), every cell drawn empty because {rct_bins_empty} of {rct_bins} data bins hold no photo; the title; three figures "
                 "computed from the repository: {rct_bins} groups planned with {rct_bins_empty} empty, {photos} pilot photos, {llm_runs} "
                 "blind-model runs on one frame."),
    },
    "ru": {
        "title": "Гиперполе и растения",
        "kicker": "АГРОНОМИЧЕСКОЕ ИССЛЕДОВАНИЕ",
        "tag": "ПРИВАТНО · РЕЗУЛЬТАТОВ RCT ПОКА НЕТ",
        "sub": ["Испытание на 13 групп описано полностью;", "пока есть только пилотный слой"],
        "chips": ["{rct_bins} групп, {rct_bins_empty} пустых", "{photos} фото", "{llm_runs} прогонов, 1 кадр"],
        "foot": "сетка = группы плана; каждая ячейка пока пуста",
        "desc": ("Сгенерированная иллюстрация, не скриншот. Сетка из {rct_bins} запланированных групп RCT (контроль и три канала на четыре "
                 "режима), каждая ячейка нарисована пустой, потому что {rct_bins_empty} из {rct_bins} корзин данных без фото; заголовок; "
                 "три числа, посчитанные по репозиторию: {rct_bins} групп в плане, из них {rct_bins_empty} пустых, {photos_ru} пилота, "
                 "{llm_runs_ru} слепой модели на одном кадре."),
    },
}


def banner(lang):
    c = BANNER[lang]
    desc = fmt(c["desc"])
    W, H = 1200, 330
    o = [svg_open(W, H, c["title"], desc)]
    cw, ch, g = 62, 40, 8
    gx, gy = 40, 52
    # control cell on top, then three channel rows of four modes
    o.append("<rect x='%d' y='%d' width='%d' height='%d' rx='8' fill='none' stroke='%s' stroke-width='1.6' stroke-dasharray='5 5'/>"
             % (gx, gy, cw * 2 + g, ch, TEAL))
    o.append(text(gx + (cw * 2 + g) / 2, gy + 25, "control" if lang == "en" else "контроль", FS_SMALL, INK, "middle", 700))
    for r in range(3):
        for k in range(4):
            x, y = gx + k * (cw + g), gy + (ch + g) * (r + 1) + 8
            o.append("<rect x='%d' y='%d' width='%d' height='%d' rx='8' fill='none' stroke='%s' stroke-width='1.6' stroke-dasharray='5 5'/>"
                     % (x, y, cw, ch, [GOLD, VIOLET, BLUE][r]))
    for r, chn in enumerate(CHANNELS):
        o.append(text(gx + 4 * (cw + g) + 6, gy + (ch + g) * (r + 1) + 8 + 26, "ch" + chn, FS_SMALL, MUTED, "start", 700))
    o.append(text(gx, gy + (ch + g) * 4 + 38, "0 / %s" % F["rct_bins"], 30, AMBER, "start", 800, 0, 200))
    o.append(text(gx + 110, gy + (ch + g) * 4 + 38, "groups with data" if lang == "en" else "групп с данными", FS_BODY, MUTED, "start", 400, 0, 220))
    tx = 520
    box = W - tx - 36
    o.append(text(tx, 66, c["kicker"], FS_KICKER, TEAL, "start", 700, 2, box))
    o.append(text(W - 36, 36, c["tag"], FS_SMALL, MUTED, "end", 700, 2, 520))
    o.append(text(tx, 128, c["title"], 44, INK, "start", 800, 0, box))
    for i, line in enumerate(c["sub"]):
        o.append(text(tx, 170 + 28 * i, line, 21, MUTED, "start", 400, 0, box))
    x = tx
    for i, chip in enumerate(c["chips"]):
        chip = fmt(chip)
        w = text_width(chip, FS_KICKER, True) + 28
        if x + w > W - 30:
            raise SystemExit("chips overflow the banner: %r" % chip)
        col = [AMBER, TEAL, GREEN][i]
        o.append("<rect x='%.1f' y='246' width='%.1f' height='38' rx='19' fill='%s' fill-opacity='0.08' stroke='%s'/>" % (x, w, col, col))
        o.append(text("%.1f" % (x + w / 2), 271, chip, FS_KICKER, INK, "middle", 700))
        x += w + 12
    o.append(text(24, H - 14, c["foot"], FS_SMALL, MUTED, "start", 400, 0, 460))
    o.append("</svg>\n")
    return "\n".join(o)


# --- design matrix ---------------------------------------------------------------------------
MATRIX = {
    "en": {
        "title": "The planned 13 groups: all bins empty",
        "desc": ("A table of the {rct_bins} planned groups of protocol {protocol_version}: one control group, and channels 17, 19 and 21 each "
                 "in four modes, direct, water, crystal and combined. Every cell reads zero photos, {rct_bins_empty} of {rct_bins} bins are "
                 "empty placeholders. On the right the design factors: {crops} crops, {substrates} substrates, {seeds_per_group} seeds per "
                 "group and crop, {seeds_total} seeds in total, a design number and not an executed trial. Channel 14, mutagenesis, is a "
                 "separate hypothesis without a group."),
        "sub": "Protocol v8.3 layout (data/ bins); photos are not attributed to groups",
        "tag": "DESIGN",
        "ctrl": "control", "cell": "0 photos",
        "factors": ("Design factors", ["{crops} crops · {substrates} substrates", "{seeds_per_group} seeds per group and crop", "{rct_bins} x {seeds_per_group} x {crops} = {seeds_total} seeds"],
                    "◇ DESIGN NUMBER, NOT A TRIAL"),
        "ch14": ("Channel 14 (mutagenesis)", ["a separate hypothesis, no group, no data", "combinations 14, 14+17, 14+19"], "◇ HYPOTHESIS ONLY"),
        "foot": "Two photos are tagged ch17 in the manifest free text only; no photo sits in any bin.",
    },
    "ru": {
        "title": "Запланированные 13 групп: все корзины пусты",
        "desc": ("Таблица {rct_bins} запланированных групп протокола {protocol_version}: одна контрольная группа и каналы 17, 19 и 21 в четырёх "
                 "режимах каждый: прямой, вода, кристалл, комбинированный. В каждой ячейке ноль фото, {rct_bins_empty} из {rct_bins} корзин "
                 "пустые плейсхолдеры. Справа факторы дизайна: {crops} культур, {substrates} субстратов, {seeds_per_group} семян на группу и "
                 "культуру, всего {seeds_total} семян, это число дизайна, а не выполненное испытание. Канал 14, мутагенез, это отдельная "
                 "гипотеза без группы."),
        "sub": "Раскладка протокола v8.3 (корзины data/); фото к группам не привязаны",
        "tag": "ДИЗАЙН",
        "ctrl": "контроль", "cell": "0 фото",
        "factors": ("Факторы дизайна", ["{crops} культур · {substrates} субстратов", "{seeds_per_group} семян на группу и культуру", "{rct_bins} x {seeds_per_group} x {crops} = {seeds_total} семян"],
                    "◇ ЧИСЛО ДИЗАЙНА, НЕ ИСПЫТАНИЕ"),
        "ch14": ("Канал 14 (мутагенез)", ["отдельная гипотеза, без группы и данных", "комбинации 14, 14+17, 14+19"], "◇ ТОЛЬКО ГИПОТЕЗА"),
        "foot": "Два фото помечены ch17 только в свободном тексте манифеста; ни одно фото не лежит в корзине.",
    },
}


def matrix(lang):
    c = MATRIX[lang]
    W, H = 1100, 500
    cv = Canvas(W, H, c["title"], fmt(c["desc"]), c["title"], c["sub"], c["tag"])
    x0, y0, cw, chh, g = 24, 104, 118, 74, 8
    cv.box(x0 + 80, y0, cw, c["ctrl"], [c["cell"]], stroke=TEAL, h=chh, center=True)
    for k, m in enumerate(MODES[lang]):
        cv.label(x0 + 80 + k * (cw + g) + cw / 2, y0 + chh + 40, m, FS_KICKER, TEAL, "middle", 700, box=cw)
    cols = [GOLD, VIOLET, BLUE]
    for r, chn in enumerate(CHANNELS):
        y = y0 + chh + 52 + r * (chh - 10 + g)
        cv.label(x0, y + 38, "ch" + chn, FS_BODY, cols[r], weight=800, box=70)
        for k in range(4):
            cv.box(x0 + 80 + k * (cw + g), y, cw, None, [c["cell"]], stroke=cols[r], h=chh - 10, center=True)
    xr = x0 + 80 + 4 * (cw + g) + 14
    wr = W - xr - 24
    t, lines, st = c["factors"]
    cv.box(xr, y0, wr, t, [fmt(x) for x in lines], status=[(st, VIOLET)], stroke=VIOLET, h=186, valign="top")
    t, lines, st = c["ch14"]
    cv.box(xr, y0 + 198, wr, t, lines, status=[(st, VIOLET)], stroke=VIOLET, h=170, valign="top")
    foot(cv, c["foot"], H - 16)
    return "\n".join(cv.o + ["</svg>\n"])


# --- claimed vs shown ------------------------------------------------------------------------
CLAIM = {
    "en": {
        "title": "Claimed versus shown",
        "desc": ("Eight rows: topic, what the plan or a report claims, what the files show, and a status word. RCT: {rct_bins} groups planned, "
                 "no group holds data. Germination and growth targets: planned ranges, no counts. Regolith survival above 80 percent: a "
                 "target, no data. Exp29: laid down, no growth result. Radish panel: {llm_correct} of {llm_runs} runs picked the treated side "
                 "on one frame by one model, pixel metrics did not confirm. Microscopy greenness: not reproduced on {frames_total} frames. "
                 "Pattern classifier: frame level, leakage inflated. Percipient layer: subjective."),
        "sub": "Every row cites a file on the Evidence page",
        "tag": "EVIDENCE",
        "cols": ["Topic", "Claimed or planned", "Shown by the files", "Status"],
        "rows": [
            ("RCT", "{rct_bins} groups, {crops} crops, {seeds_total} seeds (protocol {protocol_version})", "No group holds data; {rct_bins_empty} of {rct_bins} bins are empty", "plan"),
            ("Germination, growth", "T50 -20-40 %, germination +10-20 %, growth +15-30 %", "No counts, heights or biomass anywhere", "none"),
            ("Regolith", "above 80 % survival in Mars / Moon simulants", "No regolith data", "none"),
            ("Exp29 (2 x 2)", "seed x water, coconut substrate", "Laid down 2026-06-29; no growth result", "plan"),
            ("Radish panel", "treated side picked", "{llm_correct} of {llm_runs} runs, one frame, one model family; pixel metrics disagree", "weak"),
            ("Microscopy colour", "treated leaves greener", "8 frames; not reproduced on {frames_total} frames; capture not calibrated", "weak"),
            ("Pattern classifier", "{frames_control} vs {frames_treated} frames separable", "Frame-level, leakage inflated; not proof of an effect", "weak"),
            ("Percipient layer", "impressions on plant trays", "Subjective, n=3, hypothesis generation only", "obs"),
        ],
    },
    "ru": {
        "title": "Заявлено и показано",
        "desc": ("Восемь строк: тема, что заявляют план или отчёт, что показывают файлы и слово-статус. RCT: {rct_bins} групп в плане, ни "
                 "одна не содержит данных. Цели по всхожести и росту: диапазоны плана, подсчётов нет. Выживаемость в реголите выше 80 "
                 "процентов: цель, данных нет. Exp29: заложен, результата роста нет. Панель по редису: {llm_correct} из {llm_runs} прогонов "
                 "выбрали обработанную сторону на одном кадре одной моделью, пиксельные метрики не подтвердили. Цвет при микроскопии: не "
                 "воспроизведён на {frames_total} кадрах. Классификатор паттернов: на уровне кадров, завышен утечкой. Перципиентный слой: "
                 "субъективный."),
        "sub": "Каждая строка опирается на файл со страницы «Доказательства»",
        "tag": "ДОКАЗАТЕЛЬСТВА",
        "cols": ["Тема", "Заявлено или в плане", "Что показывают файлы", "Статус"],
        "rows": [
            ("RCT", "{rct_bins} групп, {crops} культур, {seeds_total} семян (протокол {protocol_version})", "Ни одна группа не содержит данных; {rct_bins_empty} из {rct_bins} корзин пусты", "plan"),
            ("Всхожесть, рост", "T50 -20-40 %, всхожесть +10-20 %, рост +15-30 %", "Нигде нет подсчётов, высот или биомассы", "none"),
            ("Реголит", "выше 80 % выживаемости в симулянтах Марса / Луны", "Данных по реголиту нет", "none"),
            ("Exp29 (2 x 2)", "семена x вода, кокосовый субстрат", "Заложен 2026-06-29; результата роста нет", "plan"),
            ("Панель по редису", "выбрана обработанная сторона", "{llm_correct} из {llm_runs} прогонов, один кадр, одно семейство моделей; пиксели не согласны", "weak"),
            ("Цвет при микроскопии", "обработанные листья зеленее", "8 кадров; не воспроизведено на {frames_total} кадрах; съёмка не калибрована", "weak"),
            ("Классификатор паттернов", "{frames_control} против {frames_treated} кадров различимы", "На уровне кадров, завышен утечкой; не доказательство эффекта", "weak"),
            ("Перципиентный слой", "впечатления по лоткам с растениями", "Субъективно, n=3, только для порождения гипотез", "obs"),
        ],
    },
}


def claimed(lang):
    c = CLAIM[lang]
    st = STATE[lang]
    W, H = 1200, 836
    cv = Canvas(W, H, c["title"], fmt(c["desc"]), c["title"], c["sub"], c["tag"])
    x0, x1, x2, x3 = 24, 190, 580, 1000
    w1, w2, w3 = 390, 430, 176
    ytop = 98
    for x, lab, bw in ((x0, c["cols"][0], 160), (x1, c["cols"][1], w1), (x2, c["cols"][2], w2), (x3, c["cols"][3], w3)):
        cv.label(x, ytop + 10, lab, FS_KICKER, TEAL, weight=700, box=bw)
    rh, gap = 78, 8
    for i, (topic, claim, shown, state) in enumerate(c["rows"]):
        y = ytop + 26 + i * (rh + gap)
        label, col = st[state]
        for k, ln in enumerate(wrap(topic, FS_BODY, 156, True)):
            cv.label(x0, y + rh / 2 + 5 + (k - (len(wrap(topic, FS_BODY, 156, True)) - 1) / 2) * 18, ln, FS_BODY, INK, weight=700, box=160)
        cv.box(x1, y, w1 - 12, None, [fmt(claim)], stroke=BLUE, h=rh)
        cv.box(x2, y, w2 - 12, None, [fmt(shown)], stroke=col, h=rh)
        cv.box(x3, y, w3, None, [], status=[(label, col)], stroke=col, h=rh, center=True)
    return "\n".join(cv.o + ["</svg>\n"])


# --- timeline --------------------------------------------------------------------------------
# (date shown, text, file that carries the date, needle searched in that file)
PLAN = [
    ("2026 Q1", {"en": "Mar: protocol v8.3 finalised", "ru": "Март: протокол v8.3 финализирован"}, "README.md", "March 2026"),
    ("2026 Q2", {"en": "Apr equipment setup, May pilot, Jun main experiment starts", "ru": "Апр: оборудование, май: пилот, июнь: старт основного"}, "charts/mermaid/root_2.png", None),
    ("2026 Q3", {"en": "Jul-Aug main experiment, Sep growth monitoring", "ru": "Июль-авг: основной эксперимент, сен: мониторинг роста"}, "charts/mermaid/root_2.png", None),
    ("2026 Q4", {"en": "Oct-Nov growth monitoring, Dec data analysis starts", "ru": "Окт-ноя: мониторинг роста, дек: старт анализа"}, "charts/mermaid/root_2.png", None),
    ("2027 Q1", {"en": "Jan data analysis, Feb-Mar publication", "ru": "Янв: анализ данных, фев-март: публикация"}, "charts/mermaid/root_2.png", None),
]
PILOT = [
    ("2026-05-02", {"en": "First photo of the 23-photo set", "ru": "Первое фото набора из 23"}, "data/README.md", "2026-05-02"),
    ("2026-06-04", {"en": "Labelled pea pair; mould confound in the control", "ru": "Маркированная пара гороха; плесень в контроле"}, "data/README.md", "2026-06-04"),
    ("2026-06-16", {"en": "Radish blind panel: one frame, one model", "ru": "Слепая панель по редису: один кадр, одна модель"}, "reports/2026-06-16_llm-blind-photo/report_en.md", "2026-06-16"),
    ("2026-06-29", {"en": "Exp29 laid down (2 x 2 seed x water)", "ru": "Заложен exp29 (2 x 2 семена x вода)"}, "protocols/2026-06-29_exp29-irradiated-germination.md", "2026-06-29"),
    ("2026-07-02", {"en": "Microscopy pilot, 8 frames", "ru": "Микроскопия, пилот, 8 кадров"}, "reports/2026-07-02_microscopy-cell-structure/report_en.md", "2026-07-02"),
    ("2026-07-03", {"en": "Pattern analysis, 52 frames", "ru": "Анализ паттернов, 52 кадра"}, "reports/2026-07-03_pattern-embedding-analysis/report_en.md", "2026-07-03"),
    ("2026-07-07", {"en": "Blind plant protocol with percipients designed; no result", "ru": "Спроектирован слепой протокол с перципиентами; результата нет"}, "reports/percipient_reports/PLANT_CENSOR_EVIDENCE_SO_FAR.md", "2026-07-07"),
    ("2026-07-08", {"en": "Earlier-samples batch received; not analysed", "ru": "Получена партия ранних образцов; анализа нет"}, "data/incoming/2026-07-08_earlier-samples/MANIFEST.md", "2026-07-08"),
]
TL = {
    "en": {"title": "Planned schedule and what happened", "tag": "TIMELINE", "sub": "Not to scale; each pilot date is taken from one repository text",
           "desc": "Two lanes, not to scale. Lane one, the plan: {plan}. Lane two, the pilot layer: {pilot}.",
           "lanes": ["PLAN (DIAGRAM IN THE REPOSITORY)", "WHAT EXISTS (DATED FILES)"], "state": "◇ PLANNED"},
    "ru": {"title": "План и то, что произошло", "tag": "ХРОНОЛОГИЯ", "sub": "Без масштаба; каждая дата пилота взята из одного текста репозитория",
           "desc": "Две дорожки, без масштаба. Первая, план: {plan}. Вторая, пилотный слой: {pilot}.",
           "lanes": ["ПЛАН (СХЕМА В РЕПОЗИТОРИИ)", "ЧТО ЕСТЬ (ДАТИРОВАННЫЕ ФАЙЛЫ)"], "state": "◇ ПЛАН"},
}


def check_dates():
    for date, _t, src, needle in PILOT + PLAN:
        if needle is None:
            continue
        if needle not in factsmod.read(src):
            raise SystemExit("timeline date %s (%r) is not in %s" % (date, needle, src))


def timeline(lang):
    check_dates()
    c = TL[lang]
    desc = c["desc"].format(plan="; ".join("%s %s" % (d, t[lang]) for d, t, _, _ in PLAN),
                            pilot="; ".join("%s %s" % (d, t[lang]) for d, t, _, _ in PILOT))
    W, H = 1200, 520
    cv = Canvas(W, H, c["title"], desc, c["title"], c["sub"], c["tag"])
    gap = 8
    for lane, (events, col, y, lab, h) in enumerate(((PLAN, VIOLET, 100, c["lanes"][0], 118), (PILOT, TEAL, 270, c["lanes"][1], 160))):
        n = len(events)
        bw = (W - 48 - gap * (n - 1)) / n
        cv.label(24, y, lab, FS_KICKER, col, weight=800, box=600)
        cv.o.append("<line x1='24' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2' stroke-opacity='0.6'/>" % (y + 18, W - 24, y + 18, col))
        for i, (date, t, _s, _n) in enumerate(events):
            x = 24 + i * (bw + gap)
            cv.o.append("<circle cx='%.1f' cy='%d' r='6' fill='%s'/>" % (x + bw / 2, y + 18, col))
            cv.box(x, y + 34, bw, date, [t[lang]], status=[(c["state"], VIOLET)] if lane == 0 else [], stroke=col, h=h, title_size=14, pad=10, valign="top")
    foot(cv, {"en": "Quarters are copied from the plan diagram charts/mermaid/root_2.png; the repository does not say whether they were kept.",
              "ru": "Кварталы взяты со схемы плана charts/mermaid/root_2.png; репозиторий не говорит, соблюдались ли они."}[lang], H - 16)
    return "\n".join(cv.o + ["</svg>\n"])


# --- evidence ladder -------------------------------------------------------------------------
LADDER = {
    "en": {
        "title": "Evidence ladder: which rungs exist",
        "desc": ("Five rungs from plan to result. Rung one, protocol {protocol_version} with {rct_bins} groups: planned only. Rung two, "
                 "{photos} photos and {exp29_setup_files} set-up files: observation. Rung three, one-frame blind-model panel and an "
                 "{micro_report_frames}-frame microscopy pilot: not confirmed. Rung four, a {frames_total}-frame pattern classifier: "
                 "frame level and leakage inflated. Rung five, a randomised, replicated result: none yet."),
        "sub": "A plan is not a result; a pilot is not a trial",
        "tag": "EVIDENCE",
        "rungs": [
            ("1 · Protocol", ["{rct_bins} groups, {crops} crops, {seeds_total} seeds on paper"], "plan"),
            ("2 · Observation", ["{photos} tray photos, {exp29_setup_files} exp29 set-up files, no measurements"], "obs"),
            ("3 · Small pilots", ["one-frame blind panel; {micro_report_frames}-frame microscopy; colour not calibrated"], "weak"),
            ("4 · Classifier", ["{frames_total} frames, frame-level, pseudoreplicated; not proof of an effect"], "weak"),
            ("5 · RCT result", ["randomised, replicated, per-group counts"], "none"),
        ],
        "foot": "Rungs 3 and 4 are the repository's own reports and say so in their conclusions.",
    },
    "ru": {
        "title": "Лестница доказательств: какие ступени есть",
        "desc": ("Пять ступеней от плана к результату. Первая, протокол {protocol_version} с {rct_bins} группами: только план. Вторая, "
                 "{photos_ru} и {exp29_setup_files} файлов закладки: наблюдение. Третья, слепая панель моделей по одному кадру и "
                 "микроскопический пилот на {micro_report_frames} кадрах: не подтверждено. Четвёртая, классификатор паттернов на "
                 "{frames_total} кадрах: на уровне кадров, завышен утечкой. Пятая, рандомизированный воспроизведённый результат: пока нет."),
        "sub": "План не результат; пилот не испытание",
        "tag": "ДОКАЗАТЕЛЬСТВА",
        "rungs": [
            ("1 · Протокол", ["{rct_bins} групп, {crops} культур, {seeds_total} семян на бумаге"], "plan"),
            ("2 · Наблюдение", ["{photos_ru} лотков, {exp29_setup_files} файлов закладки exp29, измерений нет"], "obs"),
            ("3 · Малые пилоты", ["слепая панель по одному кадру; {micro_report_frames} кадров микроскопии; цвет не калиброван"], "weak"),
            ("4 · Классификатор", ["{frames_total} кадров, уровень кадров, псевдоповторы; не доказательство эффекта"], "weak"),
            ("5 · Результат RCT", ["рандомизированный, воспроизведённый, подсчёты по группам"], "none"),
        ],
        "foot": "Ступени 3 и 4 это собственные отчёты репозитория, и они так и пишут в выводах.",
    },
}


def ladder(lang):
    c = LADDER[lang]
    st = STATE[lang]
    W, H = 1200, 346
    cv = Canvas(W, H, c["title"], fmt(c["desc"]), c["title"], c["sub"], c["tag"])
    n = 5
    gap = 12
    bw = (W - 48 - gap * (n - 1)) / n
    for i, (t, body, s) in enumerate(c["rungs"]):
        lab, col = st[s]
        x = 24 + i * (bw + gap)
        cv.box(x, 120, bw, t, [fmt(b) for b in body], status=[(lab, col)], stroke=col, h=156, valign="top", title_size=15, pad=12)
        if i < n - 1:
            cv.arrow([(x + bw + 1, 185), (x + bw + gap - 1, 185)], MUTED)
    foot(cv, c["foot"], H - 16)
    return "\n".join(cv.o + ["</svg>\n"])


# --- family map ------------------------------------------------------------------------------
FAMILY = {
    "en": {
        "title": "Where the study sits in the hyperbolic-field family",
        "desc": ("A hub card for the emitter and channel technology behind patent application KZ 2025/1095.1, an application and not a "
                 "granted patent, applicants being individuals. Four study cards below it: blood plasma, yeast, DAAT crystal, and this "
                 "agricultural study, highlighted, which makes no separate IP claim. Sibling studies are listed in the previous README only; "
                 "no repository link shows shared data or results."),
        "sub": "Siblings are named in the previous README; no shared data is shown",
        "tag": "FAMILY",
        "hub": ("Emitter and channel technology", ["IP basis: application KZ 2025/1095.1 (FBHFS)", "an application, not a granted patent; applicants are individuals"], "◇ APPLICATION"),
        "kids": [("Blood plasma study", ["sibling repository"], False), ("Yeast study (Saccharomyces)", ["sibling repository"], False),
                 ("DAAT crystal study", ["sibling repository"], False),
                 ("This study: plants", ["pilot layer only", "asserts no separate IP claim"], True)],
        "foot": "Whether the crystal arm of this study uses the DAAT crystal is not stated in the repository.",
    },
    "ru": {
        "title": "Место исследования в семействе гиперболических полей",
        "desc": ("Карточка-хаб технологии эмиттера и каналов, лежащей в основе патентной заявки KZ 2025/1095.1: это заявка, а не выданный "
                 "патент, заявители физические лица. Под ней четыре карточки исследований: плазма крови, дрожжи, кристалл DAAT и это "
                 "агрономическое исследование, выделенное, которое не заявляет отдельных прав на ИС. Соседние исследования названы только "
                 "в прежнем README; ни одна ссылка на репозиторий не показывает общих данных или результатов."),
        "sub": "Соседи названы в прежнем README; общих данных не показано",
        "tag": "СЕМЕЙСТВО",
        "hub": ("Технология эмиттера и каналов", ["основа ИС: заявка KZ 2025/1095.1 (FBHFS)", "заявка, а не выданный патент; заявители физические лица"], "◇ ЗАЯВКА"),
        "kids": [("Исследование плазмы крови", ["соседний репозиторий"], False), ("Исследование дрожжей (Saccharomyces)", ["соседний репозиторий"], False),
                 ("Исследование кристалла DAAT", ["соседний репозиторий"], False),
                 ("Это исследование: растения", ["только пилотный слой", "не заявляет отдельных прав на ИС"], True)],
        "foot": "Использует ли кристальная ветвь этого исследования кристалл DAAT, в репозитории не сказано.",
    },
}


def family(lang):
    c = FAMILY[lang]
    W, H = 1200, 430
    cv = Canvas(W, H, c["title"], c["desc"], c["title"], c["sub"], c["tag"])
    t, lines, st = c["hub"]
    hx, hw = 250, 700
    cv.box(hx, 98, hw, t, lines, status=[(st, VIOLET)], stroke=VIOLET, h=130, center=True, valign="top", title_size=18)
    n = 4
    gap = 12
    bw = (W - 48 - gap * (n - 1)) / n
    for i, (kt, kl, me) in enumerate(c["kids"]):
        x = 24 + i * (bw + gap)
        cv.box(x, 272, bw, kt, kl, stroke=GREEN if me else TEAL, h=96, center=True, valign="top", title_size=15, pad=12,
               fill="#10223a" if me else PANEL)
        cv.arrow([(x + bw / 2, 262), (x + bw / 2, 270)], MUTED)
    cv.o.append("<line x1='%.1f' y1='262' x2='%.1f' y2='262' stroke='%s' stroke-width='2'/>" % (24 + bw / 2, 24 + 3 * (bw + gap) + bw / 2, MUTED))
    cv.o.append("<line x1='%d' y1='228' x2='%d' y2='262' stroke='%s' stroke-width='2'/>" % (W / 2, W / 2, MUTED))
    foot(cv, c["foot"], H - 16)
    return "\n".join(cv.o + ["</svg>\n"])


# --- icons -----------------------------------------------------------------------------------
def icon(col, body, title):
    return ("<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 64 64\" width=\"64\" height=\"64\" role=\"img\">\n"
            "<title>%s</title>\n<desc>Navigation icon: %s.</desc>\n<rect x=\"2\" y=\"2\" width=\"60\" height=\"60\" rx=\"12\" fill=\"#101826\" "
            "stroke=\"%s\" stroke-width=\"3\"/>\n<g fill='none' stroke='%s' stroke-width='2.6' stroke-linecap='round' "
            "stroke-linejoin='round'>%s</g>\n</svg>\n" % (title, title, col, col, body))


ICONS = {
    "study": (TEAL, "<circle cx='32' cy='32' r='16'/><circle cx='32' cy='32' r='5'/><path d='M32 12v8M32 44v8M12 32h8M44 32h8'/>", "the study"),
    "design": (GOLD, "<rect x='13' y='14' width='16' height='16' rx='3'/><rect x='35' y='14' width='16' height='16' rx='3'/>"
                     "<rect x='13' y='36' width='16' height='14' rx='3'/><rect x='35' y='36' width='16' height='14' rx='3'/>", "the plan"),
    "pilot": (TEAL, "<path d='M32 50V30M32 30c0-9-7-13-15-13 0 9 6 13 15 13zM32 36c0-8 6-11 14-11 0 8-5 11-14 11z'/>", "pilot data"),
    "evidence": (AMBER, "<circle cx='28' cy='28' r='13'/><path d='M38 38l12 12M23 28l4 4 7-8'/>", "evidence"),
    "ecosystem": (BLUE, "<circle cx='32' cy='32' r='6'/><circle cx='32' cy='14' r='4'/><circle cx='48' cy='41' r='4'/>"
                        "<circle cx='16' cy='41' r='4'/><path d='M32 26V18M37 35l8 4M27 35l-8 4'/>", "ecosystem and IP"),
    "navigation": (GREEN, "<path d='M20 14v36M20 22h10M20 34h10M20 46h10'/><rect x='30' y='17' width='20' height='10' rx='2'/>"
                          "<rect x='30' y='29' width='20' height='10' rx='2'/><rect x='30' y='41' width='20' height='10' rx='2'/>", "navigation"),
    "open": (GOLD, "<circle cx='32' cy='32' r='18'/><path d='M26 27a6 6 0 1 1 9 5c-2 1-3 2-3 4M32 43v2'/>", "open questions"),
    "archive": (MUTED, "<rect x='12' y='14' width='40' height='11' rx='3'/><path d='M16 25v25h32V25M26 34h12'/>", "archive"),
}


def main():
    for lang in ("en", "ru"):
        write("guide/assets/banner/hero-banner.%s.svg" % lang, banner(lang))
        write("guide/assets/diagrams/design-matrix.%s.svg" % lang, matrix(lang))
        write("guide/assets/diagrams/claimed-vs-shown.%s.svg" % lang, claimed(lang))
        write("guide/assets/diagrams/timeline.%s.svg" % lang, timeline(lang))
        write("guide/assets/diagrams/evidence-ladder.%s.svg" % lang, ladder(lang))
        write("guide/assets/diagrams/family-map.%s.svg" % lang, family(lang))
    for name, (col, body, title) in ICONS.items():
        write("guide/assets/icons/%s.svg" % name, icon(col, body, title))


if __name__ == "__main__":
    main()
