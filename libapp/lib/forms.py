from django import forms
class libform(forms.Form):
    Book_name = forms.CharField(max_length=30,required=True)
    Book_author = forms.CharField(max_length=30,required=True)
    Book_category = forms.CharField(max_length=30,required=True)
    Book_shelf = forms.CharField(max_length=30,required=True)
    Number_of_available_copies = forms.IntegerField(required=True)
    isbn = forms.CharField( max_length=13,required=True)
    Image = forms.ImageField(required=False)
    Summary = forms.CharField(widget=forms.Textarea,required=True)



class Sform(forms.Form):
    Book_name = forms.CharField(max_length=30)
class returnss(forms.Form):
    Return_Code = forms.CharField(max_length=30)






