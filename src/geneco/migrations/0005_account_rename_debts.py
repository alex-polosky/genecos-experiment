# Generated by Django 5.0.6 on 2024-06-10 00:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geneco', '0004_rename_base_pubk_to_uuid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='remaining_debt',
            new_name='balance',
        ),
        migrations.RenameField(
            model_name='account',
            old_name='original_debt',
            new_name='debt',
        ),
    ]
