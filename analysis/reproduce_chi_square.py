from __future__ import annotations

import math
import zipfile
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET


SCENARIO_ORDER = [
    "교착 상태 장기화",
    "내부 붕괴",
    "외교적 해결",
    "전면전 확전",
    "제한적 국지 충돌",
]

MODEL_BY_FILE = {
    "gemini.xlsx": "Gemini",
    "gpt.xlsx": "GPT",
    "opus 4.xlsx": "Claude opus-4",
    "perplexity.xlsx": "Perplexity_Pro",
}


def column_name(index: int) -> str:
    letters = ""
    while index:
        index, remainder = divmod(index - 1, 26)
        letters = chr(65 + remainder) + letters
    return letters


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def read_shared_strings(zf: zipfile.ZipFile) -> list[str]:
    if "xl/sharedStrings.xml" not in zf.namelist():
        return []
    root = ET.fromstring(zf.read("xl/sharedStrings.xml"))
    strings: list[str] = []
    for item in root:
        texts = [node.text or "" for node in item.iter() if local_name(node.tag) == "t"]
        strings.append("".join(texts))
    return strings


def workbook_sheet_paths(zf: zipfile.ZipFile) -> list[tuple[str, str]]:
    wb_root = ET.fromstring(zf.read("xl/workbook.xml"))
    rel_root = ET.fromstring(zf.read("xl/_rels/workbook.xml.rels"))
    rels = {
        rel.attrib["Id"]: "xl/" + rel.attrib["Target"].lstrip("/")
        for rel in rel_root
    }

    sheets: list[tuple[str, str]] = []
    for sheet in wb_root.iter():
        if local_name(sheet.tag) != "sheet":
            continue
        rel_id = sheet.attrib.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id")
        if rel_id in rels:
            sheets.append((sheet.attrib["name"], rels[rel_id]))
    return sheets


def cell_value(cell: ET.Element, shared_strings: list[str]) -> Any:
    cell_type = cell.attrib.get("t")
    if cell_type == "inlineStr":
        texts = [node.text or "" for node in cell.iter() if local_name(node.tag) == "t"]
        return "".join(texts)

    value_node = next((node for node in cell if local_name(node.tag) == "v"), None)
    if value_node is None or value_node.text is None:
        return ""

    raw = value_node.text
    if cell_type == "s":
        return shared_strings[int(raw)]
    if cell_type == "b":
        return raw == "1"
    try:
        number = float(raw)
    except ValueError:
        return raw
    return int(number) if number.is_integer() else number


def read_first_nonempty_sheet(path: Path) -> tuple[str, list[dict[str, Any]]]:
    with zipfile.ZipFile(path) as zf:
        shared_strings = read_shared_strings(zf)
        for sheet_name, sheet_path in workbook_sheet_paths(zf):
            root = ET.fromstring(zf.read(sheet_path))
            rows: list[list[Any]] = []
            for row in root.iter():
                if local_name(row.tag) != "row":
                    continue
                values: dict[int, Any] = {}
                for cell in row:
                    if local_name(cell.tag) != "c":
                        continue
                    ref = cell.attrib.get("r", "")
                    col = 0
                    for char in ref:
                        if char.isalpha():
                            col = col * 26 + ord(char.upper()) - 64
                        else:
                            break
                    values[col] = cell_value(cell, shared_strings)
                if values:
                    max_col = max(values)
                    rows.append([values.get(i, "") for i in range(1, max_col + 1)])

            if not rows:
                continue
            headers = [str(value).strip() for value in rows[0]]
            records = [
                {headers[i]: row[i] if i < len(row) else "" for i in range(len(headers))}
                for row in rows[1:]
                if any(str(value).strip() for value in row)
            ]
            if records:
                return sheet_name, records
    raise ValueError(f"No non-empty worksheet found in {path}")


def is_present(value: Any) -> bool:
    if value is None:
        return False
    text = str(value).strip()
    return bool(text) and text.lower() != "nan"


def clean(value: Any) -> str:
    return str(value).strip()


def crosstab(rows: list[dict[str, str]], model_key: str = "Model") -> tuple[list[str], list[list[int]]]:
    models = sorted({row[model_key] for row in rows})
    counts = {model: Counter() for model in models}
    for row in rows:
        counts[row[model_key]][row["Scenario_Type"]] += 1
    table = [[counts[model].get(scenario, 0) for scenario in SCENARIO_ORDER] for model in models]
    return models, table


