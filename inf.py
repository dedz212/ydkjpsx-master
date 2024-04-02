import os
import sys
import json

def process_data(data_block):
    return data_block.replace(b'\x00', b'').replace(b'\xd2', b'\xe2\x80\x9c').replace(b'\xd3', b'\xe2\x80\x9d').replace(b'\xd4', b"\xe2\x80\x98").replace(b'\xd5', b"\xe2\x80\x99").replace(b'\x96', b"\xC3\xB1").replace(b'\xaa', b'\xe2\x84\xa2').replace(b'\x7B', b'').replace(b'\x97', b'o').replace(b'\xC9', b'\xe2\x80\xa6').decode('utf-8', errors='ignore').rstrip('\x00')

def process_inf_file_(inf_file):
    print("Reading the contents of a .inf file:", inf_file)
    with open(inf_file, 'rb') as f:
        data = f.read()

    # Initialize dictionary for output data
    infos = {}

    # Extracting data containers
    mape_id = process_data(data[0x0:0x3])
    container_start = 0x40
    container_size = 0x68
    offset = container_start  # Starting offset of the containers

    for _ in range(15):
        # Extracting content_id
        content_id = process_data(data[offset + 4:offset + 7])
        # Extracting category_data
        category_data = process_data(data[offset + 24:offset + 63])

        # Extracting type_data
        type_byte = data[offset + 8]
        if type_byte == 0x01:
            type_data = "Simple Question"
        elif type_byte == 0x02:
            type_data = "DisOrDat"
        elif type_byte == 0x03:
            type_data = "Wendithap'n"
        elif type_byte == 0x04:
            type_data = "Coinkydink"
        elif type_byte == 0x05:
            type_data = "Jack Attack"
        else:
            print('wtf?')
            return

        infos[content_id] = {
            "category": category_data,
            "type": type_data
        }

        offset += container_size

    # Create a dictionary for the data
    output_data = {
        mape_id: [infos]
    }
    
    # Export data to JSON file
    name = os.path.splitext(inf_file)[0]
    json_file = os.path.join(f'{name}.json')
    print(f'Export data to JSON file {name}.json...')
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=4)

    print(".json processing is complete")

if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == 'file':
        inf_file = sys.argv[2]
        process_inf_file_(inf_file)
    else:
        print("Usage: python inf.py file <filename>")
        print("Example: python inf.py file HTE.INF")