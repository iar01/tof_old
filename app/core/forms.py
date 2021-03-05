from django import forms

from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.conf import settings



def SignupDomainValidator(value):
    if '*' not in settings.ALLOWED_SIGNUP_DOMAINS:
        try:
            domain = value[value.index("@"):]
            if domain not in settings.ALLOWED_SIGNUP_DOMAINS:
                raise ValidationError(u'Invalid domain. Allowed domains on this network: {0}'.format(','.join(settings.ALLOWED_SIGNUP_DOMAINS)))
        except Exception:
            raise ValidationError(u'Invalid domain. Allowed domains on this network: {0}'.format(','.join(settings.ALLOWED_SIGNUP_DOMAINS)))

def ForbiddenUsernamesValidator(value):
    forbidden_usernames = ['admin', 'settings', 'news', 'about', 'help', 'signin', 'signup',
        'signout', 'terms', 'privacy', 'cookie', 'new', 'login', 'logout', 'administrator',
        'join', 'account', 'username', 'root', 'blog', 'user', 'users', 'billing', 'subscribe',
        'reviews', 'review', 'blog', 'blogs', 'edit', 'mail', 'email', 'home', 'job', 'jobs',
        'contribute', 'newsletter', 'shop', 'profile', 'register', 'auth', 'authentication',
        'campaign', 'config', 'delete', 'remove', 'forum', 'forums', 'download', 'downloads',
        'contact', 'blogs', 'feed', 'feeds', 'faq', 'intranet', 'log', 'registration', 'search',
        'explore', 'rss', 'support', 'status', 'static', 'media', 'setting', 'css', 'js',
        'follow', 'activity', 'questions', 'articles', 'network',]
    if value.lower() in forbidden_usernames:
        raise ValidationError('This is a reserved word.')

def InvalidUsernameValidator(value):
    if '@' in value or '+' in value or '-' in value:
        raise ValidationError('Enter a valid username.')

def UniqueEmailValidator(value):
    if User.objects.filter(email__iexact=value).exists():
        raise ValidationError('User with this Email already exists.')

def UniqueUsernameIgnoreCaseValidator(value):
    if User.objects.filter(username__iexact=value).exists():
        raise ValidationError('User with this Username already exists.')

class SignUpForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),
        max_length=30,
        required=True,
        help_text='Usernames may contain <strong>alphanumeric</strong>, <strong>_</strong> and <strong>.</strong> characters')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}),
        label="Confirm your password",
        required=True)
    email = forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control'}),
        required=True,
        max_length=75)

    class Meta:
        model = User
        exclude = ['last_login', 'date_joined']
        fields = ['username', 'email', 'password', 'confirm_password',]

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].validators.append(ForbiddenUsernamesValidator)
        self.fields['username'].validators.append(InvalidUsernameValidator)
        self.fields['username'].validators.append(UniqueUsernameIgnoreCaseValidator)
        self.fields['email'].validators.append(UniqueEmailValidator)
        self.fields['email'].validators.append(SignupDomainValidator)

    def clean(self):
        super(SignUpForm, self).clean()
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and password != confirm_password:
            self._errors['password'] = self.error_class(['Passwords don\'t match'])
        return self.cleaned_data
        
class ProfileForm(forms.ModelForm):
    
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), 
        max_length=30,
        required=False)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), 
        max_length=30,
        required=False)
    job_title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), 
        max_length=50,
        required=False)
    email = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),
        max_length=75,
        required=False)
    url = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), 
        max_length=50,
        required=False)
    location = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), 
        max_length=50,
        required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'job_title', 'email', 'url', 'location',]

    def full_clean(self):
        'Strip whitespace automatically in all form fields'
        data = self.data.copy()
        if data:
            for k, vs in self.data.lists():
                new_vs = []
                for v in vs:
                    new_vs.append(v.strip())
                data.setlist(k, new_vs)
            self.data = data
        super(ProfileForm, self).full_clean()


class ChangePasswordForm(forms.ModelForm):
    id = forms.CharField(widget=forms.HiddenInput())
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}), 
        label="Old password",
        required=True)

    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}), 
        label="New password",
        required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}), 
        label="Confirm new password",
        required=True)

    class Meta:
        model = User
        fields = ['id', 'old_password', 'new_password', 'confirm_password']

    def clean(self):
        super(ChangePasswordForm, self).clean()
        old_password = self.cleaned_data.get('old_password')
        new_password = self.cleaned_data.get('new_password')
        confirm_password = self.cleaned_data.get('confirm_password')
        id = self.cleaned_data.get('id')
        user = User.objects.get(pk=id)
        if not user.check_password(old_password):
            self._errors['old_password'] = self.error_class(['Old password don\'t match'])
        if new_password and new_password != confirm_password:
            self._errors['new_password'] = self.error_class(['Passwords don\'t match'])
        return self.cleaned_data