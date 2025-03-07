from flask import Flask, render_template, request
from typing import List, Dict
from tabulate import tabulate
import random

app = Flask(__name__)

class Column:
    def __init__(self, name: str, data: List[int]):
        self.name = name
        self.data = data
    
    def get_data(self) -> List[int]:
        return self.data

class Table:
    def __init__(self, name: str, columns: Dict[str, Column]):
        self.name = name
        self.columns = columns
    
    def get_column(self, name: str) -> Column:
        if name not in self.columns:
            raise ValueError(f"No column found with the name: {name}")
        return self.columns[name]
    
    def display_table(self):
        headers = ["Index"] + list(self.columns.keys())
        rows = list(zip(*[col.get_data() for col in self.columns.values()]))
        indexed_rows = [[i] + list(row) for i, row in enumerate(rows)]
        return headers, indexed_rows

class ComputationEngine:
    def __init__(self, table: Table):
        self.table = table
        self.computed_columns: Dict[str, List[int]] = {}
    
    def compute_sum(self, new_col: str, col1: str, col2: str):
        data1 = self.table.get_column(col1).get_data()
        data2 = self.table.get_column(col2).get_data()
        self.computed_columns[new_col] = [x + y for x, y in zip(data1, data2)]
    
    def compute_diff(self, new_col: str, col1: str, col2: str):
        data1 = self.table.get_column(col1).get_data()
        data2 = self.table.get_column(col2).get_data()
        self.computed_columns[new_col] = [x - y for x, y in zip(data1, data2)]
    
    def get_computed_column(self, name: str) -> List[int]:
        if name not in self.computed_columns:
            raise ValueError(f"No computed column found with the name: {name}")
        return self.computed_columns[name]

data = {
    "col1": Column("col1", [1, 2, 3]),
    "col2": Column("col2", [4, 5, 6])
}

table = Table("TestTable", data)
engine = ComputationEngine(table)

engine.compute_sum("sum_col", "col1", "col2")
engine.compute_diff("diff_col", "col1", "col2")

@app.route('/')
def index():
    headers, rows = table.display_table()
    # Include the sum and diff columns in the rows
    sum_column = engine.get_computed_column("sum_col")
    diff_column = engine.get_computed_column("diff_col")
    
    for i, row in enumerate(rows):
        row.append(sum_column[i])
        row.append(diff_column[i])
    
    headers += ["Sum", "Difference"]  # Add headers for the sum and diff columns
    return render_template('index.html', headers=headers, rows=rows)

@app.route('/refresh', methods=['POST'])
def refresh_table():
    new_data = {
        "col1": Column("col1", [random.randint(1, 10) for _ in range(5)]),
        "col2": Column("col2", [random.randint(1, 10) for _ in range(5)])
    }
    
    new_table = Table("TestTable", new_data)
    new_engine = ComputationEngine(new_table)
    
    new_engine.compute_sum("sum_col", "col1", "col2")
    new_engine.compute_diff("diff_col", "col1", "col2")

    headers, rows = new_table.display_table()
    
    sum_column = new_engine.get_computed_column("sum_col")
    diff_column = new_engine.get_computed_column("diff_col")
    
    for i, row in enumerate(rows):
        row.append(sum_column[i])
        row.append(diff_column[i])

    headers += ["Sum", "Difference"]
    
    return render_template('index.html', headers=headers, rows=rows)

if __name__ == '__main__':
    app.run(debug=True)
