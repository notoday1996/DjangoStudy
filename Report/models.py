# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class User(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    spark_id = models.CharField(max_length=255)
    stu_id = models.CharField(max_length=255)
    email = models.CharField(max_length=255, blank=True, null=True)
    privilege = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'user'
