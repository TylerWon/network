# Generated by Django 3.0.8 on 2021-07-30 20:35

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0006_auto_20210730_2028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='followers',
            field=models.ManyToManyField(null=True, related_name='_user_followers_+', to=settings.AUTH_USER_MODEL),
        ),
    ]
