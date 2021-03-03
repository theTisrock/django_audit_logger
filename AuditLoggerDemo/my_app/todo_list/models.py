from django.db import models


class ListItem(models.Model):
    item = models.CharField(max_length=150)
    complete = models.BooleanField(default=False)  # model has proper component for implementation of 'toggle'

    def __str__(self):
        return self.item