def chi_square(table: list[list[int]]) -> tuple[float, int, list[list[float]]]:
    row_totals = [sum(row) for row in table]
    col_totals = [sum(table[row][col] for row in range(len(table))) for col in range(len(table[0]))]
    total = sum(row_totals)
    expected = [
        [row_total * col_total / total for col_total in col_totals]
        for row_total in row_totals
    ]
    statistic = 0.0
    for row_idx, row in enumerate(table):
        for col_idx, observed in enumerate(row):
            exp = expected[row_idx][col_idx]
            if exp:
                statistic += (observed - exp) ** 2 / exp
    df = (len(table) - 1) * (len(table[0]) - 1)
    return statistic, df, expected


def gammaincc(a: float, x: float) -> float:
    if x < 0 or a <= 0:
        raise ValueError("Invalid incomplete gamma arguments")
    if x == 0:
        return 1.0

    eps = 3e-14
    tiny = 1e-300
    gln = math.lgamma(a)

    if x < a + 1:
        ap = a
        total = 1.0 / a
        delta = total
        for _ in range(1000):
            ap += 1
            delta *= x / ap
            total += delta
            if abs(delta) < abs(total) * eps:
                break
        return max(0.0, 1.0 - total * math.exp(-x + a * math.log(x) - gln))

    b = x + 1.0 - a
    c = 1.0 / tiny
    d = 1.0 / b
    h = d
    for i in range(1, 1000):
        an = -i * (i - a)
        b += 2.0
        d = an * d + b
        if abs(d) < tiny:
            d = tiny
        c = b + an / c
        if abs(c) < tiny:
            c = tiny
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < eps:
            break
    return max(0.0, h * math.exp(-x + a * math.log(x) - gln))


def chi_square_sf(statistic: float, df: int) -> float:
    return gammaincc(df / 2.0, statistic / 2.0)


def rows_to_sheet_xml(rows: list[list[Any]]) -> str:
    def escape_text(value: Any) -> str:
        text = "" if value is None else str(value)
        return (
            text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
        )

    sheet_rows = []
    for r_idx, row in enumerate(rows, start=1):
        cells = []
        for c_idx, value in enumerate(row, start=1):
            ref = f"{column_name(c_idx)}{r_idx}"
            if isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value):
                cells.append(f'<c r="{ref}"><v>{value}</v></c>')
            else:
                cells.append(f'<c r="{ref}" t="inlineStr"><is><t>{escape_text(value)}</t></is></c>')
        sheet_rows.append(f'<row r="{r_idx}">{"".join(cells)}</row>')
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        f'<sheetData>{"".join(sheet_rows)}</sheetData></worksheet>'
    )


def write_xlsx(path: Path, sheets: dict[str, list[list[Any]]]) -> None:
    content_types = [
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">',
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>',
        '<Default Extension="xml" ContentType="application/xml"/>',
        '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>',
        '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>',
    ]
    for idx in range(1, len(sheets) + 1):
        content_types.append(
            f'<Override PartName="/xl/worksheets/sheet{idx}.xml" '
            'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
        )
    content_types.append("</Types>")

    workbook_sheets = []
    workbook_rels = []
    for idx, sheet_name in enumerate(sheets, start=1):
        workbook_sheets.append(
            f'<sheet name="{sheet_name}" sheetId="{idx}" '
            f'r:id="rId{idx}"/>'
        )
        workbook_rels.append(
            f'<Relationship Id="rId{idx}" '
            'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" '
            f'Target="worksheets/sheet{idx}.xml"/>'
        )
    workbook_rels.append(
        f'<Relationship Id="rId{len(sheets) + 1}" '
        'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" '
        'Target="styles.xml"/>'
    )

    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", "".join(content_types))
        zf.writestr(
            "_rels/.rels",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
            "</Relationships>",
        )
        zf.writestr(
            "xl/workbook.xml",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
            'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
            f'<sheets>{"".join(workbook_sheets)}</sheets></workbook>',
        )
        zf.writestr(
            "xl/_rels/workbook.xml.rels",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            f'{"".join(workbook_rels)}</Relationships>',
        )
        zf.writestr(
            "xl/styles.xml",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
            '<fonts count="1"><font><sz val="11"/><name val="Calibri"/></font></fonts>'
            '<fills count="1"><fill><patternFill patternType="none"/></fill></fills>'
            '<borders count="1"><border/></borders>'
            '<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>'
            '<cellXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/></cellXfs>'
            '<cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles>'
            '<dxfs count="0"/>'
            '<tableStyles count="0" defaultTableStyle="TableStyleMedium9" defaultPivotStyle="PivotStyleLight16"/>'
            "</styleSheet>",
        )
        for idx, rows in enumerate(sheets.values(), start=1):
            zf.writestr(f"xl/worksheets/sheet{idx}.xml", rows_to_sheet_xml(rows))


