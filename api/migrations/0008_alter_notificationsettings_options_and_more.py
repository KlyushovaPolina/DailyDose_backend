# Generated by Django 5.2 on 2025-05-05 23:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_medication_instructions'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notificationsettings',
            options={'verbose_name': 'Notification Settings', 'verbose_name_plural': 'Notification Settings'},
        ),
        migrations.AlterField(
            model_name='medicationintake',
            name='medication',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='intakes', to='api.medication'),
        ),
        migrations.AlterField(
            model_name='medicationintake',
            name='schedule',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='intakes', to='api.medicationschedule'),
        ),
    ]
