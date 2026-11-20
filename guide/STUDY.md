**English | [Русский](STUDY.ru.md)**

[← Hyperbolic Field Agricultural Study](../README.md) · [Guide index](README.md)

<div align="center">

# The study: what it is and what it asks

</div>

## What the study is

This repository holds the **design of a planned randomized controlled trial (RCT)** of hyperbolic-field exposure on seed germination, plant growth dynamics and agricultural yield, **plus a small pilot layer** of photographs and image analyses. The trial would compare direct exposure, water-mediated effects and crystal-based treatment across <!--n:crops-->6<!--/n--> crop varieties and <!--n:substrates-->8<!--/n--> substrates, including Mars and Moon regolith simulants for space agriculture.

**Read the data status before any result is inferred.** Protocol <!--n:protocol_version-->v8.3<!--/n--> is complete (as the previous README states; its text is not in this repository), but **no quantitative RCT results exist yet**: all <!--n:rct_bins-->13<!--/n--> group bins in `data/` are empty placeholders (<!--n:rct_bins_empty-->13<!--/n--> of <!--n:rct_bins-->13<!--/n-->). **No claim anywhere in the repository is confirmatory, statistically significant, dose-response, or based on completed trials.** Targets in the goals table below are protocol-defined hypotheses, not measured outcomes.

The pilot layer is real but small: <!--n:photos-->23<!--/n--> tray photographs, one laid-down germination experiment (exp29) without a result, a one-frame blind-model comparison, two microscopy analyses, and a subjective percipient layer. See [Pilot data](PILOT.md) and [Evidence](EVIDENCE.md).

## Why it exists

The study is the agricultural sibling of the other hyperbolic-field studies of ASRP (blood plasma, yeast, DAAT crystal). It asks whether the emitter and channel technology behind patent application KZ 2025/1095.1 has any observable effect on seeds and plants: faster germination, better growth, resilience in poor substrates and regolith, treated water, passive crystal effects. It is **exploratory** and **asserts no separate IP claim** of its own; the patent link is described on the [ecosystem page](ECOSYSTEM.md). The repository states no result that feeds a publication or a product.

## Key metrics

These are design numbers of the plan, not outcomes. The seed total is the product of the groups, seeds per group and crops (checked at build time).

| Parameter | Value |
|---|---|
| **Study type** | Randomized controlled trial (RCT), planned |
| **Protocol version** | <!--n:protocol_version-->v8.3<!--/n--> (March 2026) |
| **Duration** | 196–226 days (~7 months), planned |
| **Treatment groups** | <!--n:rct_bins-->13<!--/n--> (1 control + 12 treatment) |
| **Crops** | <!--n:crops-->6<!--/n--> |
| **Seeds per group** | <!--n:seeds_per_group-->200<!--/n--> |
| **Total seeds** | <!--n:seeds_total-->15,600<!--/n--> |
| **Substrates** | <!--n:substrates-->8<!--/n--> (including Mars/Moon regolith simulants) |
| **Channels** | 17, 19, 21 (+ Channel 14 mutagenic) |
| **Patent** | KZ 2025/1095.1 (an application, not a granted patent) |

## Research goals

Seven measurable goals. The expected effects are **targets written into the plan**, not findings.

| Goal | Target | Expected effect (planned) |
|---|---|---|
| **G1** Germination acceleration | T50 (time to 50% germination) | -20–40% reduction |
| **G2** Germination rate | Germination percentage | +10–20% increase |
| **G3** Growth rate | Plant height, biomass | +15–30% increase |
| **G4** Stress resilience | Survival in poor substrates | >80% in regolith |
| **G5** Yield optimization | Seed yield per plant | +10–25% increase |
| **G6** Water treatment | Treated water effects | Measurable growth difference |
| **G7** Crystal treatment | Passive field effects | Validate crystal efficacy |

## Measurements

| Category | Parameters |
|---|---|
| **Primary** | Germination time (T50), germination percentage, germination uniformity |
| **Secondary** | Plant height, leaf count, stem diameter, chlorophyll (SPAD), fresh/dry biomass, seed yield |

None of these has been measured in the repository. The pilot reports use image-derived proxies instead (green fraction, nuclei area, embeddings), see [Pilot data](PILOT.md).
