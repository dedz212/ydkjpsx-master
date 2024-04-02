import os
import sys
import struct

f = [[0.0, 0.0],
     [60.0 / 64.0, 0.0],
     [115.0 / 64.0, -52.0 / 64.0],
     [98.0 / 64.0, -55.0 / 64.0],
     [122.0 / 64.0, -60.0 / 64.0]]

samples = [0] * 28

class WaveHeader:
    def __init__(self):
        self.chunkId = b'RIFF'
        self.chunkSize = 0
        self.format = b'WAVE'
        self.subchunk1Id = b'fmt '
        self.subchunk1Size = 16
        self.audioFormat = 1
        self.numChannels = 1
        self.sampleRate = 44100
        self.byteRate = self.sampleRate * self.numChannels * 16 // 8
        self.blockAlign = self.numChannels * 16 // 8
        self.bitsPerSample = 16
        self.subchunk2Id = b'data'
        self.subchunk2Size = 0

def convert_vag_to_wav(vag_filename):
    pcm_filename = vag_filename.replace('.vag', '.PCM')
    wav_filename = vag_filename.replace('.vag', '.WAV')

    try:
        vag = open(vag_filename, "rb")
        pcm = open(pcm_filename, "wb")
    except IOError:
        print("Error: Cannot open input/output file")
        return -8
    
    vag.seek(64)

    while True:
        predict_nr = ord(vag.read(1))
        shift_factor = predict_nr & 0xf
        predict_nr >>= 4
        flags = ord(vag.read(1))
        if flags == 1 or flags == -1:
            break
        for i in range(0, 28, 2):
            d = ord(vag.read(1))
            s = (d & 0xf) << 12
            if s & 0x8000:
                s |= 0xffff0000
            samples[i] = s >> shift_factor
            s = (d & 0xf0) << 8
            if s & 0x8000:
                s |= 0xffff0000
            samples[i + 1] = s >> shift_factor
        s_1 = s_2 = 0.0
        for i in range(28):
            samples[i] += s_1 * f[predict_nr][0] + s_2 * f[predict_nr][1]
            s_2 = s_1
            s_1 = samples[i]
            d = int(samples[i] + 0.5)
            pcm.write(struct.pack('<l', d))

    pcm.close()
    vag.close()

    try:
        pcm = open(pcm_filename, "rb")
        wav = open(wav_filename, "wb")
    except IOError:
        print("Error: Cannot open PCM/WAV file")
        return -8

    pcm.seek(0, 2)
    filesize = pcm.tell()
    pcm.seek(0)

    header = WaveHeader()
    header.chunkSize = filesize + 36
    header.subchunk2Size = filesize

    wav.write(struct.pack('<4sI4s4sIHHIIHH4sI', header.chunkId, header.chunkSize, header.format, header.subchunk1Id,
                          header.subchunk1Size, header.audioFormat, header.numChannels, header.sampleRate,
                          header.byteRate, header.blockAlign, header.bitsPerSample, header.subchunk2Id,
                          header.subchunk2Size))

    buffer_size = 1024
    buffer = pcm.read(buffer_size)
    while buffer:
        wav.write(buffer)
        buffer = pcm.read(buffer_size)

    pcm.close()
    wav.close()

def main():
    if len(sys.argv) == 3 and sys.argv[1] == 'file':
        convert_vag_to_wav(sys.argv[2])
    elif len(sys.argv) == 2 and sys.argv[1] == 'all':
        for file in os.listdir("."):
            if file.endswith(".vag"):
                convert_vag_to_wav(file)
    else:
        print("Usage:")
        print("  python vagtowav.py file <vag_filename>")
        print("  python vagtowav.py all")

if __name__ == "__main__":
    main()
