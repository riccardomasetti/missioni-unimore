# Generated by Django 2.2.3 on 2019-07-26 07:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comuni_italiani', '0001_initial'),
        ('RimborsiApp', '0027_add_indirizzo_in_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='luogo_nascita_2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='comuni_italiani.Comune'),
        ),
    ]