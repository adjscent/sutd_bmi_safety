import os
import sys
import re

def get_csv_files(folder):
    return [f for f in os.listdir(folder) if f.endswith('.csv')]

def extract_action(filename):
    match = re.search(r'_(.*?)_', filename)
    return match.group(1) if match else None

def count_actions(folder):
    action_counts = {}
    for filename in get_csv_files(folder):
        action = extract_action(filename)
        if action:
            action_counts[action] = action_counts.get(action, 0) + 1
    return action_counts

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python check_data.py <folder>")
        sys.exit(1)
    folder = sys.argv[1]
    if not os.path.isdir(folder):
        print(f"Error: {folder} is not a valid directory.")
        sys.exit(1)
    counts = count_actions(folder)
    for action, count in counts.items():
        print(f"{action}: {count}")
    print (f"Total files: {sum(counts.values())}")
    print(f"Unique actions: {len(counts)}")