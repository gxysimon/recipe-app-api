"""
Django command to wait for the database to be available.
"""
import time

from psycopg2 import OperationalError as Psycopg2OpError

from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to wait for database."""

    def handle(self, *args, **options):
        """Entrypoint for command."""
        self.stdout.write('Waiting for database...')
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True # assume exceptions were not raised
            except (Psycopg2OpError, OperationalError): # if database is not ready, raise a error, depending on the stage it stops
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)
        # if true, the while loop will stop, because bd_up is not false

        self.stdout.write(self.style.SUCCESS('Database available!')) # database is available