# Generated by Django 4.0.3 on 2022-03-18 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('powers', '0001_initial'),
        ('supers', '0008_rename_primary_ability_super_powers_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='super',
            name='powers',
            field=models.ManyToManyField(to='powers.power'),
        ),
    ]
