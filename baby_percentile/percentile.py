"""WHO weight-for-age percentile calculation using the LMS method.

Data: WHO Child Growth Standards (0-1826 days, both sexes).
Source: https://github.com/WorldHealthOrganization/anthro (GPL-3.0).
"""

import math
import os
from functools import lru_cache

DATA_PATH = os.path.join(os.path.dirname(__file__), 'data', 'weianthro.txt')

MAX_AGE_DAYS = 1826  # WHO standards cover 0-5 years inclusive
SEX_BOY = 1
SEX_GIRL = 2


@lru_cache(maxsize=1)
def _load_table():
    """Return {(sex, age_days): (L, M, S)} from the WHO LMS file."""
    table = {}
    with open(DATA_PATH, 'r') as f:
        header = f.readline()  # sex\tage\tl\tm\ts
        assert header.strip().split('\t') == ['sex', 'age', 'l', 'm', 's']
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) != 5:
                continue
            sex = int(parts[0])
            age = int(parts[1])
            L = float(parts[2])
            M = float(parts[3])
            S = float(parts[4])
            table[(sex, age)] = (L, M, S)
    return table


def _normal_cdf(z):
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


def weight_percentile(sex, age_days, weight_kg):
    """Compute z-score and percentile for weight-for-age.

    sex: 1 (boy) or 2 (girl)
    age_days: integer days since birth, 0..1826
    weight_kg: positive float

    Returns dict with z, percentile, L, M, S.
    """
    if sex not in (SEX_BOY, SEX_GIRL):
        raise ValueError("sex must be 1 (boy) or 2 (girl)")
    if age_days < 0 or age_days > MAX_AGE_DAYS:
        raise ValueError(
            f"age_days {age_days} outside WHO standard range 0-{MAX_AGE_DAYS}"
        )
    if weight_kg <= 0:
        raise ValueError("weight_kg must be positive")

    table = _load_table()
    L, M, S = table[(sex, age_days)]

    if L == 0:
        z = math.log(weight_kg / M) / S
    else:
        z = ((weight_kg / M) ** L - 1.0) / (L * S)

    percentile = _normal_cdf(z) * 100.0
    return {
        'z': z,
        'percentile': percentile,
        'L': L,
        'M': M,
        'S': S,
    }
