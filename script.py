files = [
    "dataset_final2/human_centric.txt",
    "dataset_final2/idiomatic.txt",
    "dataset_final2/imperial_units.txt",
    "dataset_final2/informal.txt",
    "dataset_final2/international_terms.txt",
    "dataset_final2/metric_units.txt",
    "dataset_final2/numerical.txt",
    "dataset_final2/relative_time1.txt",
    "dataset_final2/relative_time2.txt",
    "dataset_final2/relative_time3.txt",
    "dataset_final2/relative_time4.txt",
]

for file_path in files:
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    updated_lines = [line.rstrip("\n") + "\t.\n" for line in lines]

    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(updated_lines)

print("All files updated successfully.")