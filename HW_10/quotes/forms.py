from django import forms
from .models import Author, Quotes



class AddAuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['fullname', 'born_date', 'born_loc', 'desc']
        labels = {
            "fullname": "Authors Full Name",
            "born_date": "Date of birth",
            "born_loc": "Birth location",
            "desc": "Description",
        }


class AddQuoteForm(forms.ModelForm):
    custom_author = forms.CharField(label='Custom Author', required=False)
    existing_author = forms.ModelChoiceField(queryset=Author.objects.all(),
                                             label='Existing Author', required=False)

    class Meta:
        model = Quotes
        fields = ['quote']
        labels = {
            'quote': 'Quote',
        }

    def save(self, commit=True):
        quote = super().save(commit=False)

        if commit:
            quote.save()

        custom_author = self.cleaned_data['custom_author']
        existing_author = self.cleaned_data['existing_author']
        if custom_author:
            author, created = Author.objects.get_or_create(fullname=custom_author)
            quote.author = author
        elif existing_author:
            quote.author = existing_author

        if commit:
            quote.save()
        return quote
