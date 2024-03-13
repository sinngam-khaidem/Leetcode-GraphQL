import json
import csv

with open('coding-questions-sql-with-output.json', 'r') as json_file:
    data = json.load(json_file)

# Specify the keys you want to include in the CSV
selected_keys = ["questionFrontendId", "title", "titleSlug","difficulty", "tags"]

# Specify CSV file name
csv_file_name = 'coding-questions-sql-with-output.csv'

# Write CSV file
with open(csv_file_name, 'w', newline='') as csv_file:
    # Create a CSV writer object
    csv_writer = csv.writer(csv_file)

    # Write header
    csv_writer.writerow(selected_keys)

    # Write data
    for row in data:
        # Extract values for selected keys
        selected_values = [row[key] for key in selected_keys]
        csv_writer.writerow(selected_values)

print(f'Conversion completed. CSV file saved as {csv_file_name}')
