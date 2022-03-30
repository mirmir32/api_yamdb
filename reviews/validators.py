from django import forms


def validate_emptiness(value):
    if value == '':
        raise forms.ValidationError(
            'Add review text.',
            params={'value': value}
        )
