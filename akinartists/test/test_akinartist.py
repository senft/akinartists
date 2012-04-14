#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import unittest

import akinartist


class AkinArtistTest(unittest.TestCase):

    def testNormalize(self):
        normalize_tests = ((u'Lantlôs', 'Lantlos', 'lantlos'),
                           ('John F. Kennedy', 'john f kennedy', 'John F\
                            Kennedy'),
                           (u'té', u'tè', 'TE'),
                           ('Meanwhile, Back in Communist Russia...',
                            'Meanwhile Back In Communist Russia'))

        for testcase in normalize_tests:
            first = testcase[0]
            for spelling in testcase[1:]:
                self.failUnlessEqual(akinartist.normalize_artist(first),
                                     akinartist.normalize_artist(spelling))

    def testFindSimilar(self):
        pass

if __name__ == '__main__':
    #unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(AkinArtistTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
