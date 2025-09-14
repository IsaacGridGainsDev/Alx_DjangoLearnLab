from django import forms
from .models import Book

class ExampleForm(forms.ModelForm):
    """Form for creating and updating books."""
    
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']

    def clean_title(self):
        title = self.cleaned_data['title']
        if 'badword' in title.lower():
            raise forms.ValidationError("Title contains badword")
        elif not title or len(title.strip()) < 3:
            raise forms.ValidationError("Title must be at least 3 characters long")
        return title.strip()

    def clean_author(self):
        author = self.cleaned_data['author']
        if 'badword' in author.lower():
            raise forms.ValidationError("Author contains badword")
        elif not author or len(author.strip()) < 3:
            raise forms.ValidationError("Author must be at least 3 characters long")
        return author.strip()
    
    def clean_publication_year(self):
        publication_year = self.cleaned_data['publication_year']
        if not publication_year or publication_year < 1900 or publication_year > 2100:
            raise forms.ValidationError("Publication year must be between 1900 and 2100")
        return publication_year
    