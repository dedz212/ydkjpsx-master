import os
import sys
import json

def process_94_file_psxexe(kyuhuyon_file):
    print("PS-X EXE | Reading the contents of a .94 file:", kyuhuyon_file)
    with open(kyuhuyon_file, 'rb') as f:
        data = f.read()

    # Find positions for each data block
    magicnum_start = 0x00
    execution_start_address_start = 0x10
    text_section_start_address_start = 0x18
    text_section_size_start = 0x1C
    stack_start_address_start = 0x30
    region_specific_start = 0x4C
    end = 0x800

    # Extracting data
    magicnum = data[magicnum_start:magicnum_start + 8].decode('ascii').strip('\0')
    execution_start_address = hex(int.from_bytes(data[execution_start_address_start:execution_start_address_start + 4], byteorder='little'))
    text_section_start_address = hex(int.from_bytes(data[text_section_start_address_start:text_section_start_address_start + 4], byteorder='little'))
    text_section_size = hex(int.from_bytes(data[text_section_size_start:text_section_size_start + 4], byteorder='little'))
    stack_start_address = hex(int.from_bytes(data[stack_start_address_start:stack_start_address_start + 4], byteorder='little'))
    region_specific = data[region_specific_start:end].replace(b'\x00', b'').replace(b'\xd5', b"'").decode('utf-8').rstrip('\x00')

    # Create a dictionary for the data
    output_data = {
        "magicnum": magicnum,
        "execution_start_address": execution_start_address,
        "text_section_start_address": text_section_start_address,
        "text_section_size": text_section_size,
        "stack_start_address": stack_start_address,
        "region_specific": region_specific
    }

    # Create a folder for the .94 file
    folder_name = os.path.splitext(kyuhuyon_file)[0]
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    
    # Export data to JSON file
    json_file = os.path.join(folder_name, f'{folder_name}.json')
    print(f'Export data to JSON file {folder_name}.json...')
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=4)

    print(".json processing is complete")


def process_94_file_img(kyuhuyon_file):
    print("IMG | Reading the contents of a .glu file:", kyuhuyon_file)
    with open(kyuhuyon_file, 'rb') as f:
        data = f.read()

    img_counter = 1
    img_data = []

    # Find the start of each IMG block
    start_index = data.find(b'\x49\x4D\x47\x34')
    if start_index == -1:
        print("No data found for .img file")
        return

    while start_index != -1:
        print(f"Data processing for .img file {img_counter}...")
        end_index = data.find(b'\x56\x41\x47\x70', start_index + 1)  # IMG block ends when VAG block begins
        if end_index == -1:
            end_index = len(data)
        img_data.append((os.path.splitext(kyuhuyon_file)[0], data[start_index:end_index]))
        start_index = data.find(b'\x49\x4D\x47\x34', end_index)  # Find the start of the next IMG block

        img_counter += 1

    # Create a folder for the .glu file
    folder_name = os.path.splitext(kyuhuyon_file)[0]
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    
    # Export to .img
    print("Exporting data to .img files...")
    for prefix, img_block in img_data:
        img_filename = os.path.join(folder_name, f'{prefix}.IMG')
        with open(img_filename, 'wb') as f:
            f.write(img_block)

    print(".img processing is complete")

def process_94_file_vag(kyuhuyon_file):
    print("VAG | Reading the contents of a .94 file:", kyuhuyon_file)
    with open(kyuhuyon_file, 'rb') as f:
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
    while start_index != -1:
        # Find the name offset
        name_offset = start_index + 0x20
        name_length = data.find(b'\x00', name_offset) - name_offset
        name = data[name_offset:name_offset + name_length].decode('utf-8').rstrip('\x00')
        vag_names.append(name)

        start_index = data.find(b'\x56\x41\x47\x70', start_index + 1)

    start_index = data.find(b'\x56\x41\x47\x70')
    while start_index != -1:
        # Find the name offset
        name_offset = start_index + 0x20
        name_length = data.find(b'\x00', name_offset) - name_offset
        name = data[name_offset:name_offset + name_length].decode('utf-8').rstrip('\x00')
        vag_names.append(name)

        # Find the end of VAG block
        end_index = start_index + int.from_bytes(data[start_index + 0xE:start_index + 0x10], byteorder='big') + 0x10
        vag_data.append((vag_names[vag_counter - 1], data[start_index:end_index]))

        start_index = data.find(b'\x56\x41\x47\x70', end_index)

        vag_counter += 1

    # Create a folder for the .94 file
    folder_name = os.path.splitext(kyuhuyon_file)[0]
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    
    # Export to .vag
    print("Exporting data to .vag files...")
    for prefix, vag_block in vag_data:
        prefix_parts = prefix.split('\\')
        if len(prefix_parts) > 1:
            subfolder_name = os.path.join(folder_name, prefix_parts[0])
            if not os.path.exists(subfolder_name):
                os.makedirs(subfolder_name)
            vag_filename = os.path.join(subfolder_name, f'{prefix_parts[1]}.vag')
        else:
            vag_filename = os.path.join(folder_name, f'{prefix}.vag')
        with open(vag_filename, 'wb') as f:
            f.write(vag_block)

    print(".vag processing is complete")


def is_exe_file(file_path):
    with open(file_path, 'rb') as f:
        first_bytes = f.read(8)
    return b'PS-X' in first_bytes

if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == 'file':
        kyuhuyon_file = sys.argv[2]
        if is_exe_file(kyuhuyon_file):
            process_94_file_psxexe(kyuhuyon_file)
            process_94_file_img(kyuhuyon_file)
            process_94_file_vag(kyuhuyon_file)
        else:
            print("Not a valid 94 file")
    else:
        print("Usage: python 94.py file <filename>")
        print("Example: python glu.py file SLUS_011.94")