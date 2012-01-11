from django.forms import ModelForm, DateField
from django.forms.extras.widgets import SelectDateWidget
from django.forms.models import inlineformset_factory
from title.models import *

class JournalForm(ModelForm):
    class Meta:
        model = Journal
        exclude = ('collection',)
        widgets = {
            'init_year': SelectDateWidget(),
            'final_year': SelectDateWidget(),            
        }

class InstitutionForm(ModelForm):
    class Meta:
        model = Institution
        exclude = ('collection',)

class UserForm(ModelForm):
    class Meta:
        model = User
        exclude = ('is_staff','is_superuser','last_login','date_joined','groups',
                   'user_permissions')
    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

