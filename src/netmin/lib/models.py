from django.db import models


class BaseModel(models.Model):

    @property
    def action_label(self):
        return 'Update' if self.id else 'Add'
