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

