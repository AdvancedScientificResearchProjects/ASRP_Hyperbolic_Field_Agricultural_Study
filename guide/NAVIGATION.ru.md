**[English](NAVIGATION.md) | Русский**

[← Исследование влияния гиперболических полей на сельское хозяйство](../README.ru.md) · [Указатель](README.ru.md)

<div align="center">

# Навигация и структура

</div>

## Где что лежит

| Нужно | Куда идти |
|---|---|
| Что за исследование и что в плане | [Исследование](STUDY.ru.md), [План](DESIGN.ru.md) |
| Сырые наблюдения | `data/photos/` (<!--n:photos-->23<!--/n--> фото, `manifest.json`), `data/exp29-setup/` |
| Что проанализировано | `reports/` (<!--n:reports_dated-->4<!--/n--> датированных анализа; пары EN и RU, кроме одного отчёта только на русском), `results/llm_blind/` |
| Единственный протокол в виде файла | `protocols/2026-06-29_exp29-irradiated-germination.md` (только на русском) |
| Код | `scripts/llm_analysis/run_blind_panel.py` и папки `scripts/` внутри отчётов (<!--n:analysis_scripts-->10<!--/n--> файлов Python всего) |
| Диаграммы плана | `charts/mermaid/root_1.png` — `root_3.png` |
| Прежний README | `archive/README_2026-11-19_pre-showcase.md` |

## Структура данных

Раскладка хаба данных двухслойная: плоский набор `photos/` — каноничная сырая запись, и <!--n:rct_bins-->13<!--/n--> корзин, выровненных по протоколу, — аналитическая проекция, пустая, пока руководитель не привяжет фото к обработкам. Ниже раскладка из прежнего README.

```
Hyperbolic_Field_Agricultural_Study/
|
|-- README.md
|
|-- data/
|   |-- README.md                      # Хаб данных
|   |-- photos/                        # Плоский набор + манифест
|   |   |-- README.md
|   |   |-- manifest.json
|   |   |-- original/                  # HEIC originals / HEIC-оригиналы
|   |   `-- jpg/                       # Превью
|   |-- control/                       # Контрольная группа
|   |   `-- photos/
|   |-- ch17-direct/                   # Прямое воздействие
|   |   `-- photos/
|   |-- ch17-water/                    # Через воду
|   |   `-- photos/
|   |-- ch17-crystal/                  # Через кристалл
|   |   `-- photos/
|   |-- ch17-combined/                 # Комбинированный
|   |   `-- photos/
|   |-- ch19-direct/                   # Прямое
|   |   `-- photos/
|   |-- ch19-water/
|   |   `-- photos/
|   |-- ch19-crystal/
|   |   `-- photos/
|   |-- ch19-combined/
|   |   `-- photos/
|   |-- ch21-direct/                   # Прямое
|   |   `-- photos/
|   |-- ch21-water/
|   |   `-- photos/
|   |-- ch21-crystal/
|   |   `-- photos/
|   |-- ch21-combined/
|   |   `-- photos/
|   |-- exp29-setup/                   # Фото установки exp29 + рукописный протокол
|   `-- incoming/                      # Новые поступления на рассмотрении
|       `-- 2026-07-08_earlier-samples/
|
|-- charts/                            # Диаграммы Mermaid
|-- protocols/                         # Протоколы экспериментов (v8.3)
|-- reports/                           # Датированные отчёты (пары EN+RU)
|-- results/                           # Производные результаты
`-- scripts/                           # Analysis code (llm_analysis) / Код анализа
```

См. **[data/README.md](../data/README.md)** — хаб данных, индексирующий плоский набор фотографий в `data/photos/` и RCT-выровненные корзины канал/режим.

## Дерево папок сегодня

Дерево ниже генерируется по реальному списку файлов (`tools/tree.py`), поэтому не может разойтись с репозиторием.

<!-- tree -->
```
ASRP_Hyperbolic_Field_Agricultural_Study/
├── README.md                                   # главная страница (английская)
├── README.ru.md                                # главная страница (русская)
├── guide/                                      # страницы-детали X.md + X.ru.md; assets/ = сгенерированные SVG
├── archive/                                    # прежний README, сохранён байт в байт
├── tools/                                      # инструменты витрины: факты, визуалы, выдержки, проверка без потерь
├── tests/                                      # регрессионный гейт витрины
├── charts/                                     # 3 диаграммы Mermaid плана (root_1..3.png)
│   └── mermaid/                                # группы, хронология, связь с патентом
├── data/                                       # фото, фото закладки, входящая партия, 13 пустых корзин RCT
│   ├── README.md                               # хаб данных: слои и чего он не утверждает
│   ├── photos/                                 # 23 фото (18 JPEG, 5 HEIC) + manifest.json
│   ├── exp29-setup/                            # 17 файла закладки exp29, вкл. рукописный протокол
│   ├── incoming/                               # партия 2026-07-08 на рассмотрении (медиа в .gitignore)
│   └── control/                                # корзины RCT control, ch17/ch19/ch21 x 4 режима: плейсхолдеры
├── protocols/                                  # протокол exp29 (только на русском)
├── reports/                                    # 4 датированных анализа (EN+RU) и перципиентный слой
│   ├── 2026-06-16_llm-blind-photo/             # редис: слепая панель моделей по одному кадру
│   ├── 2026-06-29_exp29-setup-observation/     # наблюдение закладки exp29 (только на русском)
│   ├── 2026-07-02_microscopy-cell-structure/   # микроскопия, пилот: цвет и форма клеток
│   ├── 2026-07-03_pattern-embedding-analysis/  # 52 кадра: эмбеддинги, ядра, паттерны
│   └── percipient_reports/                     # субъективный перципиентный слой (приватно; папки участников не описаны)
├── results/                                    # llm_blind: 10 прогонов и ключ
└── scripts/                                    # llm_analysis: скрипт слепой панели
```
<!-- /tree -->

## Правила витрины

- Переписан только `README.md`; добавлены `README.ru.md`, `guide/`, `tools/`, `tests/` и `archive/`. Ни один существующий файл не перемещён, не изменён и не удалён; файлы Git LFS не тронуты.
- Числа на этих страницах посчитаны по репозиторию скриптом `tools/build_facts.py` (невидимые маркеры в исходнике Markdown).
- Диаграммы строит `tools/build_visuals.py`; у каждой картинки есть английская и русская пара.
- `python3 tools/verify_no_loss.py` сверяет новые страницы с заархивированным README; `python3 -m unittest discover -s tests` запускает регрессионный гейт.
