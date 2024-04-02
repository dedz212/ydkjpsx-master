import os
import sys
import json


def process_cnf_file_(cnf_file):
    print("Reading the contents of a .inf file:", cnf_file)
    with open(cnf_file, 'rb') as f:
        data = f.read()

    # Extracting data containers
    boot = data[0x7:0x19].decode('utf-8')
    version = data[0x1a:0x1b].decode('utf-8')
    tcb = data[0x23:0x24].decode('utf-8')
    event  = data[0x2e:0x30].decode('utf-8')
    stack = data[0x3a:0x42].decode('utf-8')

    # Create a dictionary for the data
    output_data = {
        "boot": boot,
        "version": version,
        "tcb": tcb,
        "event": event,
        "stack": stack
    }
    
    # Export data to JSON file
    name = os.path.splitext(cnf_file)[0]
    json_file = os.path.join(f'{name}.json')
    print(f'Export data to JSON file {name}.json...')
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=4)

    print(".json processing is complete")

if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == 'file':
        cnf_file = sys.argv[2]
        process_cnf_file_(cnf_file)
    else:
        print("Usage: python cnf.py file <filename>")
        print("Example: python cnf.py file HTE.INF")