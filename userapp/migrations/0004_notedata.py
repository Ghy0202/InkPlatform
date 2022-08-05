# Generated by Django 3.2.12 on 2022-06-25 09:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0003_scrapydata'),
    ]

    operations = [
        migrations.CreateModel(
            name='NoteData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.EmailField(max_length=100)),
                ('create_at', models.DateTimeField(default=datetime.datetime.now)),
                ('username', models.EmailField(max_length=100)),
                ('content', models.EmailField(max_length=600)),
            ],
            options={
                'db_table': 'NoteData',
            },
        ),
    ]
