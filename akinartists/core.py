#!/usr/bin/env python2
# -*- coding: utf-8 -*-


from collections import defaultdict
import logging
import mutagen
from mutagen.easyid3 import EasyID3
import os
import string

# TODO: delete leading 'the's so that 'The Beatles' == 'Beatles'


# Valid extensions (based on mutagens abilities)
extensions = ['.mp3', '.ogg']

# Determines how the artist names become normalized:
# ( <characters_to_replace>, <character_to_replace_with> )
#
# This does:
#   - replace all 'é', 'è', 'ê' and 'ẽ' with a simple e
#   - replace all 'á', 'à', 'â' and 'ã' with a simple a
#   - replace all 'ô' and 'õ' with a simple o
#   - delete all special characters
normalization = ((u'éèêẽ', u'e'),
                 (u'áàâã', u'a'),
                 (u'óòôõ', u'o'),
                 (string.punctuation, u''))

# Init logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)


def read_collection(path):
    """ Reads the collection at the given path in a dict:
        {artist: [path_to_file1, path_to_file2, ..], ..}. """
    collection = defaultdict(list)

    for (dirpath, _, filenames) in os.walk(path):
        for file in filenames:
            if os.path.splitext(file)[1] in extensions:
                fullpath = os.path.join(dirpath, file)
                try:
                    track = EasyID3(fullpath)
                    if 'artist' in track:
                        # File has an artist-tag
                        artist = track['artist'][0]

                        if artist not in collection:
                            # Artist has not been added before
                            logger.debug('Added artist %s' % artist)

                        collection[artist].append(fullpath)

                except mutagen.id3.ID3NoHeaderError:
                    logger.debug('No ID3 tag found in %s' % fullpath)
    return collection


def find_similar(collection):
    """ Searches the collection for (probably) similar artist and returns
        lists containing the "candidates". """

    spellings = defaultdict(list)
    for artist in collection:
        spellings[normalize_artist(artist)].append(artist)

    return [spellings[artist] for artist in spellings
            if len(spellings[artist]) > 1]


def normalize_artist(artist):
    """ Normalizes an artist name. """
    artist = artist.lower()
    for (replace_what, replace_with) in normalization:
        for char in replace_what:
            artist = artist.replace(char, replace_with)

    # Remove possible multiple whitespaces that came up when deleting special
    # characters (e.g. 'a + b' -> 'a  b')
    if '  ' in artist:
        artist = ' '.join(artist.split())
    return artist


def write_files(artist, files):
    """ Writes the given artist in all the given files' ID3 tag. """
    for file in files:
        print 'Writing to {}...'.format(file),

        track = EasyID3(file)
        track['artist'] = artist
        track.save()

        print 'Finished'
