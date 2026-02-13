import pandas as pd
import os

src = "dataset_for_excel"
files = [
    "human_centric.txt",
    "idiomatic.txt",
    "imperial_units.txt",
    "informal.txt",
    "international_terms.txt",
    "metric_units.txt",
    "numerical.txt",
    "relative_time1.txt",
    "relative_time2.txt",
    "relative_time3.txt",
    "relative_time4.txt",
]

output_file = "mapping.xlsx"

with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
    for fname in files:
        full_path = os.path.join(src, fname)
        df = pd.read_csv(full_path, sep="\t", header=None)
        sheet_name = os.path.splitext(fname)[0]

        df.to_excel(
            writer,
            sheet_name=sheet_name,
            index=False,
            header=False
        )
