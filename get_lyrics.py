#!/usr/bin/env python3
import sys
import lyricsgenius as lg

genius = lg.Genius('Client_Access_Token_Goes_Here', skip_non_songs=True, excluded_terms=["(Remix)", "(Live)"], remove_section_headers=True)

def get_lyrics(arr, k):
    c = 0
    for name in arr:
        try:
            songs = (genius.search_artist(name, max_songs=k, sort='popularity')).songs
            s = [song.lyrics for song in songs]
            file.write("\n \n   <|endoftext|>   \n \n".join(s))
            c += 1
            print(f"Songs grabbed:{len(s)}")
        except:
            print(f"some exception at {name}: {c}")

if __name__=='__main__':
    if len(sys.argv) < 2:
        print('usage: getLyrics numberOfSongs Artist(s)')
        sys.exit()
    with open('test.lrc', 'w') as file:
        get_lyrics(sys.argv[2:], sys.argv[1])
