# Generated by Django 4.1.11 on 2024-10-06 08:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0002_rename_case_appointment_caseinfo'),
        ('healthrecord', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='healthrecord',
            name='appointment',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='appointment.appointment'),
            preserve_default=False,
        ),
    ]
