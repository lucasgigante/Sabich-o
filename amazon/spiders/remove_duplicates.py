import csv

def remove_duplicates(input_file, column_name):
    seen = set()
    unique_data = []
    
    # Read the data into memory
    with open(input_file, 'r', encoding='latin-1') as file:
        reader = csv.DictReader(file)
        header = reader.fieldnames
        for row in reader:
            if row[column_name] not in seen:
                seen.add(row[column_name])
                unique_data.append(row)

    # Rewrite data back to the same file after clearing its contents
    with open(input_file, 'w', newline='', encoding='latin-1') as file:
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        writer.writerows(unique_data)
