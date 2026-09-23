# SEC Financial Statement Normalization Library

## 1. Purpose

SEC financial statements (via EDGAR) are inconsistent across companies and filings — the same line item can appear with different period bases (cumulative vs. quarterly) depending on the filer and the statement type. sec-finnorm these SEC financial statements (Income Statement, Balance Sheet, Cash Flow Statement) into a single, consistent format so that downstream consumers don't have to reverse-engineer each filer's reporting conventions.

## 2. Problem Statement

- Converting the Cash Flow Statement (CF) into a QTD (quarter-to-date) basis is particularly difficult: SEC filings report CF values cumulatively (YTD), and no standard "quarterly" figure is disclosed.
- More broadly, the period basis (cumulative vs. quarterly) that each statement reports varies table by table and filer by filer, making it hard to produce one uniform output format.
- **Approach**: Use [`edgartools`](https://github.com/dgunning/edgartools) as the underlying data access layer, and build sec-finnorm as a thin library on top of it that focuses solely on providing normalized values and transparent calculation logic — not on raw data retrieval.

## 3. Supported Data (IS / BS / CF)

### 3.1 US Domestic Filers

| Statement               | Supported Period Types                     |
| ----------------------- | ------------------------------------------ |
| **Income Statement**    | QTD / YTD / Annual / TTM                   |
| **Cash Flow Statement** | QTD / YTD / Annual / TTM                   |
| **Balance Sheet**       | Instant (point-in-time; no period concept) |

**Query granularity:**
- **Company**: single or multiple lookup by Ticker or CIK
- **Single filing**: lookup by accession number, or by a specific year + quarter (e.g., "2025 Q2")
- **Multiple filings**: lookup by multiple accession numbers, by date range, or by year/quarter range (e.g., 2024 Q1 – 2025 Q2)

> **Note**: Annual (10-K) filings only provide the `Annual` period type. `YTD` is not separately provided, since for an annual report, Annual == YTD.

### 3.2 FPI (Foreign Private Issuer)

- Applies to Form 20-F / 20-F/A filers.
- **Income Statement** / **Cash Flow Statement**: Annual only
- **Balance Sheet**: Instant
- **QTD / YTD / TTM are not supported** for FPI filers.

## 4. Out of Scope
- Data sources outside SEC EDGAR (private companies, non-US exchange filings, etc.) are not supported.
- Parsing of footnotes or narrative/text disclosures within financial statements is not supported — only numeric line-item data is in scope.

## 5. Period Normalization Rules

### 5.1 Income Statement (QTD / YTD / Annual / TTM)

- **10-Q and 10-Q/A**: QTD and YTD values are used as reported, with no transformation.
- **10-K and 10-K/A**: Annual values are used as reported, with no transformation.
- **TTM (Trailing Twelve Months)**:
    - From a 10-Q: `TTM(Y, Q) = YTD(Y, Q) + FY(Y-1) - YTD(Y-1, Q)`
    - From a 10-K: Annual value **is** the TTM value.

### 5.2 Balance Sheet

- Reported as an **Instant** (point-in-time balance); no period conversion is required or applicable.

### 5.3 Cash Flow Statement (QTD / YTD / Annual / TTM)

- **YTD**: Used as reported from the CF statement, with no transformation.
- **Annual**: Used as reported from the FY filing, with no transformation.
- **QTD** (derived): `QTD(Q) = YTD(Q) - YTD(Q-1)`
- **TTM**:
    - From a 10-Q: `TTM(Y, Q) = YTD(Y, Q) + FY(Y-1) - YTD(Y-1, Q)`
    - From a 10-K: Annual value **is** the TTM value.

### 5.4 Handling Missing Data / Calculation Errors

When a value is missing, cannot be computed, or fails a consistency check, the library returns a **status code** instead of a numeric value (in which case `value` is set to `null`):

|Status Code|Meaning|
|---|---|
|`MISSING`|Source data does not exist in the underlying filing|
|`UNCOMPUTABLE`|Required upstream/prerequisite data for the calculation is unavailable|
|`SUSPICIOUS`|A value was computed, but failed a consistency/validation check|
|`NOT_APPLICABLE`|The requested data or period type is structurally not applicable (e.g., QTD for an FPI filer)|

An optional **detailed calculation object** can be returned alongside the value, containing the source values used, their accession numbers, and the formula applied — for full traceability.

## 6. Derived Metrics

| Statement               | Metrics                                  |
| ----------------------- | ---------------------------------------- |
| **Income Statement**    | QoQ, YoY (% change and absolute change)  |
| **Cash Flow Statement** | QoQ, YoY (% change and absolute change)  |
| **Balance Sheet**       | QoQ Delta, YoY Delta (change in balance) |

## 7. Query API

### 7.1 Filing Conditions and Period

- **Amendment inclusion**: `amendments=True/False`
- **Period specification**:
    - By date range: `by_date(start, end)`
    - By year/quarter range: `by_quarter(start, end)`

```python
# Define filing conditions and period
filings = get_filings(
    companies=["AAPL", "0000320193", ...],
    amendments=True,  # True/False
    period=by_date("2024-01-01", "2025-06-30"),
)

# Or, using quarter range
filings = get_filings(
    companies=["AAPL", "0000320193", ...],
    amendments=False,  # True/False
    period=by_quarter("2024Q1", "2025Q2"),
)
```

**Building a filing list directly from accession numbers:**

```python
filings = get_filings(accessions=[acc_num1, acc_num2])
```

### 7.2 Financial Statements

Retrieve normalized financial statement data.

**Parameters:**

- `period_type` (Enum): `QTD`, `YTD`, `Annual`, `TTM`
- `statement` (Enum): `INCOME`, `BALANCE`, `CASHFLOW`

```python
filing.get_financials(period_type=..., statement=...)
filing.get_financials(period_type=Eumn.QTD, statement=Enum.INCOME)
```

## 8. Role of `edgartools`

- Handles collection and first-pass parsing of raw SEC EDGAR filing data (raw XBRL / financial statement access).
- sec-finnorm consumes this raw data as input and performs period normalization, standard line-item mapping, and derived-metric calculation as an upper layer built on top of it.

## 9. MVP Scope
- Normalized SEC financial statements (IS / BS / CF)
- Filing lookup by accession number, and by single or range of year/quarter
- Period normalization: QTD / YTD / Annual / TTM for IS/CF, Instant for BS
- FPI (20-F) support

## 10. Future Roadmap (Post-MVP)

- Derived metrics: QoQ / YoY for IS and CF; QoQ / YoY Delta for BS
- Support for Statement of Stockholders' Equity
- Support for FPI 6-K financial and period structures
- Support for fiscal year changes
- Caching and local storage support (to improve performance on repeated queries)
- Asynchronous bulk query support
- Data visualization utilities

---

_This document was written with Claude._