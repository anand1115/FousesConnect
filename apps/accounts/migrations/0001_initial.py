# Generated by Django 4.0.5 on 2022-06-06 13:28

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=250)),
                ('last_name', models.CharField(max_length=250)),
                ('phonenumber', models.CharField(max_length=15, unique=True)),
                ('email', models.EmailField(max_length=250, unique=True)),
                ('active', models.BooleanField(default=False)),
                ('admin', models.BooleanField(default=False)),
                ('added_on', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
