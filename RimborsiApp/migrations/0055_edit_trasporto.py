# Generated by Django 2.2.3 on 2024-08-03 07:59

import RimborsiApp.models
import RimborsiApp.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RimborsiApp', '0054_remove_altrespese_textfield'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trasporto',
            name='img_scontrino',
            field=models.ImageField(blank=True, null=True, upload_to=RimborsiApp.models.trasporti_path),
        ),
    ]
