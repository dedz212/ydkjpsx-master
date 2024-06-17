This project provides tools to extract content from YDKJ [Playstation] game files, including Q&A data and audio files. The extracted content is exported in .json files for easy access and manipulation.

# GLUEX
<table>
  <tr>
    <td>
      The GLUEX program provides a graphical user interface for data viewing and export. Simply run the program and use the intuitive interface to drag and drop files, set export paths, and play audio files.
    </td>
    <td>
      <img src="https://github.com/dedz212/ydkjpsx-master/assets/75216495/422289f0-2917-4463-a868-8521a3a52b8b" alt="GLUEX logo" width="300"/>
    </td>
  </tr>
</table>

<table style="width: 100%;">
  <tr>
    <td style="width: 33%;">
      Drag & Drop
    </td>
    <td style="width: 33%;">
      .GLU viewer
    </td>
    <td style="width: 33%;">
      Listen in the app
    </td>
  </tr>
  <tr>
    <td style="width: 33%;">
      Move it or click "View" button and then select .glu file
    </td>
    <td style="width: 33%;">
      If it contains Q&A data, you can view the entire contents
    </td>
    <td style="width: 33%;">
      Open the "List" and listen to an audio in the app
    </td>
  </tr>
  <tr>
    <td style="width: 33%;">
      <img src="https://github.com/dedz212/ydkjpsx-master/assets/75216495/c706969e-bd58-45bf-a604-9297bd63dce2" alt="Drag & Drop" width="100%"/>
    </td>
    <td style="width: 33%;">
      <img src="https://github.com/dedz212/ydkjpsx-master/assets/75216495/0531c59f-0a19-4521-a773-ef2f344b6ff9" alt="GLU file" width="100%"/>
    </td>
    <td style="width: 33%;">
      <img src="https://github.com/dedz212/ydkjpsx-master/assets/75216495/7b1e63d3-5130-42b3-b7b2-9ce4fd0c6d85" alt="GLU list" width="100%"/>
    </td>
  </tr>
  <tr>
    <td style="width: 33%;">
      Settings
    </td>
    <td style="width: 33%;">
      View all
    </td>
    <td style="width: 33%;">
      Remove all
    </td>
  </tr>
  <tr>
    <td style="width: 33%;">
      Do you want to change the export path for the data or the audio format? Then this is for you!
    </td>
    <td style="width: 33%;">
      Are you tired of clicking "View" and selecting a .glu file every time? Click "View all" and choose a folder with the contents.
    </td>
    <td style="width: 33%;">
      Tired of clicking the x button every time? Just click "Remove All" to clear all content.
    </td>
  </tr>
  <tr>
    <td style="width: 33%;">
      <img src="https://github.com/dedz212/ydkjpsx-master/assets/75216495/882b49b8-8bab-424e-b060-ac824e943d13" alt="Settings" width="100%"/>
    </td>
    <td style="width: 33%;">
      <img src="https://github.com/dedz212/ydkjpsx-master/assets/75216495/3844b192-aa63-494c-9dbc-8885fc8e33d6" alt="Remove all" width="100%"/>
    </td>
    <td style="width: 33%;">
      <img src="https://github.com/dedz212/ydkjpsx-master/assets/75216495/f6662040-7cd9-49e3-96e1-09281b539365" alt="View all" width="100%"/>
    </td>
  </tr>
</table>


