from django.db import models
import os
import sys
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from PIL import Image


sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from common.models import User

class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_question')
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_question')
    image = models.ImageField(upload_to='image/', blank=True, null=True)
    #image_thumbnail = ImageSpecField(source='image', processors=[ResizeToFill(500, 200)], format='JPEG', options={'quality': 100})

    def img_save(self):
        if self.image:
            img = Image.open(self.image.path)
            max_width = 500    #가로사이즈 고정
            max_height = 200   #세로사이즈 고정
            bow_width = 600    #최대 가로사이즈
            bow_height = 400   #최대 세로사이즈
            if img.width > bow_width or img.height > bow_height:
                img.thumbnail((bow_width, bow_height), Image.ANTIALIAS)
            elif img.width > max_width:
                img.thumbnail((img.width, max_height), Image.ANTIALIAS)
            elif img.height > max_height:
                img.thumbnail((max_width, img.height), Image.ANTIALIAS)
            img.thumbnail((max_width, max_height), Image.ANTIALIAS)
            img.save(self.image.path, format='JPEG', quality=100)
       

    
    def __str__(self):
        return self.subject
    
class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_answer')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_answer')

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE)
