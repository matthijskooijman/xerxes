# Generated by Django 2.2.7 on 2019-11-09 19:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registrations', '0005_auto_20191109_1356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registrationfieldvalue',
            name='registration',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='registrations.Registration'),
        ),
    ]
