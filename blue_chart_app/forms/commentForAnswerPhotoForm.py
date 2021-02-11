# -*- coding: utf-8 -*-
"""
Created on Fri Jan  8 12:42:18 2021

@author: Mayuko
"""


from django import forms
from blue_chart_app.models.comment_for_answer_photo import CommentForAnswerPhoto


class CommentForAnswerPhotoForm(forms.ModelForm):
    
    class Meta:
        
        model = CommentForAnswerPhoto
        
        fields = {'content',}
        
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control'})
            }
        
        labels = {
            'content': 'コメント'}
        
        requires = {
            'content': False}
    
    def clean_content(self):
        
        content = self.cleaned_data['content']
        if len(content) == 0 or content is None:
            
            raise forms.ValidationError('コメントを入力してください')
            
        return content
        
    
    