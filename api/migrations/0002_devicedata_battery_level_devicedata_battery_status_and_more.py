# Generated by Django 4.2 on 2023-04-20 16:48

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='devicedata',
            name='battery_level',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='devicedata',
            name='battery_status',
            field=models.CharField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='devicedata',
            name='location_finished',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='devicedata',
            name='location_horizontal_accuracy',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='devicedata',
            name='location_is_inaccurate',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='devicedata',
            name='location_is_old',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='devicedata',
            name='location_position_type',
            field=models.CharField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='devicedata',
            name='location_timestamp',
            field=models.DateTimeField(default='2018-12-25 09:27:53'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='devicedata',
            name='location_vertical_accuracy',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='devicedata',
            name='identifier',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='devicedata',
            name='location',
            field=django.contrib.gis.db.models.fields.PointField(geography=True, srid=4326, verbose_name='location'),
        ),
        migrations.AlterField(
            model_name='devicedata',
            name='name',
            field=models.CharField(max_length=250),
        ),
    ]