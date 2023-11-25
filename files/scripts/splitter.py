import json

def split_json_file(input_file):
    # Read the original JSON file
    with open(input_file, 'r') as file:
        data = json.load(file)

    # Iterate over the elements and write each to a separate file
    for i, element in enumerate(data):
        output_file = f'output_{i+1}.json'
        with open(output_file, 'w') as file:
            json.dump([element], file, indent=4)  # Wrap element in a list and write to file

    print(f"Split into {len(data)} files.")

# Replace 'your_file.json' with the path to your JSON file
split_json_file('data/mighty-tracking-annotated-11-18-23.json')