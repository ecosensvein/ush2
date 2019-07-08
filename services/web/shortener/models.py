from django.db import models


class Url(models.Model):
    subpart_inner = models.SlugField(max_length=6, primary_key=True)
    subpart_outer = models.URLField(max_length=400)
    created_at = models.DateTimeField(auto_now=True)
    session_key = models.CharField(max_length=40)


def __str__(self):
    return self.subpart_inner
