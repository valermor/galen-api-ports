import unittest
import mock
from galenpy.galen_webdriver import ThriftRemoteConnection


class TestGalenWebDriver(unittest.TestCase):


    @mock.patch('galenapi.thrift_client.ThriftFacade')
    def test_execute_unrecognized_command_throw_webdriver_exception(self, mock_thrift_facade):
        mocked_thrift_client = mock_thrift_facade.return_value
        remote_connection = ThriftRemoteConnection("127.0.0.1", mocked_thrift_client)

        self.assertRaises(KeyError, remote_connection.execute("non existing command", "some params"))
