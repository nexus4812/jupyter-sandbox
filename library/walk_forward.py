from datetime import date, datetime
from typing import TypedDict
from dateutil.relativedelta import relativedelta
import math

class WalkForwardDates(TypedDict):
    in_sample_start: date
    in_sample_end: date
    out_sample_start: date
    out_sample_end: date


def create_walk_forward_test_date(
        base_date: date, in_sample_payload_year: int, out_sample_payload_year: int
) -> WalkForwardDates:
    in_sample_start = base_date
    in_sample_end = in_sample_start + relativedelta(
        years=in_sample_payload_year, days=-1
    )

    out_sample_start = in_sample_end + relativedelta(days=1)
    out_sample_end = out_sample_start + relativedelta(
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


def create_walk_forward_entities(start: date, end: date, in_sample_payload_year: int, out_sample_payload_year: int):
    diff = end - start

    # 開始日と終了日が逆になっていたら終了
    if diff.days < 0:
        raise 'The start date must be earlier than the end date.'

    # 開始日と終了日がテストできないほど短かったら終了
    if (diff.days / 365) < in_sample_payload_year + out_sample_payload_year:
        raise 'period is too short'

    # サンプル期間の方が短かったらエラー
    if in_sample_payload_year < out_sample_payload_year:
        raise 'Sample period must be longer than out sample'

    # 何回テストできるか？
    times = math.floor((diff.days / 365) / (in_sample_payload_year + out_sample_payload_year))

    result = []
    tmp_start = start
    for i in range(times):
        sample = create_walk_forward_test_date(
            tmp_start,
            in_sample_payload_year,
            out_sample_payload_year,
        )
        result.append(sample)
        tmp_start = sample['out_sample_end'] + relativedelta(days=+1)

    print(result[0])
    print(result[1])


create_walk_forward_entities(
    datetime.strptime("2010-01-01", "%Y-%m-%d"),
    datetime.strptime("2016-01-01", "%Y-%m-%d"),
    2,
    1
)
