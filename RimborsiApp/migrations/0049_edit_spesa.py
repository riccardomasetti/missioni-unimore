# Generated by Django 2.2.3 on 2024-08-02 08:22

import RimborsiApp.models
import RimborsiApp.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RimborsiApp', '0048_add_pernottamenti_missione'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='spesa',
            options={'verbose_name': 'Spesa', 'verbose_name_plural': 'Spese'},
        ),
        migrations.AlterModelOptions(
            name='spesamissione',
            options={'verbose_name': 'Spesa Missione', 'verbose_name_plural': 'Spese Missione'},
        ),
        migrations.AlterField(
            model_name='spesa',
            name='img_scontrino',
            field=models.ImageField(blank=True, null=True, upload_to=RimborsiApp.models.profile_type_path),
        ),
    ]