import os
import unittest
from unittest.mock import patch, MagicMock

from sapirai.faas.torch import Action, InferenceAdapter, InferenceManager


class TestInferenceAdapter(unittest.TestCase):
    def setUp(self):
        self.manager_mock = MagicMock(spec=InferenceManager)

    @patch('sapirai.faas.torch.adapter.argparse.ArgumentParser.parse_args')
    @patch('sapirai.faas.torch.adapter.argparse.ArgumentParser.parse_known_args')
    @patch('sapirai.faas.torch.adapter.load')
    @patch('sapirai.faas.torch.adapter.HTTPServer')
    def test_run_action(self, mock_http_server, mock_load, mock_parse_known_args, mock_parse_args):
        mock_args = MagicMock()
        mock_args.action = Action.Run
        mock_args.log_level = 'DEBUG'
        mock_parse_known_args.return_value = (mock_args, [])

        mock_args = MagicMock()
        mock_args.port = 8080
        mock_parse_args.return_value = mock_args

        adapter = InferenceAdapter(self.manager_mock)
        adapter.start()

        mock_http_server.assert_called_once()


if __name__ == '__main__':
    unittest.main()
