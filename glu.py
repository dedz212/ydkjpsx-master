import os
import sys
import json

def process_data(data_block):
    return data_block.replace(b'\x00', b'').replace(b'\xd2', b'\xe2\x80\x9c').replace(b'\xd3', b'\xe2\x80\x9d').replace(b'\xd4', b"\xe2\x80\x98").replace(b'\xd5', b"\xe2\x80\x99").replace(b'\x96', b"\xC3\xB1").replace(b'\xaa', b'\xe2\x84\xa2').replace(b'\x7B', b'').replace(b'\x97', b'o').replace(b'\xC9', b'\xe2\x80\xa6').decode('utf-8').rstrip('\x00')

def process_glu_file_qbd(glu_file, isall=None):
    glu_file_name = os.path.basename(glu_file)
    print(f'QBD | Reading the contents of {glu_file_name} file:')
    with open(glu_file, 'rb') as f:
        data = f.read()
    
    start_index = data.find(b'\x51\x42\x44')
    id_value = data[0x808]
    
    if start_index == -1:
        print("No data found for .qbd file")
        return

    # Getting the question type
    if id_value == 0x01:
        id_type = "Simple Question"
    elif id_value == 0x02:
        id_type = "DisOrDat"
    elif id_value == 0x03:
        id_type = "Wendithap'n"
    elif id_value == 0x04:
        id_type = "Coinkydink"
    elif id_value == 0x05:
        id_type = "Jack Attack"
    else:
        print('wtf?')
        return

    # Find positions for each data block | Defining values of variables
    id_start = 0x804
    category_end = 0x84F
    if id_value == 0x01:
        category_start = 0x819
        question_start = 0x868
        options_start = 0x930
    elif id_value == 0x02:
        category_start = 0x819
        category_end = 0x84F
        question_start = 0x8B0
        question_end = 0x8DF
        left = 0x930
        right = 0x950
    elif id_value == 0x03:
        category_start = 0x818
        question_start = 0x8B0
        question_end = 0x8E0
    elif id_value == 0x04:
        category_start = 0x818
    elif id_value == 0x05:
        category_start = 0x819

    # Extracting data
    id_data = process_data(data[id_start:id_start + 3])
    if id_value == 0x01:
        category_data = process_data(data[category_start:question_start])
        question_data = process_data(data[question_start:options_start])
        options_data = [process_data(data[options_start + i:options_start + i + 64]) for i in range(0, 256, 64)]
        correct_answer_position = data[0xA38] # Identifying the correct answer
    elif id_value == 0x02:
        category_data = process_data(data[category_start:category_end])
        question_data = process_data(data[question_start:question_end])
        answer_mapping = {0: process_data(data[left:left + 16]), 1: process_data(data[right:right + 16])}
        answers = []
        for i in range(7):
            text_offset = 0x970 + 0x20 * i
            text = process_data(data[text_offset:text_offset + 0x20])
            answer_offset = 0xA50 + i * 2
            answer_value = data[answer_offset]
            answer_text = answer_mapping.get(answer_value, "Error")
            answers.append({"text": text, "answer": answer_text})
    elif id_value == 0x03:
        category_data = process_data(data[category_start:category_end])
        question_data = process_data(data[question_start:question_end])
        answer_mapping = {1: "Before", 2: "After", 3: "Never"}
        answers = []
        for i in range(7):
            text_offset = 0x940 + 0x40 * i
            text = process_data(data[text_offset:text_offset + 0x40])
            answer_offset = 0xB00 + i * 2
            answer_value = data[answer_offset]
            answer_text = answer_mapping.get(answer_value, "Error")
            answers.append({"text": text, "answer": answer_text})
    elif id_value == 0x04:
        category_data = process_data(data[category_start:category_end])
        texts = []
        roots = []
        answers = []
        for i in range(6):
            end_offset = 0x860 + 0x40 * i
            end = process_data(data[end_offset:end_offset + 0x40])
            texts.append(end)
        for i in range(35):
            root_offset = 0xCF0 + 0x20 * i
            root = process_data(data[root_offset:root_offset + 0x20])
            roots.append(root)
        for i in range(7):
            left_offset = 0x9E8 + 0x28 * i
            left = process_data(data[left_offset:left_offset + 0x20])
            right_offset = 0xB00 + 0x28 * i
            right = process_data(data[right_offset:right_offset + 0x27])
            answer_offset = 0xC18 + 24 * i
            answer_text = process_data(data[answer_offset:answer_offset + 0x20])
            answers.append({"left": left, "right": right, "answer": answer_text})
    elif id_value == 0x05:
        category_data = process_data(data[category_start:category_end])
        roots = []
        answers = []
        for i in range(20):
            root_offset = 0x860 + 0x20 * i
            root = process_data(data[root_offset:root_offset + 0x20])
            roots.append(root)
        for i in range(7):
            title_offset = 0xAE0 + 0x20 * i
            title = process_data(data[title_offset:title_offset + 0x20])
            answer_offset = 0xBC0 + 0x20 * i
            answer_text = process_data(data[answer_offset:answer_offset + 0x20])
            answers.append({"title": title, "answer": answer_text})

    # Create a dictionary for the data
    output_data = {}
    if id_value == 0x01:
        output_data = {
            "id": id_data,
            "type": id_type,
            "category": category_data,
            "question": question_data,
            "answers": {str(i + 1): option for i, option in enumerate(options_data)},
            "true": correct_answer_position
        }
    elif id_value == 0x02:
        output_data = {
            "id": id_data,
            "type": id_type,
            "category": category_data,
            "question": question_data,
            "answers": answers
        }
    elif id_value == 0x03:
        output_data = {
            "id": id_data,
            "type": id_type,
            "category": category_data,
            "question": question_data,
            "answers": answers
        }
    elif id_value == 0x04:
        output_data = {
            "id": id_data,
            "type": id_type,
            "category": category_data,
            "answers": answers,
            "end": {"text": texts, "true": 1},
            "root": roots
        }
    elif id_value == 0x05:
        output_data = {
            "id": id_data,
            "type": id_type,
            "category": category_data,
            "answers": answers,
            "root": roots
        }

    # Export data to JSON file
    if isall:
        json_folder = os.path.join('Output', id_data)
        if not os.path.exists(json_folder):
            os.makedirs(json_folder)
        json_file = os.path.join(json_folder, f'{id_data}.json')
    else:
        # Create a folder for the .glu file
        if not os.path.exists(os.path.splitext(glu_file)[0]):
            os.makedirs(os.path.splitext(glu_file)[0])
        json_file = os.path.join(os.path.splitext(glu_file)[0], f'{os.path.splitext(os.path.basename(glu_file))[0]}.json')
    print(f'Export data to JSON file {id_data}.json...')
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=4)

    print(".json processing is complete")

