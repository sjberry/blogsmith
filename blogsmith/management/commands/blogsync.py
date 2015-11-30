import io
import os
import re
from datetime import datetime

from django.core.management.base import BaseCommand
from django.utils.text import slugify

from blogsmith import client
from blogsmith.localization import localize
from blogsmith.models import Article


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # TODO: Delete articles if they've been removed from dropbox. We shouldn't have to rely 100% on the webhook for this.
        for filename, version in client.get_files('/'):
            if Article.objects.filter(remote_path__exact=filename, version=version).exists():
                continue

            name, ext = os.path.splitext(filename)

            if ext != '.md':
                continue

            buffer = ''
            title = name
            posted = None
            tags = []

            # TODO: Support passing in the hash in case nothing has changed and handling 304 responses.
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
                        posted = localize(datetime.strptime(value.strip(), '%m/%d/%Y'))
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
                article.remote_path = filename
                article.version = version

                self.stdout.write('Updating `{0}` in db.'.format(slug))
            except Article.DoesNotExist:
                article = Article(
                    title=title,
                    slug=slug,
                    posted=posted,
                    remote_path=filename,
                    version=version
                )

                self.stdout.write('Publishing `{0}` to db.'.format(slug))

            self.stdout.write('Posted => {0}'.format(posted))
            self.stdout.write('Tags => {0}'.format(tags))
            self.stdout.write('\n')

            article.publish(buffer, tags, validate_unique=False)
