from django import forms


def validate_emptiness(value):
    """
    Валидатор контролирует поле, чтобы оно было заполнено.
    """
    if value == '':
        raise forms.ValidationError(
            'Add review text.',
            params={'value': value}
        )
