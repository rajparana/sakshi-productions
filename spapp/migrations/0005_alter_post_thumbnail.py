# Generated by Django 4.1.1 on 2022-12-01 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spapp', '0004_album_category_alter_post_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='thumbnail',
            field=models.ImageField(default=1, upload_to='thumbnails/'),
            preserve_default=False,
        ),
    ]