# Python
- Place the extractor script in the same directory as the .glu files you wish to export. Running the script will export all the files in the current directory.
- .vag files are audio files. To open them, use the [VAGEDIT](https://archive.org/download/Sony-PSX-tools/VAGEDIT.zip) program.
- To extract the game itself, you need a .bin file of the game and the [jPSXdec](https://github.com/m35/jpsxdec/releases/tag/v2.0) program.

## .glu
This script is a tool for extracting and processing data from .glu files used in games to store various types of content such as questions (QBD), audio (VAG), and images (IMG).

### Content
#### QBD
This code block is designed to extract structured data from QBD (Question Block Data) blocks within .glu files. QBD blocks contain information about questions and answers for different question types.
The question type is determined by reading the value at offset 0x808 (id_value).

Depending on the id_value, the question type is identified as either "Simple Question", "DisOrDat", "Wendithap'n", "Coinkydink", or "Jack Attack".
Each question type has different offsets and data structure:
* **Simple Question**: Category, question, answer options, and correct answer.
* **DisOrDat**: Category, question, two answer options with their corresponding matches.
* **Wendithap'n**: Category, question, seven answer options with their corresponding matches.
* **Coinkydink**: Category, texts, roots, and answers.
* **Jack Attack**: Category, roots, and answers.
A JSON file is created with the name corresponding to the question ID, where a structured dictionary of data is stored.

#### VAG
This code block is designed to extract and save audio data in VAG format from .glu files. It searches for VAG blocks using the signature 0x56\x41\x47\x70. It finds the names of VAG files within the .glu file using a .VAG signature search. Each found VAG block is read and saved into a corresponding .vag file.

#### IMG
This code block is designed to extract and save graphic data in IMG format from .glu files. It determines the starting index to search for the beginning of IMG blocks using the signature 0x49\x4D\x47\x34. It finds the names of IMG files within the .glu file using a .IMG signature search. Each found IMG block is read and saved into a corresponding .img file.

### Usage
The project supports two usage modes via the command line:
* Processes a specific .glu file.
```
python glu.py file <filename>
```
*  Processes all .glu files in the current directory.
```
python glu.py all
```

## .inf
The script extracts and analyzes data from .inf files used to store information about question types and category names.
* **Map ID (mape_id)**: Unique identifier of the content.
* **Data containers**: Extracts up to 15 data containers, each containing:
* * **content_id**: Identifier of the content.
* * **category_data**: Category of the data.
* * **type_data**: Type of data, which can be one of the predefined values (Simple Question, DisOrDat, Wendithap'n, Coinkydink, Jack Attack).
```
python inf.py file HTE.INF
```

## vagtowav
The script is a utility for decoding VAG format files (PS2 audio format) into WAV format. VAG files are commonly used for storing sound effects and music in PlayStation games.
### Основные функции
#### vag_file_is_valid
* **File Magic and Version**: Checks the file header and its version.
* **Sampling Rate and Channels**: Extracts the sampling rate and number of channels (only supports mono).
* **Track Name**: Extracts the track name from the file header.

#### decode_vag
Decodes data from a VAG file into PCM (Pulse-code modulation) format and saves the result to a WAV file:
* **Data Decoding**: Unpacks data using coefficients and predictive values specified in the VAG header.
* **Creating WAV File**: Writes the decoded data to a WAV file with the specified sampling rate and mono channel.

### Additional Functions and Constants
* **VagLutDecoder**: Decoding table used to unpack data from VAG format into PCM.
* **VAGFlag**: Class of flags used to indicate various operations during VAG data decoding.
* **Loop offset**: Helper function to compute loop offset in VAG format.

### Usage
The project supports two usage modes via the command line:
* Processes a specific .vag file.
```
python vagtowav.py file <filename>
```
*  Processes all .vag files in the current directory.
```
python vagtowav.py all
```

## .94
This code serves as a tool for processing .94 files used in PlayStation games (PS-X EXE). It includes functions for extracting information from such files, specifically extracting PS-X EXE data (program code), images (IMG), and audio (VAG).
Extracts key parameters from a PS-X EXE file (.94) data in JSON format:
* **Magic Number**: Unique file identifier.
* **Region Specific**: Region-specific information.
* **Initial PC, GP, etc.**: Initial addresses and sizes for various code and data segments.
```
python 94.py file SLUS_011.94
```

## .cnf
This Python script is designed to process files with the .cnf extension, extracting specific data based on given offsets and saving it in JSON format. It reads the contents of the specified file, extracts information about system boot, version, TCB parameters, EVENT, and STACK, then creates a JSON file with a corresponding name containing structured data.
```
python cnf.py file SYSTEM.CNF
```