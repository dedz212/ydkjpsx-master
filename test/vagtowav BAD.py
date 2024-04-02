import sys
import os
import struct
import wave

VAG_SAMPLE_BYTES = 14
VAG_SAMPLE_NIBBL = VAG_SAMPLE_BYTES * 2

VagLutDecoder = [
    [0.0, 0.0],
    [60.0 / 64.0, 0.0],
    [115.0 / 64.0, -52.0 / 64.0],
    [98.0 / 64.0, -55.0 / 64.0],
    [122.0 / 64.0, -60.0 / 64.0]
]

class VAGFlag:
    VAGF_NOTHING = 0
    VAGF_LOOP_LAST_BLOCK = 1
    VAGF_LOOP_REGION = 2
    VAGF_LOOP_END = 3
    VAGF_LOOP_FIRST_BLOCK = 4
    VAGF_UNK = 5
    VAGF_LOOP_START = 6
    VAGF_PLAYBACK_END = 7

def get_loop_offset_for_vag(loop_offset):
    loop_offset_vag = loop_offset // 28 + (2 if loop_offset % 28 != 0 else 1)
    return loop_offset_vag

def vag_file_is_valid(input_file):
    try:
        with open(input_file, 'rb') as file:
            magic = file.read(4).decode('ascii')
            if magic != "VAGp":
                print("ERROR: Invalid file type.")
                return False, 0, bytearray(), ""

            file_version = struct.unpack('>i', file.read(4))[0]
            if file_version != 32:
                print("ERROR: The file version is not supported, file version:", file_version, "supported version: 32.")
                return False, 0, bytearray(), ""

            file.seek(16)
            sample_rate = struct.unpack('>i', file.read(4))[0]

            file.seek(30)
            channels = struct.unpack('B', file.read(1))[0]
            if channels > 1:
                print("ERROR: This decoder only supports mono files, split channels before using it.")
                return False, 0, bytearray(), ""

            file.seek(32)
            track_name = file.read(16).decode('ascii').rstrip('\x00')

            file.seek(48, os.SEEK_SET)
            vag_data = file.read()
            return True, sample_rate, vag_data, track_name

    except FileNotFoundError:
        print("ERROR: File not found.")
        return False, 0, bytearray(), ""

def decode_vag(vag_data, track_name):
    pcm_data = bytearray()
    hist_1 = 0.0
    hist_2 = 0.0

    pos = 0x30  # Skip VAG header

    while pos < len(vag_data):
        decoding_coefficient = struct.unpack('B', vag_data[pos:pos+1])[0]
        pos += 1
        flags = struct.unpack('B', vag_data[pos:pos+1])[0]
        pos += 1

        sample = vag_data[pos:pos+VAG_SAMPLE_BYTES]
        pos += VAG_SAMPLE_BYTES

        shift = decoding_coefficient & 0xF
        predict = (decoding_coefficient & 0xF0) >> 4

        if flags == VAGFlag.VAGF_PLAYBACK_END:
            break
        elif flags == VAGFlag.VAGF_LOOP_START:
            pass
        else:
            samples = [0] * VAG_SAMPLE_NIBBL

            for j in range(VAG_SAMPLE_BYTES):
                samples[j * 2] = sample[j] & 0xF
                samples[j * 2 + 1] = (sample[j] & 0xF0) >> 4

            for j in range(VAG_SAMPLE_NIBBL):
                s = samples[j] << 12
                if s & 0x8000 != 0:
                    s |= 0xFFFF0000

                predict = min(predict, len(VagLutDecoder) - 1)
                sample = (s >> shift) + hist_1 * VagLutDecoder[predict][0] + hist_2 * VagLutDecoder[predict][1]
                hist_2 = hist_1
                hist_1 = sample

                pcm_data.extend(struct.pack('<h', max(-32768, min(32767, round(sample)))))

    output_filename = f"{track_name}.wav"
    with wave.open(output_filename, 'wb') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(pcm_data)

    print(f"File {output_filename} created.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python vagtowav.py <file/all> <input>")
        sys.exit(1)

    if sys.argv[1] == "all":
        current_dir = os.path.dirname(os.path.realpath(__file__))
        for filename in os.listdir(current_dir):
            if filename.endswith(".vag"):
                input_file = os.path.join(current_dir, filename)
                is_valid, sample_rate, vag_data, track_name = vag_file_is_valid(input_file)
                if is_valid:
                    decode_vag(vag_data, track_name)
    else:
        input_file = sys.argv[2]
        is_valid, sample_rate, vag_data, track_name = vag_file_is_valid(input_file)
        if is_valid:
            decode_vag(vag_data, track_name)
