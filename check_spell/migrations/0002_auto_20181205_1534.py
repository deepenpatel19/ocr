# Generated by Django 2.1.4 on 2018-12-05 15:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('check_spell', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='upload_file',
            new_name='UploadImage',
        ),
    ]