def table_rows(models: list[str], table: list[list[Any]]) -> list[list[Any]]:
    return [["Model", *SCENARIO_ORDER], *[[model, *row] for model, row in zip(models, table)]]


def main() -> None:
    output_dir = Path(__file__).resolve().parent
    results_dir = output_dir.parent
    data_dir = results_dir / "Quantitative_Summaries"
    output_dir.mkdir(exist_ok=True)

    all_rows: list[dict[str, Any]] = []
    data_quality: list[list[Any]] = [["File", "Sheet", "Rows", "Rows with Scenario_Type", "Rows with Model", "Model value counts"]]

    for path in sorted(data_dir.glob("*.xlsx")):
        sheet_name, records = read_first_nonempty_sheet(path)
        model_counts = Counter(clean(row.get("Model")) if is_present(row.get("Model")) else "nan" for row in records)
        data_quality.append(
            [
                path.name,
                sheet_name,
                len(records),
                sum(is_present(row.get("Scenario_Type")) for row in records),
                sum(is_present(row.get("Model")) for row in records),
                ", ".join(f"{key}: {value}" for key, value in model_counts.items()),
            ]
        )
        file_model = MODEL_BY_FILE.get(path.name.lower())
        for row in records:
            scenario = clean(row.get("Scenario_Type"))
            if not scenario:
                continue
            all_rows.append(
                {
                    "File": path.name,
                    "Model": clean(row.get("Model")) if is_present(row.get("Model")) else "",
                    "Corrected_Model": file_model or clean(row.get("Model")),
                    "Scenario_Type": scenario,
                }
            )

    original_rows = [
        {"Model": row["Model"], "Scenario_Type": row["Scenario_Type"]}
        for row in all_rows
        if row["Model"] and row["Scenario_Type"] in SCENARIO_ORDER
    ]
    corrected_rows = [
        {"Model": row["Corrected_Model"], "Scenario_Type": row["Scenario_Type"]}
        for row in all_rows
        if row["Corrected_Model"] and row["Scenario_Type"] in SCENARIO_ORDER
    ]

    original_models, original_table = crosstab(original_rows)
    corrected_models, corrected_table = crosstab(corrected_rows)
    original_stat, original_df, _ = chi_square(original_table)
    corrected_stat, corrected_df, corrected_expected = chi_square(corrected_table)
    original_p = chi_square_sf(original_stat, original_df)
    corrected_p = chi_square_sf(corrected_stat, corrected_df)

    row_pct = [
        [round(value / sum(row) * 100, 2) if sum(row) else 0 for value in row]
        for row in corrected_table
    ]
    expected = [[round(value, 6) for value in row] for row in corrected_expected]

    summary = [
        ["Analysis", "Rows used", "Chi-square", "df", "p-value", "Interpretation"],
        ["Original code behavior", len(original_rows), original_stat, original_df, original_p, "Significant at 0.05" if original_p < 0.05 else "Not significant at 0.05"],
        ["File-name model corrected", len(corrected_rows), corrected_stat, corrected_df, corrected_p, "Significant at 0.05" if corrected_p < 0.05 else "Not significant at 0.05"],
        ["", "", "", "", "", ""],
        [
            "Note",
            "Original code excludes rows where Model is blank. Perplexity.xlsx has 29 blank Model cells, so the corrected analysis assigns model names from file identity.",
            "",
            "",
            "",
            "",
        ],
    ]

    output_path = output_dir / "scenario_chi_square_summary.xlsx"
    write_xlsx(
        output_path,
        {
            "Summary": summary,
            "Corrected_Counts": table_rows(corrected_models, corrected_table),
            "Corrected_RowPct": table_rows(corrected_models, row_pct),
            "Original_Code_Counts": table_rows(original_models, original_table),
            "Corrected_Expected": table_rows(corrected_models, expected),
            "Data_Quality": data_quality,
        },
    )

    print(f"Wrote {output_path}")
    print(f"Corrected chi-square({corrected_df}) = {corrected_stat:.6f}, p = {corrected_p:.8g}")


if __name__ == "__main__":
    main()
