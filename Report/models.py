# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class History(models.Model):
    id = models.IntegerField(db_column='ID', blank=True, primary_key=True)  # Field name made lowercase.
    user_id = models.IntegerField(blank=True, null=True)
    user_action = models.TextField(blank=True, null=True)
    action_post_id = models.IntegerField(blank=True, null=True)
    action_post_type = models.TextField(blank=True, null=True)
    action_time = models.TextField(blank=True, null=True)
    leave_time = models.TextField(blank=True, null=True)
    ip = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'history'


class User(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    spark_id = models.CharField(max_length=255)
    stu_id = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    privilege = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'user'


class WpPosts(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    post_author = models.BigIntegerField()
    post_date = models.DateTimeField(blank=True, null=True)
    post_date_gmt = models.DateTimeField(blank=True, null=True)
    post_content = models.TextField()
    post_title = models.TextField()
    post_excerpt = models.TextField()
    post_status = models.CharField(max_length=20)
    comment_status = models.CharField(max_length=20)
    ping_status = models.CharField(max_length=20)
    post_password = models.CharField(max_length=255)
    post_name = models.CharField(max_length=200)
    to_ping = models.TextField()
    pinged = models.TextField()
    post_modified = models.DateTimeField(blank=True, null=True)
    post_modified_gmt = models.DateTimeField(blank=True, null=True)
    post_content_filtered = models.TextField()
    post_parent = models.BigIntegerField()
    guid = models.CharField(max_length=255)
    menu_order = models.IntegerField()
    post_type = models.CharField(max_length=20)
    post_mime_type = models.CharField(max_length=100)
    comment_count = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'wp_posts'
