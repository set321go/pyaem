from mock import MagicMock
import pyaem
import unittest

class TestPyAemException(unittest.TestCase):


  def test_init(self):

    exception = pyaem.PyAemException(123, 'somemessage')
    self.assertEqual(exception.code, 123)
    self.assertEqual(exception.message, 'somemessage')


if __name__ == '__main__':
  unittest.main()