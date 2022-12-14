# Generated by Django 3.2.12 on 2022-06-21 12:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0002_userinfo_state'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScrapyData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filepath', models.CharField(max_length=100)),
                ('filename', models.CharField(max_length=50)),
                ('create_at', models.DateTimeField(default=datetime.datetime.now)),
                ('username', models.CharField(max_length=100)),
                ('type', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'ScrapyData',
            },
        ),
    ]
