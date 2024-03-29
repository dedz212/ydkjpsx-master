import os
import sys
import json

def process_glu_file_qbd(glu_file):
    print("Reading the contents of a .glu file...")
    with open(glu_file, 'rb') as f:
        data = f.read()

    # Getting the question type
    if data[0x808] != 0x01:
        print("It's not a simple question")
        return

    # Find positions for each data block
    id_start = 0x804
    category_start = 0x819
    question_start = 0x868
    options_start = 0x930

    # Extracting data
    id_data = data[id_start:id_start + 3].replace(b'\x00', b'').replace(b'\xd5', b"'").decode('utf-8').rstrip('\x00')
    category_data = data[category_start:question_start].replace(b'\x00', b'').replace(b'\xd5', b"'").decode('utf-8').rstrip('\x00')
    question_data = data[question_start:options_start].replace(b'\x00', b'').replace(b'\xd5', b"'").decode('utf-8').rstrip('\x00')
    options_data = [data[options_start + i:options_start + i + 64].replace(b'\x00', b'').replace(b'\xd5', b"'").decode('utf-8').rstrip('\x00')
                    for i in range(0, 256, 64)]
    
    # Identifying the correct answer
    correct_answer_position = data[0xA38]

    # Create a dictionary for the data
    output_data = {
        "id": id_data,
        "category": category_data,
        "question": question_data,
        "answers": {str(i + 1): option for i, option in enumerate(options_data)},
        "true": correct_answer_position
    }

    # Export data to JSON file
    print(f'Export data to JSON file {id_data}.json...')
    with open(f'{id_data}.json', 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=4)

    print(".json processing is complete")


def process_glu_file_vag(glu_file):
    print("Reading the contents of a .glu file...")
    with open(glu_file, 'rb') as f:
        data = f.read()

    vag_counter = 1
    vag_data = []
    vag_names = []
    prefix = None

    # Find the start of each VAG block
    start_index = data.find(b'\x56\x41\x47\x70')
    if start_index == -1:
        print("No data found for .vag file")
        return

    # Find .vag file names
    name_index = data.find(b'.VAG')
    while name_index != -1:
        name_start = name_index - 8
        name = data[name_start:name_index].decode('utf-8')
        vag_names.append(name)
        name_index = data.find(b'.VAG', name_index + 1)

    while start_index != -1:
        print(f"Data processing for .vag file {vag_counter}...")
        end_index = data.find(b'\x56\x41\x47\x70', start_index + 1)
        if end_index == -1:
            end_index = len(data)
        vag_data.append((vag_names[vag_counter - 1], data[start_index:end_index]))
        start_index = end_index

        # Add end-of-file check condition
        if start_index >= len(data):
            break

        vag_counter += 1

    # Export to .vag
    print("Exporting data to .vag files...")
    for prefix, vag_block in vag_data:
        vag_filename = f'{prefix}.vag'
        with open(vag_filename, 'wb') as f:
            f.write(vag_block)

    print(".vag processing is complete")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python glu.py <filename .glu>")
        print("Example: python glu.py BUA.GLU")
    else:
        glu_file = sys.argv[1]
        process_glu_file_qbd(glu_file)
        process_glu_file_vag(glu_file)