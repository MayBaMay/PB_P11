# Generated by Django 3.0.2 on 2020-02-11 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodSearch', '0004_auto_20200211_1011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favorite',
            name='initial_search_product',
            field=models.IntegerField(default=True),
            preserve_default=False,
        ),
    ]
