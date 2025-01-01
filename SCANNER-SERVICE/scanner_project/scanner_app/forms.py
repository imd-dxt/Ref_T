from django import forms

class URLScanForm(forms.Form):
    target_url = forms.URLField(label='Enter URL to Scan', widget=forms.URLInput(attrs={'placeholder': 'http://example.com'}))