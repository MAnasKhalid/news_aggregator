# Generated by Django 3.2.12 on 2022-02-28 23:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod_api', '0002_auto_20220301_0214'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='token',
            field=models.CharField(default='ukraine', max_length=200),
            preserve_default=False,
        ),
    ]