def process_all_glu_files():
    if not os.path.exists('Output'):
        os.makedirs('Output')

    glu_files = [f for f in os.listdir() if f.lower().endswith('.glu')]
    for glu_file in glu_files:
        if is_glu_file(glu_file):
            process_glu_file_qbd(glu_file, True)
            process_glu_file_vag(glu_file, True)
            process_glu_file_img(glu_file, True)
        else:
            print("Not a valid GLU file")

def process_glu_file_vag(glu_file, isall=None):
    glu_file_name = os.path.basename(glu_file)
    print(f'VAG | Reading the contents of {glu_file_name} file:')
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
        name = data[name_start:name_index].decode('utf-8', errors='ignore')
        vag_names.append(name)
        name_index = data.find(b'.VAG', name_index + 1)

#   OLDCODE
#    while start_index != -1:
#        print(f"Data processing for .vag file {vag_counter}...")
#        end_index = data.find(b'\x56\x41\x47\x70', start_index + 1)
#        if end_index == -1:
#            end_index = len(data)
#        vag_data.append((vag_names[vag_counter - 1], data[start_index:end_index]))
#        start_index = end_index
#
#        # Add end-of-file check condition
#        if start_index >= len(data):
#            break
#
#        vag_counter += 1
        
    while start_index != -1:
        # Find the name offset
        name_offset = start_index + 0x20
        name_length = data.find(b'\x00', name_offset) - name_offset
        name = data[name_offset:name_offset + name_length].decode('utf-8', errors='ignore').rstrip('\x00')
        vag_names.append(name)

        # Find the end of VAG block
        end_index = start_index + int.from_bytes(data[start_index + 0xC:start_index + 0x10], byteorder='big') + 0x10
        vag_data.append((vag_names[vag_counter - 1], data[start_index:end_index]))

        start_index = data.find(b'\x56\x41\x47\x70', end_index)

        vag_counter += 1
    
    # Export to .vag
    print("Exporting data to .vag files...")
    for prefix, vag_block in vag_data:
        if isall:
            folder_name  = os.path.join('Output', os.path.splitext(glu_file)[0])
            if not os.path.exists(folder_name):
                os.makedirs(folder_name )
            vag_filename = os.path.join(folder_name, f'{prefix}.vag')
        else:
            # Create a folder for the .glu file
            folder_name = os.path.splitext(glu_file)[0]
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)
            vag_filename = os.path.join(folder_name, f'{prefix}.vag')
        with open(vag_filename, 'wb') as f:
            f.write(vag_block)

    print(".vag processing is complete")


