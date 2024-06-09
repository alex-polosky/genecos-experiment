# Generated by Django 5.0.6 on 2024-06-09 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geneco', '0001_initial_refs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consumer',
            name='ssn_hash',
            field=models.CharField(help_text='base64 repr of SHA 256 hash digest of ssn', max_length=64),
        ),
    ]