"""Collection of SEC filings and the entry points for retrieving them.

IMPORTANT:
All processing is based on the **fiscal period end date**
(`period_of_report`), NOT the filing date. Range queries and period
matching are determined by `period_of_report`.

This module provides `FilingCollection`, a container that holds and manages
a list of `Filing` objects. It is the primary public interface for looking up
SEC EDGAR filings before extracting financial statements from them.

Filings can be retrieved in three ways, each exposed as a classmethod that
returns a `FilingCollection`:

- `from_quarters()`: by company and a fiscal year/quarter range
- `from_dates()`: by company and a period-of-report date range (YYYY-mm-dd)
- `from_accessions()`: by explicit accession numbers

The collection stores two lists and derives the third:

- `all_filings`: every filing returned by the query
- `amended_filings`: amendment filings
- `original_filings`: filings submitted without amendment

The relationship is always `all = original + amended`. Iterating over the
collection (`for filing in collection`) and `len(collection)` are based on
`all_filings`.

Notes:
    - Comparisons between filings use `accession_number`, not object identity.
    - Raw data access is delegated to the adapter layer (`adapters`), so this
      module contains no direct calls to edgartools.
"""

from typing import Iterator, Self

from edgar import Filing


class FilingCollection:
    def __init__(self, original_filings: list[Filing], amended_filings: list[Filing]):
        self._original = original_filings
        self._amended = amended_filings

    def __iter__(self) -> Iterator[Filing]:
        return iter(self.all_filings)

    def __len__(self) -> int:
        return len(self._original + self._amended)

    @classmethod
    def from_quarters(
        cls,
        companies: list[str],
        *,
        start: tuple[int, int],
        end: tuple[int, int],
        include_amendments: bool,
    ) -> Self:
        pass

    @classmethod
    def from_dates(
        cls, companies: list[str], *, start: str, end: str, include_amendments: bool
    ) -> Self:
        pass

    @classmethod
    def from_accessions(cls, *, accessions: list[str], include_amendments: bool) -> Self:
        pass

    @property
    def all_filings(self) -> list[Filing]:
        return self._original + self._amended

    @property
    def origianl_filings(self) -> list[Filing]:
        return list(self._original)

    @property
    def amended_filings(self) -> list[Filing]:
        return list(self._amended)
