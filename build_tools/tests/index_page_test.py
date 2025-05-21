from pathlib import Path
import os
import unittest
import sys

class IndexPageTest(unittest.TestCase):
    def setUp(self):
        # setup a directory
        # setup a tar.xz files
        # setup fake tar.xz sha256 sum files
        # get the indexer.py file to directory
        pass

    def tearDown(self):
        # remove the directory
        pass

    def testIndexer(self):
        # test the indexer.py file with our .tar.xz
        # checkout index.html, make sure we have X a hrefs
        # make sure our .tar.xz files are there with proper count
        pass
    
    def testRetrieveS3Artifacts(self):
        # mock url open, return html from index.html
        # check to make sure we get proper data
        # also run edge cases of 404 or exception
        pass


if __name__ == "__main__":
    unittest.main()
