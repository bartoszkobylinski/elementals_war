from django import forms


class ImageForm(forms.Form):
    ELEMENT_TYPES = (
        ('Earth', 'Earth'),
        ('Air', 'Air'),
        ('Darkness', 'Darkness'),
        ('Fire', 'Fire'),
        ('Lightning', 'Lightning'),
        ('Water', 'Water')
    )
    ENTITY_TYPES = (
        ('Earth', 'Earth'),
        ('Air', 'Air'),
        ('Darkness', 'Darkness'),
        ('Fire', 'Fire'),
        ('Lightning', 'Lightning'),
        ('Water', 'Water')
    )
    element_type = forms.ChoiceField(choices=ELEMENT_TYPES)
    entity_type = forms.ChoiceField(choices=ENTITY_TYPES)
    element_images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    entity_images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