def process_glu_file_img(glu_file, isall=None):
    glu_file_name = os.path.basename(glu_file)
    print(f'IMG | Reading the contents of {glu_file_name} file:')
    with open(glu_file, 'rb') as f:
        data = f.read()

    img_counter = 1
    img_data = []
    img_names = []

    # Find the start of each IMG block
    start_index = data.find(b'\x49\x4D\x47\x34')
    if start_index == -1:
        print("No data found for .img file")
        return

    # Find .img file names
    name_index = data.find(b'.IMG')
    while name_index != -1:
        name_start = name_index - 8
        name = data[name_start:name_index].replace(b'\x00', b'').decode('utf-8').rstrip('\x00')
        img_names.append(name)
        name_index = data.find(b'.IMG', name_index + 1)

    while start_index != -1:
        print(f"Data processing for .img file {img_counter}...")
        end_index = data.find(b'\x49\x4D\x47\x34', start_index + 1)
        if end_index == -1:
            end_index = len(data)
        img_data.append((img_names[img_counter - 1], data[start_index:end_index]))
        start_index = end_index

        # Add end-of-file check condition
        if start_index >= len(data):
            break

        img_counter += 1
    
    # Export to .img
    print("Exporting data to .img files...")
    for prefix, img_block in img_data:
        if isall:
            folder_name  = os.path.join('Output', os.path.splitext(glu_file)[0])
            if not os.path.exists(folder_name):
                os.makedirs(folder_name )
            img_filename = os.path.join(folder_name, f'{prefix}.IMG')
        else:
            # Create a folder for the .glu file
            folder_name = os.path.splitext(glu_file)[0]
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)
            img_filename = os.path.join(folder_name, f'{prefix}.IMG')
        with open(img_filename, 'wb') as f:
            f.write(img_block)

    print(".img processing is complete")

def is_glu_file(file_path):
    with open(file_path, 'rb') as f:
        first_bytes = f.read(8)
    return b'GLUE' in first_bytes

if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == 'file':
        glu_file = sys.argv[2]
        if is_glu_file(glu_file):
            process_glu_file_qbd(glu_file)
            process_glu_file_vag(glu_file)
            process_glu_file_img(glu_file)
        else:
            print("Not a valid GLU file")
    elif len(sys.argv) == 2 and sys.argv[1] == 'all':
        process_all_glu_files()
    else:
        print("Usage: python glu.py file <filename>")
        print("Usage: python glu.py all (The .glu files must be located in the same place as the produced (.py) file)")
        print("Example: python glu.py file BUA.GLU")