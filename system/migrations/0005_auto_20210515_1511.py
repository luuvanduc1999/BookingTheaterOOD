# Generated by Django 3.1.7 on 2021-05-15 15:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0004_auto_20210514_2226'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='ticket',
            unique_together={('room', 'time', 'date')},
        ),
    ]
