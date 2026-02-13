import os

# src = "dataset_final2"
src  = "dataset_for_excel"

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
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    updated_lines = []
    for line in lines:
        if line.endswith("\t.\n"):
            line = line[:-3] + "\t\n"
        elif line.endswith("\t."):
            line = line[:-2] + "\t"
        updated_lines.append(line)

    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(updated_lines)

print("All files updated successfully.")