file_path = "dataset_for_excel/relative_time4.txt"

with open(file_path, "r", encoding="utf-8") as f:
    count = 0
    lines = f.readlines()
    for line in lines:
        count += line.count("\t")
        
    f.close()
    
print(count)