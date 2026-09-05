"""Regenerate retained-coding figures for the public JDMS package.

Requires Pillow. Uses only the unchanged run-level CSV; never infers source
passages or reassigns outcomes. Public figure2 is manuscript Figure 1, and
public figure1 is manuscript Figure 2. See the manuscript for provenance limits.
"""

from __future__ import annotations

import csv
from math import isfinite
from pathlib import Path
from statistics import mean, stdev

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "coding" / "final_outcome_coding_run_level.csv"
OUT = ROOT / "figures"
OUT.mkdir(parents=True, exist_ok=True)

SYSTEMS = ["GPT-4o", "Gemini 2.5 Flash", "Claude Opus 4", "Perplexity Pro"]
SYSTEM_COLORS = {
    "GPT-4o": "#2F5597",
    "Gemini 2.5 Flash": "#C65911",
    "Claude Opus 4": "#548235",
    "Perplexity Pro": "#8064A2",
}
VARIABLES = {
    "Tension": "tension",
    "Diplomatic support": "diplomatic_engagement",
    "Public opinion": "public_support",
    "Leadership unity": "internal_unity",
}
OUTCOME_COLORS = {
    "Protracted stalemate": "#4E79A7",
    "Internal collapse": "#A0CBE8",
    "Diplomatic resolution": "#59A14F",
    "Full-scale war": "#E15759",
    "Limited conflict": "#F28E2B",
}


def load_rows() -> list[dict[str, str]]:
    with DATA.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 120:
        raise RuntimeError(f"Expected 120 rows, found {len(rows)}")
    if any(sum(row["system"] == system for row in rows) != 30 for system in SYSTEMS):
        raise RuntimeError("Expected 30 rows for each system group")
    if len({row["execution_id"] for row in rows}) != 120:
        raise RuntimeError("Expected 120 unique execution identifiers")
    if any(row["final_outcome_5"] not in OUTCOME_COLORS for row in rows):
        raise RuntimeError("Unrecognized retained outcome category")
    for row in rows:
        for field in VARIABLES.values():
            value = float(row[field])
            if not isfinite(value) or not 0 <= value <= 1:
                raise RuntimeError(f"State value outside 0-1: {row['execution_id']}, {field}")
    return rows


def font(size: int, bold: bool = False):
    filename = "timesbd.ttf" if bold else "times.ttf"
    candidates = [
        Path("C:/Windows/Fonts") / filename,
        Path("/usr/share/fonts/truetype/dejavu") / ("DejaVuSerif-Bold.ttf" if bold else "DejaVuSerif.ttf"),
        Path("/Library/Fonts") / ("Times New Roman Bold.ttf" if bold else "Times New Roman.ttf"),
    ]
    for candidate in candidates:
        if candidate.is_file():
            return ImageFont.truetype(str(candidate), size)
    try:
        return ImageFont.truetype("DejaVuSerif-Bold.ttf" if bold else "DejaVuSerif.ttf", size)
    except OSError:
        return ImageFont.load_default()


def text_center(draw, xy, text, selected_font, fill="#222222") -> None:
    box = draw.textbbox((0, 0), text, font=selected_font)
    draw.text(
        (xy[0] - (box[2] - box[0]) / 2, xy[1] - (box[3] - box[1]) / 2),
        text,
        font=selected_font,
        fill=fill,
    )


def draw_marker(draw, x, y, index, color, radius=13) -> None:
    """Use the same non-color symbol in the legend and in each panel."""
    if index == 0:
        draw.ellipse((x-radius, y-radius, x+radius, y+radius), fill=color, outline="#222222", width=2)
    elif index == 1:
        draw.rectangle((x-radius, y-radius, x+radius, y+radius), fill=color, outline="#222222", width=2)
    elif index == 2:
        draw.polygon([(x, y-radius-4), (x+radius+4, y), (x, y+radius+4), (x-radius-4, y)], fill=color, outline="#222222")
    else:
        draw.polygon([(x, y-radius-4), (x+radius+4, y+radius+1), (x-radius-4, y+radius+1)], fill=color, outline="#222222")


