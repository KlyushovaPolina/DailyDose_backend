# Generated by Django 5.2 on 2025-05-04 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_remove_user_photo_alter_medicationintake_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificationsettings',
            name='id',
            field=models.CharField(editable=False, max_length=20, primary_key=True, serialize=False),
        ),
    ]
