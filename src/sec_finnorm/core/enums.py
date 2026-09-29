"""
Core enums for sec-finnorm

This module defines all enumeration types used throughout the library:
- PeriodType: Financial statement period types (QTD, YTD, Annual, TTM, Instant)
- StatementType: Financial statement types (Income Statement, Balance Sheet, Cash Flow Statement)
- StatusCode: Result status codes for normalization operations
"""

from enum import Enum


class PeriodType(Enum):
    """
    Financial statement period types.

    Attributes:
        QTD: Quarter-to-date
        YTD: Year-to-date
        Annaul: Full fiscal year (10-K filings for US domestic; 20-F for FPI)
        TTM: Trailing twelve months
        Instant: Point-in-time (Balance Sheet only)
    """

    QTD = "QTD"
    YTD = "YTD"
    Annual = "Annual"
    TTM = "TTM"
    Instant = "Instant"


class StatementType(Enum):
    """
    Financial statement types.

    Attributes:
        INCOME: Income Statement
        BALANCE: Balance Sheet
        CASHFLOW: Cash Flow Statement
    """

    INCOME_STATEMENT = "Income Statement"
    BALANCE_SHEET = "Balance Sheet"
    CASHFLOW_STATEMENT = "Cash Flow Statement"


class StatusCode(Enum):
    """
    Result status codes for normalization operations.

    When a value cannot be computed or retrieved, a StatusCode is returned
    instead of a numeric value to provide transparency on why the operation failed.

    Attributes:
        MISSING: Source data does not exist in the underlying filing
        UNCOMPUTABLE: Required upstream/prerequisite data for calculation is unavailable
        SUSPICIOUS: Value was computed, but failed a consistency/validation check
        NOT_APPLICABLE: Requested data or period type is structurally not applicable
                       (e.g., QTD for an FPI filer)
    """

    MISSING = "Source data does not exist in the underlying filing"
    UNCOMPUTABLE = "Required prerequisite data for the calculation is unavailable"
    SUSPICIOUS = "Value was computed, but failed a validation check"
    NOT_APPLICABLE = "Requested data or period type is structurally not applicable"
