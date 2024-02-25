Information und Quellen zur Verwendung des MIDI-Konverters und Erklärung zum Sf2-Plugin

Um das Programm zu starten, muss die Datei "midiConUI.py" gestartet werden. 
Es öffnet sich dann eine grafische Nutzeroberfläche.

Zur Konvertierung der MIDI-Dateien haben wir das Plugin sf2-loader verwendet, welches aufgrund seiner Größe im .gitignore inkludiert werden musste. Unter folgendem Link finden Sie eine Beschreibung des Projekts.
https://pypi.org/project/sf2-loader/

Es kann unter folgendem Link heruntergeladen werden. Die .zip-Datei sollte im Projektordner extrahiert werden.
https://github.com/Rainbow-Dreamer/musicpy/releases/download/6.89/ffmpeg.zip

Damit das SF2-Loader Plugin ffmpeg vom MIDI-Konverter berücksichtigt wird, muss der Pfad des Plugins zu den Environment-Variable einmalig hinzugefügt werden. 

Dies wird durch die folgenden Zeilen in der midiConUI.py bewerkstelligt: (Zeile 8 + 9)
import os
os.environ["PATH"] += "/ffmpeg/bin"

Da die sf2 Soundfont-Datei ebenfalls zu groß für das Repository ist, mussten wir sie zum .gitignore hinzufügen. 
Die folgende Soundfont-Datei haben wir unter folgendem Link heruntergeladen:

https://ftp.osuosl.org/pub/musescore/soundfont/MuseScore_General/MuseScore_General.sf2

MuseScore 2 (SF2 version (208 MB))
Lizenz: freigegeben unter der MIT license