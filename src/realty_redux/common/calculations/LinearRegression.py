from typing import Self

import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression

class Regression:
    def __init__(self, records: list[dict], dependent: str, independent: list[str] = []):
        self.records = records
        self.dependent = dependent
        self.independent = independent
        self.model: LinearRegression
        self.fit_model()

    def fit_model(self) -> Self:
        y = []
        x = []
        if not self.independent:
            variables = list(self.records[0].keys())
            variables.remove(self.dependent)
            self.independent = variables

        df = pd.DataFrame.from_records(self.records)
        means = df[self.independent].mean()

        for var in self.independent:
            df[var] = df[var].fillna(means[var])

        y_array = np.array(df[self.dependent])
        x_array = np.array(df[self.independent].to_records(index=False).tolist())

        self.model = LinearRegression().fit(x_array, y_array)

        return self
