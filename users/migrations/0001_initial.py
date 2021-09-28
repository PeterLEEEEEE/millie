# Generated by Django 3.2.7 on 2021-09-28 07:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Platform',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'platforms',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('nickname', models.CharField(max_length=45, unique=True)),
                ('profile_image_url', models.CharField(max_length=500)),
                ('social_id', models.CharField(max_length=100)),
                ('platform', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.platform')),
            ],
            options={
                'db_table': 'users',
            },
        ),
    ]
