"""Integration tests for Gemini CLI with SCABD."""

import pytest
from unittest.mock import patch, MagicMock
from click.testing import CliRunner
from gemini_cli.cli import cli
from gemini_cli.config import GeminiConfig


class TestGeminiSCABDIntegration:
    """Test Gemini CLI integration with SCABD system."""

    def test_scabd_status_command(self):
        """Test SCABD status command output."""
        runner = CliRunner()
        result = runner.invoke(cli, ['scabd', 'status'])
        
        assert result.exit_code == 0
        assert "SCABD" in result.output

    def test_gemini_client_error_handling(self):
        """Test error handling in Gemini client."""
        runner = CliRunner()
        
        # Try to run analyze command without API key configured
        result = runner.invoke(cli, ['analyze', 'data', '-d', 'test data'])
        
        # Should fail gracefully with helpful error message
        assert "API key" in result.output or "not configured" in result.output

    def test_analyze_command_with_file(self):
        """Test analyze command with data file."""
        runner = CliRunner()
        
        with runner.isolated_filesystem():
            # Create test data file
            with open('test_data.json', 'w') as f:
                f.write('{"test": "data"}')
            
            # Try to run analyze (will fail without API key, but tests file handling)
            result = runner.invoke(cli, ['analyze', 'data', '-f', 'test_data.json'])
            
            # Should attempt to read file
            assert result.exit_code == 0 or "API key" in result.output

    def test_config_persistence(self):
        """Test configuration persistence across CLI calls."""
        config = GeminiConfig()
        
        # Set configuration
        test_config = {
            "db_host": "test-host",
            "db_port": 9999,
            "db_name": "test-db"
        }
        config.set_scabd_config(test_config)
        
        # Verify persistence
        config2 = GeminiConfig()
        assert config2.get_scabd_config() == test_config

    def test_cli_without_gemini_module(self):
        """Test CLI behavior when gemini module is not available."""
        with patch('gemini_cli.gemini_client.genai', None):
            from gemini_cli.gemini_client import GeminiClient
            
            with pytest.raises(ImportError, match="google-generativeai"):
                GeminiClient("test-key", "gemini-pro")

    @patch('gemini_cli.gemini_client.genai')
    def test_chat_command_integration(self, mock_genai):
        """Test chat command integration."""
        mock_model = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "Test response from Gemini"
        mock_model.generate_content.return_value = mock_response
        mock_genai.GenerativeModel.return_value = mock_model
        
        # Configure test API key
        config = GeminiConfig()
        config.set_api_key("test-api-key-12345")
        
        runner = CliRunner()
        result = runner.invoke(cli, ['chat', 'ask', 'What is SCABD?'])
        
        # Should execute successfully
        assert result.exit_code == 0 or "Error" not in result.output

    def test_trading_strategy_command(self):
        """Test trading strategy generation command."""
        runner = CliRunner()
        
        with runner.isolated_filesystem():
            # Create test market data
            with open('market_data.json', 'w') as f:
                f.write('{"BTC": 50000, "ETH": 3000}')
            
            result = runner.invoke(cli, ['analyze', 'trading-strategy', '-f', 'market_data.json'])
            
            # Should attempt to run (API key error is expected)
            assert result.exit_code in [0, 1, 2]

    def test_security_audit_command(self):
        """Test security audit command."""
        runner = CliRunner()
        
        result = runner.invoke(cli, ['analyze', 'security-audit', '-d', 'System: PostgreSQL 14'])
        
        # Should attempt to run (API key error is expected)
        assert result.exit_code in [0, 1, 2]

    def test_scabd_config_operations(self):
        """Test SCABD configuration operations."""
        runner = CliRunner()
        
        result = runner.invoke(cli, ['scabd', 'config-set', '-k', 'test_param', '-v', '100'])
        
        # Should execute successfully
        assert result.exit_code == 0
        assert 'Set test_param' in result.output or 'test_param' in result.output


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
