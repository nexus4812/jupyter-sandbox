from datetime import date
from typing import TypedDict

from dateutil.relativedelta import relativedelta


class WalkForwardDates(TypedDict):
    in_sample_start: date
    in_sample_end: date
    out_sample_start: date
    out_sample_end: date


def create_walk_forward_test_date(
    base_date: date, in_sample_payload_year: int, out_sample_payload_year: int
) -> WalkForwardDates:
    in_sample_start = base_date
    in_sample_end = in_sample_start + relativedelta.relativedelta(
        years=in_sample_payload_year, days=-1
    )

    out_sample_start = in_sample_end + relativedelta.relativedelta(days=1)
    out_sample_end = out_sample_start + relativedelta.relativedelta(
        years=out_sample_payload_year, days=-1
    )

    r: WalkForwardDates
    r = {
        "in_sample_start": in_sample_start,
        "in_sample_end": in_sample_end,
        "out_sample_start": out_sample_start,
        "out_sample_end": out_sample_end,
    }

    return r
