# Generated by Django 4.1.7 on 2023-03-19 06:18

from django.db import migrations, models
import django.utils.timezone
import storages.backends.s3boto3


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Element',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('element_type', models.CharField(choices=[('Earth', 'Earth'), ('Air', 'Air'), ('Darkness', 'Darkness'), ('Fire', 'Fire'), ('Lightning', 'Lightning'), ('Water', 'Water')], max_length=20)),
                ('image', models.ImageField(storage=storages.backends.s3boto3.S3Boto3Storage(), upload_to='')),
                ('uploaded_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Entity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entity_type', models.CharField(choices=[('Earth', 'Earth'), ('Air', 'Air'), ('Darkness', 'Darkness'), ('Fire', 'Fire'), ('Lightning', 'Lightning'), ('Water', 'Water')], max_length=20)),
                ('image', models.ImageField(storage=storages.backends.s3boto3.S3Boto3Storage(), upload_to='')),
                ('uploaded_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
