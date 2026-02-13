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

for file_path in files:
    file_path = os.path.join(src, file_path)
    df = pd.read_csv(file_path, sep="\t")
    
    file_path = os.path.basename(file_path)
    file_name = os.path.splitext(file_path)[0]

    df.to_excel("mapping.xls", file_name)
