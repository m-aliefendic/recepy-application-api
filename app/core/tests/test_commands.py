"""
Test custom Django mangment commands.
"""
from unittest import patch

from psycopg2 import OperationalError as Psycop2Error

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase

@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test commands."""

    def test_wait_for_db_ready(self,pached_check):
        """Test waiting for database if database redy."""
        pached_check.return_value =True

        call_command('wait_for_db')

        pached_check.assert_called_once_with(database=['default'])
