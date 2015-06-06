import io
import os
import re
from datetime import datetime

from django.core.management.base import BaseCommand
from django.utils.text import slugify

from blogsmith import client
from blogsmith.models import Article


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        filenames = client.get_file_names('/')

        for filename in filenames:
            name, ext = os.path.splitext(filename)

            if ext != '.md':
                continue

            buffer = ''
            title = name
            posted = None
            tags = []

            file, metadata = client.get_file_and_metadata(filename)

            with file:
                file_content = file.read().decode()

            for line in io.StringIO(file_content):
                match_obj = re.match(r'^@(\w+) (.+)$', line)

                if match_obj:
                    key = match_obj.group(1).lower()
                    value = match_obj.group(2)

                    if key == 'title':
                        title = value
                    elif key == 'date':
                        posted = datetime.strptime(value.strip(), '%m/%d/%Y')
                    elif key == 'tags':
                        tags = re.split(r',\s*', value.strip())
                else:
                    buffer += line

            buffer = buffer.strip()
            slug = slugify(title)

            try:
                article = Article.objects.get(slug__exact=slug)
                article.title = title
                article.posted = posted
                self.stdout.write('Updating `{0}` in db.'.format(slug))
            except Article.DoesNotExist:
                article = Article(
                    title=title,
                    slug=slug,
                    posted=posted
                )
                self.stdout.write('Publishing `{0}` to db.'.format(slug))

            self.stdout.write('Posted => {1}'.format(posted))
            self.stdout.write('Tags => {0}'.format(tags))
            self.stdout.write('\n')

            article.publish(buffer, tags, validate_unique=False)
