from django import forms

from blogsmith import TAG_SEPARATOR
from blogsmith.models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('title', 'posted')

    tags = forms.CharField(required=False)
    content = forms.CharField()

    def clean_tags(self):
        stripped_tags = [x.strip() for x in self.cleaned_data['tags'].split(TAG_SEPARATOR)]

        return [x for x in stripped_tags if len(x) > 0]