ROWS = load_rows()
VARIABLE_SUMMARIES = {
    label: [
        (
            mean(float(row[field]) for row in ROWS if row["system"] == system),
            stdev(float(row[field]) for row in ROWS if row["system"] == system),
        )
        for system in SYSTEMS
    ]
    for label, field in VARIABLES.items()
}
OUTCOME_COUNTS = {
    system: [
        sum(row["system"] == system and row["final_outcome_5"] == category for row in ROWS)
        for category in OUTCOME_COLORS
    ]
    for system in SYSTEMS
}


def make_variable_figure() -> None:
    width, height = 2400, 1660
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    text_center(draw, (width / 2, 65), "Workbook state summaries by system", font(52, True))
    text_center(draw, (width / 2, 120), "Mean ± sample SD; intervals clipped to 0–1; n = 30 per system", font(36), "#444444")

    text_center(draw, (width / 2, 170), "Source-passage selection remains unresolved.", font(34), "#444444")

    legend_y = 220
    legend_widths = [draw.textlength(system, font=font(34)) + 80 for system in SYSTEMS]
    start_x = (width - sum(legend_widths)) / 2
    for index, (system, slot) in enumerate(zip(SYSTEMS, legend_widths)):
        draw_marker(draw, start_x + 13, legend_y + 3, index, SYSTEM_COLORS[system])
        draw.text((start_x + 38, legend_y - 20), system, font=font(34), fill="#222222")
        start_x += slot

    boxes = [(120, 300, 1160, 910), (1240, 300, 2280, 910), (120, 970, 1160, 1580), (1240, 970, 2280, 1580)]
    for (title, values), (x0, y0, x1, y1) in zip(VARIABLE_SUMMARIES.items(), boxes):
        draw.rounded_rectangle((x0, y0, x1, y1), radius=18, outline="#B7B7B7", width=3, fill="#FCFCFC")
        text_center(draw, ((x0 + x1) / 2, y0 + 50), title, font(40, True))
        plot_x0, plot_x1 = x0 + 105, x1 - 45
        plot_y0, plot_y1 = y0 + 115, y1 - 100
        for tick in range(0, 11, 2):
            value = tick / 10
            y = plot_y1 - value * (plot_y1 - plot_y0)
            draw.line((plot_x0, y, plot_x1, y), fill="#E1E1E1", width=2)
            draw.text((x0 + 25, y - 21), f"{value:.1f}", font=font(34), fill="#444444")
        draw.line((plot_x0, plot_y0, plot_x0, plot_y1), fill="#555555", width=3)
        draw.line((plot_x0, plot_y1, plot_x1, plot_y1), fill="#555555", width=3)
        positions = [plot_x0 + (index + 0.5) * (plot_x1 - plot_x0) / 4 for index in range(4)]
        for index, (system, (average, sd), x) in enumerate(zip(SYSTEMS, values, positions)):
            low, high = max(0, average - sd), min(1, average + sd)
            y_mean = plot_y1 - average * (plot_y1 - plot_y0)
            y_low = plot_y1 - low * (plot_y1 - plot_y0)
            y_high = plot_y1 - high * (plot_y1 - plot_y0)
            color = SYSTEM_COLORS[system]
            draw.line((x, y_high, x, y_low), fill=color, width=6)
            draw.line((x - 13, y_high, x + 13, y_high), fill=color, width=5)
            draw.line((x - 13, y_low, x + 13, y_low), fill=color, width=5)
            draw_marker(draw, x, y_mean, index, color)
            short_labels = ["GPT-4o", "Gemini", "Claude", "Perplexity"]
            text_center(draw, (x, plot_y1 + 48), short_labels[index], font(34))
    image.save(OUT / "figure1_end_of_run_variables.png", dpi=(300, 300))


