# Generated by Django 4.1.1 on 2022-09-19 21:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0004_alter_restaurantmodel_administrator'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='menudishassociatemodel',
            unique_together={('menu', 'dish')},
        ),
    ]
