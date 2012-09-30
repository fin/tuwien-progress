from django.core.management.base import BaseCommand, CommandError
from project.progress.models import *


class Command(BaseCommand):
    args = '<url>'
    help = 'Parses the given url as a tiss curriculum'

    def handle(self, *args, **options):
        if not args:
            self.stderr.write("need url parameter")

        url = args[0]
        Curriculum.parse_from_curriculum_url(url)
