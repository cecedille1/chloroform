# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-13 08:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alternative',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=1000)),
                ('value', models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Configuration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.SlugField(default='default', max_length=255, unique=True)),
                ('target', models.CharField(help_text='An email or a list of emails separated by ;', max_length=2000, verbose_name='Recipient of mails sent with this configuration')),
                ('success_message', models.TextField(blank=True, help_text='This message is shown to the user after he/she uses the contact form', verbose_name='Success message')),
                ('subject', models.CharField(default='Contact on {{site}}', help_text='Subject of the mail sent to the target', max_length=1000, verbose_name='Subject')),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('message', models.TextField(verbose_name='Message')),
                ('configuration', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chloroform.Configuration')),
            ],
            options={
                'verbose_name': 'Contact',
                'verbose_name_plural': 'Contacts',
            },
        ),
        migrations.CreateModel(
            name='ContactMetadata',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('value', models.TextField(blank=True)),
                ('contact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='metadatas', to='chloroform.Contact')),
            ],
        ),
        migrations.CreateModel(
            name='Metadata',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.SlugField(max_length=255, verbose_name='Name of the field in the HTML')),
                ('verbose_name', models.CharField(max_length=255, verbose_name='Name shown to the user')),
                ('description', models.TextField(blank=True, verbose_name='Description or help text shown to the user')),
                ('type', models.CharField(choices=[('name', 'Nom'), ('phone', 'Phone'), ('address', 'Address'), ('email', 'Email'), ('bool', 'Boolean'), ('text', 'Text'), ('message', 'Message'), ('alternative', 'Choice')], max_length=100, verbose_name='Type of metadata, set the validation and the HTML field')),
            ],
        ),
        migrations.CreateModel(
            name='Requirement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('required', models.BooleanField(default=False)),
                ('configuration', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requirements', to='chloroform.Configuration')),
                ('metadata', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chloroform.Metadata')),
            ],
        ),
        migrations.AddField(
            model_name='alternative',
            name='metadata',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='alternatives', to='chloroform.Metadata'),
        ),
        migrations.AlterUniqueTogether(
            name='requirement',
            unique_together=set([('metadata', 'configuration')]),
        ),
    ]
