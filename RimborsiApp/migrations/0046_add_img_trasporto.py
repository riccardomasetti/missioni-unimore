# Generated by Django 2.2.3 on 2024-07-13 09:42

import RimborsiApp.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RimborsiApp', '0045_enable_blank_italian_profile_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='trasporto',
            name='img_scontrino',
            field=models.ImageField(blank=True, null=True, upload_to='trasporti/'),
        ),
    ]