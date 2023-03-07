from django import forms
from .models import ElementTile, Wizard


class GameForm(forms.Form):
    selected_elements = forms.ModelMultipleChoiceField(queryset=ElementTile.objects.filter(face_up=True),
                                                       widget=forms.CheckboxSelectMultiple)

    def __init__(self, *args, **kwargs):
        self.player_hand = kwargs.pop('player_hand', None)
        super().__init__(*args, **kwargs)

        if self.player_hand is not None:
            # dynamically update the queryset based on player's hand
            self.fields['selected_elements'].queryset = ElementTile.objects.filter(
                face_down=True, element_type__in=self.player_hand
            )

    def clean(self):
        cleaned_data = super().clean()
        selected_elements = cleaned_data.get('selected_elements', [])
        num_elements = len(selected_elements)

        # make sure the player only selects 2 elements at a time
        if num_elements != 2:
            raise forms.ValidationError("You must select exactly 2 elements.")

        # make sure the selected elements are face-down
        for element in selected_elements:
            if not element.face_down:
                raise forms.ValidationError("You can only select face-down elements.")

        return cleaned_data


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = Wizard
        fields = ['image']


class ElementImageUploadForm(forms.ModelForm):
    class Meta:
        model = ElementTile
        fields = ['image']


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
    entity_tye = forms.ChoiceField(choices=ENTITY_TYPES)
    element_images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    entity_images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
