from dataclasses import dataclass

import pandas as pd

from sql_test_kit.table import AbstractTable


@dataclass
class InterpolationData:
    table: AbstractTable
    data: pd.DataFrame
