#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import argparse
import os
import sys

import core


def main():
    parser = argparse.ArgumentParser(description='A programm to eliminate'\
                                     ' variations in the spelling of artist'\
                                     ' names.')
    parser.add_argument('-s', '--scan-only', action="store_true",
                        default=False, dest='only_scan', help='Only'\
                        'scan the collection for similar artist. Don\'t '\
                        'write to files.')
    parser.add_argument('directory', help='The path to your music collection')
    parser.add_argument('-v', '--verbose', action="store_true",
                        default=False, dest='verbose', help='Verbose mode')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')

    results = parser.parse_args()

    run(results.directory, results.only_scan, results.verbose)


def run(path, only_scan=False, verbose=False):
    if not os.path.isdir(path):
        print 'Please specify a valid directory.'
        sys.exit()

    print 'Reading collection...'
    collection = core.read_collection(path)
    print 'Found {} artists.'.format(len(collection))

    dupes = core.find_similar(collection)
    print 'Found {} (possible) similar artists.\n'.format(len(dupes))

    for dupe in dupes:
        print u'"{}" might be the same. '.format('", "'.join(dupe)),
        if only_scan:
            print
        else:
            print 'What should i do?'

            for index, artist in enumerate(dupe):
                print u'{}: tag everything "{}",'.format(index, artist),
            print 'else: do nothing'

            choice = raw_input('>>> ')
            try:
                choice = int(choice)

                # Tag something
                final_tag = dupe[choice]
                print u'Tagging everything "{}"...'.format(final_tag)

                # TODO Refactor, do a fancy LC
                for artist, files in collection.items():
                    if artist in dupe and artist != final_tag:
                        core.write_files(final_tag, files)
                print
            except ValueError:
                # no number
                pass


if __name__ == '__main__':
    main()
