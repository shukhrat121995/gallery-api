# Generated by Django 3.1 on 2021-03-20 13:39

from django.db import migrations
import forceartsapi.models


class Migration(migrations.Migration):

    dependencies = [
        ('forceartsapi', '0008_contactus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='title',
            field=forceartsapi.models.TitleField(max_length=255, null=True, unique=True),
        ),
    ]
