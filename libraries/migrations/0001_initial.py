# Generated by Django 3.2.7 on 2021-09-28 07:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('books', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Library',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('favorite', models.BooleanField(default=False)),
                ('reading', models.BooleanField(default=False)),
                ('current_page', models.IntegerField()),
            ],
            options={
                'db_table': 'libraries',
            },
        ),
        migrations.CreateModel(
            name='LibraryBook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.book')),
                ('library', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='libraries.library')),
                ('shelf', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.shelf')),
            ],
            options={
                'db_table': 'library_books',
            },
        ),
        migrations.AddField(
            model_name='library',
            name='book',
            field=models.ManyToManyField(through='libraries.LibraryBook', to='books.Book'),
        ),
        migrations.AddField(
            model_name='library',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user'),
        ),
    ]
