import base64

from django.core.files.base import ContentFile
from django.db import models
from django.utils.text import slugify
from django.utils.timezone import now

from blogsmith import ROOT_DIR
from blogsmith.renderers import MarkdownRenderer
from blogsmith.storage import OverwriteFileSystemStorage


fs = OverwriteFileSystemStorage(location=ROOT_DIR)


class Article(models.Model):
    title = models.CharField(blank=False, max_length=120, unique=True)
    slug = models.CharField(blank=False, db_index=True, max_length=120, unique=True)
    content = models.FileField(storage=fs)
    revision = models.CharField(blank=True, max_length=50)
    posted = models.DateTimeField(blank=True)
    updated = models.DateTimeField(auto_now=True)
    is_draft = models.BooleanField(default=False)

    tags = models.ManyToManyField('Tag', related_name='articles')

    def pre_save(self):
        # Setting this value automatically is done here instead of with auto_now_add=True because we want to retain the
        # field as editable so that the posted date can be overridden.
        if not self.pk and not self.posted:
            self.posted = now()

        if not self.slug:
            self.slug = slugify(self.title)

    def publish(self, content, tags=(), validate_unique=True):
        self.full_clean(validate_unique=validate_unique, exclude={'content', 'slug', 'source'})

        filename = base64.urlsafe_b64encode(self.title.encode()).decode()
        parsed = ContentFile(MarkdownRenderer().render(content))

        self.content.save(filename, parsed, save=False)
        self.save()
        self.tags.clear()

        for tag_name in tags:
            try:
                tag = Tag.objects.get(slug__exact=slugify(tag_name))
            except Tag.DoesNotExist:
                tag = Tag(name=tag_name)
                tag.save()

            self.tags.add(tag)


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.CharField(db_index=True, max_length=50, unique=True)

    def pre_save(self):
        if not self.slug:
            self.slug = slugify(self.name)
