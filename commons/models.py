from django.db import models

class AbstractCustomModel(models.Model):
    createon = models.DateTimeField(auto_now_add=True, null=True)
    editedon = models.DateTimeField(auto_now=True, null=True)
    createdby = models.ForeignKey(to='users.User', null=True, on_delete=models.PROTECT,
                                  related_name='%(app_label)s_%(class)s_createdby')
    editedby = models.ForeignKey(to='users.User', null=True, on_delete=models.PROTECT,
                                 related_name='%(app_label)s_%(class)s_editedby')


    class Meta:
        abstract = True
