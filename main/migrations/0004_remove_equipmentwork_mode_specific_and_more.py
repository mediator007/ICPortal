# Generated by Django 4.0.2 on 2022-03-05 06:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_remove_mode_characters_equipmentwork_mode_specific'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='equipmentwork',
            name='mode_specific',
        ),
        migrations.AlterField(
            model_name='equipmentwork',
            name='line_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='main.line', verbose_name='Испытание'),
        ),
    ]
