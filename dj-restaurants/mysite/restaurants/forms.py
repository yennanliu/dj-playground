from django import forms

class CommentForm(forms.Form):
	# ordering matters, since this ordering will sync with the ones on HTML
	visitor = forms.CharField(max_length=20)
	email = forms.EmailField(max_length=20, required=False)
	content = forms.CharField(max_length=200, widget=forms.Textarea())