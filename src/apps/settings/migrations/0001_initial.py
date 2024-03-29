# Generated by Django 4.1.7 on 2023-05-10 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ServicePackage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=100)),
                ('technologies', models.CharField(max_length=255)),
                ('type', models.CharField(max_length=20)),
                ('downstream', models.FloatField()),
                ('upstream', models.FloatField()),
            ],
        ),
    ]
