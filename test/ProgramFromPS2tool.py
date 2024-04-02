import sys
import os
import wave

class WavFunctions:
    @staticmethod
    def convert_byte_array_to_short_array(PCM_data):
        samples_short = []
        for i in range(0, len(PCM_data), 2):
            sample = PCM_data[i] + (PCM_data[i+1] << 8)
            if sample >= 32768:
                sample -= 65536
            samples_short.append(sample)
        return samples_short

    @staticmethod
    def read_sample_chunk(wave_reader):
        loop_info = [0, 0, 0]
        riff_chunk = next((ec for ec in wave_reader.extra_chunks if ec.identifier_as_string == "smpl"), None)
        if riff_chunk:
            chunk_data = wave_reader.get_chunk_data(riff_chunk)
            midi_note = int.from_bytes(chunk_data[12:16], byteorder='little')
            number_of_samples = int.from_bytes(chunk_data[28:32], byteorder='little')
            offset = 36
            for _ in range(number_of_samples):
                cue_point_id = int.from_bytes(chunk_data[offset:offset+4], byteorder='little')
                type_ = int.from_bytes(chunk_data[offset+4:offset+8], byteorder='little')  # 0 = loop forward, 1 = alternating loop, 2 = reverse
                start = int.from_bytes(chunk_data[offset+8:offset+12], byteorder='little')
                end = int.from_bytes(chunk_data[offset+12:offset+16], byteorder='little')
                fraction = int.from_bytes(chunk_data[offset+16:offset+20], byteorder='little')
                play_count = int.from_bytes(chunk_data[offset+20:offset+24], byteorder='little')
                offset += 24
                loop_info[0] = 1
                loop_info[1] = start
                loop_info[2] = end
        return loop_info

class AiffFileChunksReader:
    class MarkerChunkData:
        pass  # Placeholder for MarkerChunkData, you may define its structure as per your needs

    @staticmethod
    def read_aiff_header(stream, markers):
        # Implement the reading of AIFF header here
        pass  # Placeholder, replace with actual implementation

    def __init__(self, aiff_file):
        pass  # Placeholder for constructor, replace with actual implementation

    def read(self, array, offset, count):
        # Implement the reading of AIFF file here
        pass  # Placeholder, replace with actual implementation

    @property
    def wave_format(self):
        pass  # Placeholder for property, replace with actual implementation

    @property
    def length(self):
        pass  # Placeholder for property, replace with actual implementation

    @property
    def sample_count(self):
        pass  # Placeholder for property, replace with actual implementation

    @property
    def position(self):
        pass  # Placeholder for property, replace with actual implementation

    @position.setter
    def position(self, value):
        pass  # Placeholder for property setter, replace with actual implementation

    def dispose(self, disposing):
        pass  # Placeholder for method, replace with actual implementation

class SonyVag:
    @staticmethod
    def get_loop_offset_for_vag(loop_offset):
        loop_offset_vag = loop_offset // 28 + (2 if loop_offset % 28 != 0 else 1)
        return loop_offset_vag

    @staticmethod
    def vag_file_is_valid(input_file):
        file_is_valid = True
        sample_rate = 0
        vag_data = []

        try:
            with open(input_file, 'rb') as bin_reader:
                magic = bin_reader.read(4).decode('ascii')
                if magic == "VAGp":
                    file_version = int.from_bytes(bin_reader.read(4), byteorder='little')
                    if file_version == 32:
                        bin_reader.seek(16, os.SEEK_SET)
                        sample_rate = int.from_bytes(bin_reader.read(4), byteorder='little')

                        bin_reader.seek(30, os.SEEK_SET)
                        channels = bin_reader.read(1)[0]
                        if channels > 1:
                            file_is_valid = False
                            print("ERROR: This decoder only supports mono files, split channels before using it.")
                        else:
                            bin_reader.seek(48, os.SEEK_SET)
                            total_size = os.fstat(bin_reader.fileno()).st_size - 0x30
                            vag_data = bin_reader.read(total_size)
                    else:
                        file_is_valid = False
                        print("ERROR: The file version is not supported, file version: {} supported version: 32.".format(file_version))
                else:
                    file_is_valid = False
                    print("ERROR: Invalid file type.")
        except Exception as ex:
            file_is_valid = False
            print("ERROR:", ex)

        return file_is_valid, sample_rate, vag_data

    @staticmethod
    def decode_vag(vag_data):
        pcm_data = bytearray()

        hist_1 = 0.0
        hist_2 = 0.0

        with wave.open(vag_data, 'rb') as vag_reader:
            vag_reader.seek(16, os.SEEK_SET)
            while True:
                decoding_coefficient = vag_reader.read(1)[0]
                shift = decoding_coefficient & 0xF
                predict = (decoding_coefficient & 0xF0) >> 4
                flags = vag_reader.read(1)[0]
                sample = vag_reader.read(14)

                if flags == 7:
                    break
                elif flags == 6:
                    sample = pcm_data.tell() // 2
                else:
                    samples = []
                    for i in range(0, len(sample), 2):
                        samples.append(sample[i] & 0xF)
                        samples.append((sample[i] & 0xF0) >> 4)

                    for i in range(0, len(samples), 2):
                        s = samples[i] << 12
                        if s & 0x8000:
                            s = (s | 0xFFFF0000)

                        predict = min(predict, 4)
                        sample = (s >> shift) + hist_1 * VagLutDecoder[predict][0] + hist_2 * VagLutDecoder[predict][1]
                        hist_2 = hist_1
                        hist_1 = sample

                        pcm_data.extend(sample.to_bytes(2, byteorder='little', signed=True))

        return pcm_data

class SonyVagWritter:
    @staticmethod
    def write_vag_file(vag_data, output_file_path, num_of_channels, sampling_frequency):
        try:
            with open(output_file_path, 'wb') as bin_writer:
                bin_writer.write(b'VAGp')
                bin_writer.write((32).to_bytes(4, byteorder='little'))
                bin_writer.write((0).to_bytes(4, byteorder='little'))
                bin_writer.write((len(vag_data) + 16).to_bytes(4, byteorder='little'))
                bin_writer.write(sampling_frequency.to_bytes(4, byteorder='little'))
                bin_writer.write(b'\x00' * 10)
                bin_writer.write((2 if num_of_channels > 1 else 0).to_bytes(1, byteorder='little'))
                bin_writer.write((0).to_bytes(1, byteorder='little'))
                bin_writer.write(os.path.basename(output_file_path).encode('ascii'))
                bin_writer.write(b'\x00' * (16 - len(os.path.basename(output_file_path))))
                bin_writer.write(b'\x00' * 16)
                bin_writer.write(vag_data)
        except Exception as ex:
            print("ERROR:", ex)

def main():
    if len(sys.argv) < 2:
        print("Usage: python ps2_vag_tool.py <InputFile>")
        return

    input_file = sys.argv[1]
    output_file = os.path.splitext(input_file)[0] + ".wav"

    if input_file.endswith(".vag"):
        file_is_valid, sample_rate, vag_data = SonyVag.vag_file_is_valid(input_file)
        if file_is_valid:
            pcm_data = SonyVag.decode_vag(vag_data)
            SonyVagWritter.write_vag_file(pcm_data, output_file, 1, sample_rate)
            print("Conversion completed successfully.")
        else:
            print("Invalid VAG file.")

if __name__ == "__main__":
    main()
