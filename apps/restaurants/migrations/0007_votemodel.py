# Generated by Django 4.1.1 on 2022-09-19 22:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('restaurants', '0006_dishmodel_price_dishmodel_weight'),
    ]

    operations = [
        migrations.CreateModel(
            name='VoteModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('menu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votes', to='restaurants.menumodel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'votes',
                'unique_together': {('menu', 'user')},
            },
        ),
    ]
