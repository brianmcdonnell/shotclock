import unittest

from fileformats.mov import MOVFile


class TestMovFile(unittest.TestCase):

    def test_parse(self):
        f = MOVFile('test.mpg')
        dt = f.creation_date
        print dt
        self.assertEqual(0, 0)
