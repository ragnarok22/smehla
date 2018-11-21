from django import forms


class BMDWidget(forms.Widget):
    def __init__(self, attrs=None):
        self.attrs = {'class': 'form-control'} if attrs is None else attrs.copy()
        super(BMDWidget, self).__init__(self.attrs)


class Select(BMDWidget, forms.Select):
    def __init__(self):
        super(Select, self).__init__({'class': 'form-control custom-select'})


class TextInput(BMDWidget, forms.TextInput):
    def __init__(self):
        super(TextInput, self).__init__()


class DateInput(BMDWidget, forms.DateInput):
    def __init__(self):
        super(DateInput, self).__init__({'class': 'form-control datepicker'})


class EmailInput(BMDWidget, forms.EmailInput):
    def __init__(self):
        super(EmailInput, self).__init__()


class NumberInput(BMDWidget, forms.NumberInput):
    def __init__(self):
        super(NumberInput, self).__init__()
