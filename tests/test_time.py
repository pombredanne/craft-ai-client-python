import unittest

from craftai.time import Time

class TestTime(unittest.TestCase):

  def test_timezone_format(self):
    self.assertEqual(Time(timezone='+01:00').timezone, '+01:00')
