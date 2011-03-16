from django_evolution.mutations import *
from django.db import models

MUTATIONS = [
    AddField('Author', 'user', models.ForeignKey, initial=1, related_model='auth.User')
]
