# Generated by Django 2.2.5 on 2019-09-27 05:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20190927_1451'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='is_publick',
            new_name='is_public',
        ),
    ]
