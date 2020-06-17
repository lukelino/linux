
""" Pobiera metadane z pliku mp3: odczytuje numer ścieżki i zmienia nazwę pliku wg numeru ścieżki.
    Wykorzystuje mutagen id3. TAG 'TIT2' - tytuł, 'TRCK' - numer ścieżki """

from mutagen.id3 import ID3
import os
import sys
import re

# path = sys.argv[1]      # argument wiersza poleceń -- katalog z utworami
# path = ' '.join(sys.argv[1:])   # Nie trzeba używać ""


def create_numbers(path):
    # ending = input('Rodzaj pliku (mp3, FLAC): ')
    # Wszystkie pliki z katalogu z końcówką mp3
    ending = 'mp3'
    all_files = [files for files in os.listdir(path) if files.endswith(ending)]

    audio_files = []
    # Utworzenie ścieżki dostępu do każdego pliku mp3
    for elem in all_files:
        audio_files.append(os.path.join(path, elem))

    files_metadata_dct = {}

    # Wyszukanie tylko cyfr/liczb początkowych
    pattern = re.compile(r"""^(\d{1,3})""")     # Jedna, dwie, lub trzy cyfry

    # Pobranie numeru ścieżki i utworzenie słownika NUM:TITLE
    strange_symbol_pattern = re.compile(r"""(\*)*""")       # Jeśli w metadata pojawią się znaki '*'
    for f in audio_files:
        audio = ID3(f)
        digit = pattern.search(audio['TRCK'].text[0])       # Dopasowanie wzorca
        if int(digit.group()) in files_metadata_dct.keys():     # Jeśli pojawi się ponownie ten sam numer utworu
            print(f'Nadpisanie utworu {digit.group()}.\nSprawdź poprawność i ilość plików.')
            sys.exit()
        new_audio = strange_symbol_pattern.sub('', audio['TIT2'].text[0])    # Usuń znalezione gwiazdki
        files_metadata_dct.setdefault(int(digit.group()), new_audio)
        # files_metadata_dct[int(digit.group())] = audio['TIT2'].text[0]        # Druga możliwość przypisania

    tmp = []
    # Lista Track_Num, Title
    for k, v in files_metadata_dct.items():
        if int(k) < 10:
            tmp.append('0' + str(k))
            tmp.append(v)
        else:
            tmp.append(str(k))
            tmp.append(v)

    # Utworzenie pełnego tytułu ze składowych listy tmp
    full_title_list = [i + ' ' + j + '.mp3' for i, j in zip(tmp[0::2], tmp[1::2])]

    for i, elem in enumerate(audio_files):
        # print(f'{elem}', ' --> ', f'{path}\\{full_title_list[i]}')
        # os.rename(f'{elem}', f'{path}\\{full_title_list[i]}')     # old, new
        os.rename(elem, os.path.join(path, full_title_list[i]))


