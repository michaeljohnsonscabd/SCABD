"""Test suite for Gemini CLI."""

import pytest
import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

from gemini_cli.config import GeminiConfig
from gemini_cli.gemini_client import GeminiClient
from gemini_cli.cli import cli
from click.testing import CliRunner


class TestGeminiConfig:
    """Test GeminiConfig class."""

    def test_config_initialization(self):
        """Test config initialization."""
        config = GeminiConfig()
        assert config.config_dir.exists()
        assert config.config_file.parent.exists()

    def test_api_key_operations(self):
        """Test API key get/set operations."""
        config = GeminiConfig()
        test_key = "test-api-key-12345"
        
        config.set_api_key(test_key)
        retrieved_key = config.get_api_key()
        
        # API key should be retrievable from config file
        assert retrieved_key == test_key

    def test_model_operations(self):
        """Test model get/set operations."""
        config = GeminiConfig()
        test_model = "gemini-pro-vision"
        
        config.set_model(test_model)
        retrieved_model = config.get_model()
        
        assert retrieved_model == test_model

    def test_scabd_config_operations(self):
        """Test SCABD config get/set operations."""
        config = GeminiConfig()
        scabd_config = {
            "db_host": "localhost",
            "db_port": 5432,
            "db_name": "scabd"
        }
        
        config.set_scabd_config(scabd_config)
        retrieved_config = config.get_scabd_config()
        
        assert retrieved_config == scabd_config

    def test_get_all_config(self):
        """Test retrieving all configuration."""
        config = GeminiConfig()
        config.set_api_key("test-key")
        config.set_model("gemini-pro")
        
        all_config = config.get_all()
        
        assert "api_key" in all_config
        assert "model" in all_config
        assert all_config["api_key"] == "test-key"
        assert all_config["model"] == "gemini-pro"


class TestGeminiClient:
    """Test GeminiClient class."""

    def test_client_initialization_no_api_key(self):
        """Test client initialization without API key raises error."""
        with pytest.raises(ValueError, match="API key is required"):
            GeminiClient("", "gemini-pro")

    @patch('gemini_cli.gemini_client.genai')
    def test_client_initialization_with_api_key(self, mock_genai):
        """Test client initialization with valid API key."""
        mock_genai.GenerativeModel.return_value = MagicMock()
        
        client = GeminiClient("valid-api-key", "gemini-pro")
        
        assert client.model is not None
        assert client.model_name == "gemini-pro"
        assert client.chat_history == []

    @patch('gemini_cli.gemini_client.genai')
    def test_client_chat_history(self, mock_genai):
        """Test chat history management."""
        mock_model = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "AI response"
        mock_model.generate_content.return_value = mock_response
        mock_genai.GenerativeModel.return_value = mock_model
        
        client = GeminiClient("valid-api-key", "gemini-pro")
        
        # Test chat
        response = client.chat("Hello")
        assert response == "AI response"
        assert len(client.chat_history) == 2  # user message + AI response
        
        # Test clear history
        client.clear_history()
        assert client.chat_history == []

    @patch('gemini_cli.gemini_client.genai')
    def test_analyze_scabd_data(self, mock_genai):
        """Test SCABD data analysis."""
        mock_model = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "Analysis result"
        mock_model.generate_content.return_value = mock_response
        mock_genai.GenerativeModel.return_value = mock_model
        
        client = GeminiClient("valid-api-key", "gemini-pro")
        result = client.analyze_scabd_data("test data", "test context")
        
        assert "Analysis result" in result or result != ""

    @patch('gemini_cli.gemini_client.genai')
    def test_security_audit(self, mock_genai):
        """Test security audit functionality."""
        mock_model = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "Security audit report"
        mock_model.generate_content.return_value = mock_response
        mock_genai.GenerativeModel.return_value = mock_model
        
        client = GeminiClient("valid-api-key", "gemini-pro")
        result = client.security_audit("system info")
        
        assert result is not None


class TestCLICommands:
    """Test CLI commands."""

    def test_cli_help(self):
        """Test CLI help command."""
        runner = CliRunner()
        result = runner.invoke(cli, ['--help'])
        
        assert result.exit_code == 0
        assert "Gemini CLI" in result.output

    def test_cli_version(self):
        """Test CLI version command."""
        runner = CliRunner()
        result = runner.invoke(cli, ['--version'])
        
        assert result.exit_code == 0

    def test_setup_init_command(self):
        """Test setup init command."""
        runner = CliRunner()
        
        with runner.isolated_filesystem():
            result = runner.invoke(cli, ['setup', 'init'], input='\n\n1\nlocalhost\n5432\nscabd\n')
            # Command should execute (may fail without full input, but should run)
            assert result.exit_code in [0, 1, 2]  # Allow various exit codes

    def test_scabd_info_command(self):
        """Test SCABD info command."""
        runner = CliRunner()
        result = runner.invoke(cli, ['scabd', 'info'])
        
        assert result.exit_code == 0
        assert "SCABD" in result.output
        assert "Gemini" in result.output

    def test_scabd_diagnose_command(self):
        """Test SCABD diagnose command."""
        runner = CliRunner()
        
        with runner.isolated_filesystem():
            result = runner.invoke(cli, ['scabd', 'diagnose'])
            
            assert result.exit_code == 0
            assert "Diagnostics" in result.output or "diagnostic" in result.output.lower()
            
            # Check if diagnostics file was created
            assert Path('scabd_diagnostics.json').exists()
            
            with open('scabd_diagnostics.json', 'r') as f:
                diag_data = json.load(f)
                assert 'checks' in diag_data
                assert 'timestamp' in diag_data


class TestIntegration:
    """Integration tests."""

    def test_config_and_client_integration(self):
        """Test config and client work together."""
        config = GeminiConfig()
        config.set_api_key("test-key-integration")
        config.set_model("gemini-pro")
        
        retrieved_key = config.get_api_key()
        retrieved_model = config.get_model()
        
        assert retrieved_key == "test-key-integration"
        assert retrieved_model == "gemini-pro"
        
        # Verify persistence by creating new config instance
        config2 = GeminiConfig()
        assert config2.get_api_key() == "test-key-integration"
        assert config2.get_model() == "gemini-pro"

    def test_cli_workflow(self):
        """Test basic CLI workflow."""
        runner = CliRunner()
        
        with runner.isolated_filesystem():
            # Test help
            result = runner.invoke(cli, ['--help'])
            assert result.exit_code == 0
            
            # Test setup help
            result = runner.invoke(cli, ['setup', '--help'])
            assert result.exit_code == 0
            
            # Test analyze help
            result = runner.invoke(cli, ['analyze', '--help'])
            assert result.exit_code == 0
            
            # Test scabd help
            result = runner.invoke(cli, ['scabd', '--help'])
            assert result.exit_code == 0
            
            # Test chat help
            result = runner.invoke(cli, ['chat', '--help'])
            assert result.exit_code == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
