# Generated by Django 2.1.7 on 2019-02-22 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Image', '0002_image_size'),
    ]

    operations = [
        migrations.RenameField(
            model_name='image',
            old_name='image',
            new_name='image_file',
        ),
        migrations.AddField(
            model_name='image',
            name='image_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