def make_outcome_figure() -> None:
    width, height = 2400, 1460
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    text_center(draw, (width / 2, 70), "Retained author-coded outcome distributions", font(52, True))
    text_center(draw, (width / 2, 125), "Five retained categories; n = 30 per system; segment labels are counts", font(35), "#444444")
    text_center(draw, (width / 2, 180), "Source-passage selection remains unresolved.", font(34), "#444444")
    items = list(OUTCOME_COLORS.items())
    category_keys = dict(zip(OUTCOME_COLORS, "ABCDE"))
    for legend_items, legend_y in [(items[:3], 245), (items[3:], 302)]:
        legend_widths = [draw.textlength(f"{category_keys[label]}  {label}", font=font(35)) + 90 for label, _ in legend_items]
        start_x = (width - sum(legend_widths)) / 2
        for (label, color), slot in zip(legend_items, legend_widths):
            draw.rectangle((start_x, legend_y - 12, start_x + 28, legend_y + 16), fill=color, outline="#333333", width=2)
            draw.text((start_x + 39, legend_y - 21), f"{category_keys[label]}  {label}", font=font(35), fill="#222222")
            start_x += slot

    chart_x0, chart_x1 = 520, 2260
    bar_height = 145
    for system, y in zip(SYSTEMS, [390, 620, 850, 1080]):
        draw.text((60, y + 42), system, font=font(34, True), fill="#222222")
        x = chart_x0
        for (category, color), count in zip(items, OUTCOME_COUNTS[system]):
            segment_width = (chart_x1 - chart_x0) * count / 30
            if count:
                draw.rectangle((x, y, x + segment_width, y + bar_height), fill=color, outline="white", width=3)
                # Letters identify categories in grayscale; all nonzero counts
                # are shown, including narrow segments with just one or two rows.
                label = f"{category_keys[category]}\n{count}"
                selected_font = font(38 if count >= 3 else 35, True)
                box = draw.multiline_textbbox((0, 0), label, font=selected_font, align="center")
                draw.multiline_text(
                    (x + segment_width / 2 - (box[2] - box[0]) / 2,
                     y + bar_height / 2 - (box[3] - box[1]) / 2),
                    label, font=selected_font, fill="#111111", align="center",
                )
            x += segment_width
        draw.rectangle((chart_x0, y, chart_x1, y + bar_height), outline="#444444", width=3)
    for tick in range(0, 101, 20):
        x = chart_x0 + (chart_x1 - chart_x0) * tick / 100
        draw.line((x, 1260, x, 1275), fill="#444444", width=3)
        text_center(draw, (x, 1310), f"{tick}%", font(35))
    draw.line((chart_x0, 1260, chart_x1, 1260), fill="#444444", width=3)
    image.save(OUT / "figure2_final_outcome_distribution.png", dpi=(300, 300))



def validate_summary_tables() -> None:
    """Cross-check retained data against shipped tables without altering either."""
    aliases = {"Perplexity Pro-based RAG": "Perplexity Pro"}
    with (ROOT / "analysis" / "outcome_tables.csv").open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            system = aliases.get(row["condition"], row["condition"])
            category_index = list(OUTCOME_COLORS).index(row["outcome"])
            if int(row["count"]) != OUTCOME_COUNTS[system][category_index]:
                raise RuntimeError(f"Outcome table mismatch: {system}, {row['outcome']}")
    labels = {label.lower(): label for label in VARIABLES}
    with (ROOT / "analysis" / "variable_summary.csv").open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            system = aliases.get(row["condition"], row["condition"])
            label = labels[row["variable"].lower()]
            average, sd = VARIABLE_SUMMARIES[label][SYSTEMS.index(system)]
            if abs(average - float(row["mean"])) > 0.000501 or abs(sd - float(row["sd"])) > 0.000501:
                raise RuntimeError(f"State table mismatch: {system}, {label}")


if __name__ == "__main__":
    validate_summary_tables()
    make_variable_figure()
    make_outcome_figure()
    print(OUT)
