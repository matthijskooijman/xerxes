# Generated by Django 2.2.12 on 2020-04-13 21:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Series',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('url', models.CharField(max_length=100, verbose_name='Url')),
                ('email', models.CharField(max_length=100, verbose_name='E-mail address of game masters / organisation')),
            ],
            options={
                'verbose_name': 'series',
                'verbose_name_plural': 'series',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of the event. Unique if this is a oneshot, name of the series plus a number if part of a series. Do not forget the X when this is your only title.', max_length=100, verbose_name='Name')),
                ('title', models.CharField(blank=True, help_text='Actual subtitle when within series. Do not forget the X if the name does not contain it.', max_length=100, verbose_name='Title')),
                ('description', models.TextField(blank=True, help_text='Event details like what is included or not', verbose_name='Description')),
                ('start_date', models.DateField(verbose_name='Start date')),
                ('end_date', models.DateField(verbose_name='End date')),
                ('url', models.CharField(blank=True, help_text='Can be left blank if event is part of a series, then value of series will be used.', max_length=100, verbose_name='Url')),
                ('email', models.CharField(blank=True, help_text='Can be left blank if event is part of a series, then value of series will be used.', max_length=100, verbose_name='E-mail address of game masters / organisation')),
                ('location_name', models.CharField(blank=True, help_text='Name of the location, will be used as link text if url is also available', max_length=100, verbose_name='Location name')),
                ('location_url', models.CharField(blank=True, help_text='Url of location website', max_length=100, verbose_name='Location url')),
                ('location_info', models.TextField(blank=True, help_text='Address and additional information about the location', verbose_name='Location information')),
                ('registration_opens_at', models.DateTimeField(blank=True, help_text='At this time registration is open for everyone.', null=True, verbose_name='Registration opens at')),
                ('public', models.BooleanField(default=False, help_text='When checked, the event is visible to users. If registration is not open yet, they can prepare a registration already.', verbose_name='Public')),
                ('slots', models.IntegerField(blank=True, help_text='Maximum number of attendees for this event. If omitted, no there is no limit.', null=True)),
                ('full', models.BooleanField(default=False)),
                ('series', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='events.Series', verbose_name='Series this event is part of')),
            ],
            options={
                'verbose_name': 'event',
                'verbose_name_plural': 'events',
            },
        ),
    ]
