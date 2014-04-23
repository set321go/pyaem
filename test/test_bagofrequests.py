from mock import MagicMock
import pyaem
import pycurl
import unittest

class TestBagOfRequests(unittest.TestCase):


    def test_request_post(self):

        def _handler_dummy(response, **kwargs):

            result = {
                'status' : 'success',
                'message': 'some dummy message'
            }

            return result

        curl         = pycurl.Curl()
        curl.setopt  = MagicMock()
        curl.perform = MagicMock()
        curl.getinfo = MagicMock(return_value = 200)
        curl.close   = MagicMock()
        pycurl.Curl  = MagicMock(return_value = curl)

        method   = 'post'
        url      = 'http://localhost:4502/.cqactions.html'
        params   = { 'foo1': 'bar1', 'foo2': 'bar2' }
        handlers = { 200: _handler_dummy }

        result = pyaem.bagofrequests.request(method, url, params, handlers)

        curl.setopt.assert_any_call(pycurl.POST, 1)
        curl.setopt.assert_any_call(pycurl.POSTFIELDS, 'foo1=bar1&foo2=bar2')
        curl.setopt.assert_any_call(pycurl.URL, 'http://localhost:4502/.cqactions.html')
        curl.setopt.assert_any_call(pycurl.FOLLOWLOCATION, 1)

        # 5 calls including the one with pycurl.WRITEFUNCTION
        self.assertEqual(curl.setopt.call_count, 5)

        curl.perform.assert_called_once_with()
        curl.getinfo.assert_called_once_with(pycurl.HTTP_CODE)
        curl.close.assert_called_once_with()

        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['message'], 'some dummy message')


    def test_request_get(self):

        def _handler_dummy(response, **kwargs):

            result = {
                'status' : 'success',
                'message': 'some dummy message'
            }

            return result

        curl         = pycurl.Curl()
        curl.setopt  = MagicMock()
        curl.perform = MagicMock()
        curl.getinfo = MagicMock(return_value = 200)
        curl.close   = MagicMock()
        pycurl.Curl  = MagicMock(return_value = curl)

        method   = 'gett'
        url      = 'http://localhost:4502/.cqactions.html'
        params   = { 'foo1': 'bar1', 'foo2': 'bar2' }
        handlers = { 200: _handler_dummy }

        result = pyaem.bagofrequests.request(method, url, params, handlers)

        curl.setopt.assert_any_call(pycurl.URL, 'http://localhost:4502/.cqactions.html?foo1=bar1&foo2=bar2')
        curl.setopt.assert_any_call(pycurl.FOLLOWLOCATION, 1)

        # 3 calls including the one with pycurl.WRITEFUNCTION
        self.assertEqual(curl.setopt.call_count, 3)

        curl.perform.assert_called_once_with()
        curl.getinfo.assert_called_once_with(pycurl.HTTP_CODE)
        curl.close.assert_called_once_with()

        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['message'], 'some dummy message')


    def test_request_unexpected(self):

        curl         = pycurl.Curl()
        curl.setopt  = MagicMock()
        curl.perform = MagicMock()
        curl.getinfo = MagicMock(return_value = 500)
        curl.close   = MagicMock()
        pycurl.Curl  = MagicMock(return_value = curl)

        method   = 'gett'
        url      = 'http://localhost:4502/.cqactions.html'
        params   = { 'foo1': 'bar1', 'foo2': 'bar2' }
        handlers = {}

        try:
                pyaem.bagofrequests.request(method, url, params, handlers)
                self.fail('An exception should have been raised')
        except pyaem.PyAemException, e:
                self.assertEqual(e.code, 500)
                self.assertEqual(e.message, 'Unexpected response\nhttp code: 500\nbody:\n')

        curl.setopt.assert_any_call(pycurl.URL, 'http://localhost:4502/.cqactions.html?foo1=bar1&foo2=bar2')
        curl.setopt.assert_any_call(pycurl.FOLLOWLOCATION, 1)

        # 3 calls including the one with pycurl.WRITEFUNCTION
        self.assertEqual(curl.setopt.call_count, 3)

        curl.perform.assert_called_once_with()
        curl.getinfo.assert_called_once_with(pycurl.HTTP_CODE)
        curl.close.assert_called_once_with()


    def test_download_file(self):

        def _handler_dummy(response, **kwargs):

            result = {
                'status' : 'success',
                'message': 'some dummy message'
            }

            return result

        curl         = pycurl.Curl()
        curl.setopt  = MagicMock()
        curl.perform = MagicMock()
        curl.getinfo = MagicMock(return_value = 200)
        curl.close   = MagicMock()
        pycurl.Curl  = MagicMock(return_value = curl)

        url      = 'http://localhost:4502/.cqactions.html'
        params   = { 'foo1': 'bar1', 'foo2': 'bar2' }
        handlers = { 200: _handler_dummy }

        result = pyaem.bagofrequests.download_file(url, params, handlers, file = '/tmp/somefile')

        curl.setopt.assert_any_call(pycurl.URL, 'http://localhost:4502/.cqactions.html?foo1=bar1&foo2=bar2')
        curl.setopt.assert_any_call(pycurl.FOLLOWLOCATION, 1)

        # 4 calls including the one with pycurl.WRITEDATA and pycurl.WRITEFUNCTION
        self.assertEqual(curl.setopt.call_count, 4)

        curl.perform.assert_called_once_with()
        curl.getinfo.assert_called_once_with(pycurl.HTTP_CODE)
        curl.close.assert_called_once_with()

        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['message'], 'some dummy message')


    def test_download_file_unexpected(self):

        curl         = pycurl.Curl()
        curl.setopt  = MagicMock()
        curl.perform = MagicMock()
        curl.getinfo = MagicMock(return_value = 500)
        curl.close   = MagicMock()
        pycurl.Curl  = MagicMock(return_value = curl)

        url      = 'http://localhost:4502/.cqactions.html'
        params   = { 'foo1': 'bar1', 'foo2': 'bar2' }
        handlers = {}

        try:
                pyaem.bagofrequests.download_file(url, params, handlers, file = '/tmp/somefile')
                self.fail('An exception should have been raised')
        except pyaem.PyAemException, e:
                self.assertEqual(e.code, 500)
                self.assertEqual(e.message, 'Unexpected response\nhttp code: 500\nbody:\n')

        curl.setopt.assert_any_call(pycurl.URL, 'http://localhost:4502/.cqactions.html?foo1=bar1&foo2=bar2')
        curl.setopt.assert_any_call(pycurl.FOLLOWLOCATION, 1)

        # 4 calls including the one with pycurl.WRITEDATA and pycurl.WRITEFUNCTION
        self.assertEqual(curl.setopt.call_count, 4)

        curl.perform.assert_called_once_with()
        curl.getinfo.assert_called_once_with(pycurl.HTTP_CODE)
        curl.close.assert_called_once_with()


    def test_upload_file(self):

        def _handler_dummy(response, **kwargs):

            result = {
                'status' : 'success',
                'message': 'some dummy message'
            }

            return result

        curl         = pycurl.Curl()
        curl.setopt  = MagicMock()
        curl.perform = MagicMock()
        curl.getinfo = MagicMock(return_value = 200)
        curl.close   = MagicMock()
        pycurl.Curl  = MagicMock(return_value = curl)

        url      = 'http://localhost:4502/.cqactions.html'
        params   = { 'foo1': 'bar1', 'foo2': 'bar2' }
        handlers = { 200: _handler_dummy }

        result = pyaem.bagofrequests.upload_file(url, params, handlers, file = '/tmp/somefile')

        curl.setopt.assert_any_call(pycurl.POST, 1)
        curl.setopt.assert_any_call(pycurl.HTTPPOST, [('foo1', 'bar1'), ('foo2', 'bar2')])
        curl.setopt.assert_any_call(pycurl.URL, 'http://localhost:4502/.cqactions.html')
        curl.setopt.assert_any_call(pycurl.FOLLOWLOCATION, 1)

        # 5 calls including the one with pycurl.WRITEFUNCTION
        self.assertEqual(curl.setopt.call_count, 5)

        curl.perform.assert_called_once_with()
        curl.getinfo.assert_called_once_with(pycurl.HTTP_CODE)
        curl.close.assert_called_once_with()

        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['message'], 'some dummy message')


    def test_upload_file_unexpected(self):

        curl         = pycurl.Curl()
        curl.setopt  = MagicMock()
        curl.perform = MagicMock()
        curl.getinfo = MagicMock(return_value = 500)
        curl.close   = MagicMock()
        pycurl.Curl  = MagicMock(return_value = curl)

        url      = 'http://localhost:4502/.cqactions.html'
        params   = { 'foo1': 'bar1', 'foo2': 'bar2' }
        handlers = {}

        try:
                pyaem.bagofrequests.upload_file(url, params, handlers, file = '/tmp/somefile')
                self.fail('An exception should have been raised')
        except pyaem.PyAemException, e:
                self.assertEqual(e.code, 500)
                self.assertEqual(e.message, 'Unexpected response\nhttp code: 500\nbody:\n')

        curl.setopt.assert_any_call(pycurl.POST, 1)
        curl.setopt.assert_any_call(pycurl.HTTPPOST, [('foo1', 'bar1'), ('foo2', 'bar2')])
        curl.setopt.assert_any_call(pycurl.URL, 'http://localhost:4502/.cqactions.html')
        curl.setopt.assert_any_call(pycurl.FOLLOWLOCATION, 1)

        # 5 calls including the one with pycurl.WRITEFUNCTION
        self.assertEqual(curl.setopt.call_count, 5)

        curl.perform.assert_called_once_with()
        curl.getinfo.assert_called_once_with(pycurl.HTTP_CODE)
        curl.close.assert_called_once_with()


if __name__ == '__main__':
    unittest.main()
    