"""Module of calling edgartools related with filing

This module provides calling edgartools apis related about filing.


"""

import logging
from edgar import Filing, Company, get_by_accession_number

logger = logging.getLogger(__name__)


def _get_by_accessions(accessions: list[str]) -> dict[str, Filing]:
    filings: list[Filing] = []

    for accession in accessions:
        try:
            filing = get_by_accession_number(accession)
        except AssertionError as e:
            logger.exception(f"fetching filing by accession number failed: {e}")
            raise AssertionError from e

        if filing:
            filings.append(filing)


def _get_by_dates(companies: list[str], start: str, end: str) -> dict[str, Filing]:
    pass


def _get_by_quarter(
    companies: list[str], start: tuple[int, int], end: tuple[int, int]
) -> dict[str, Filing]:
    pass
