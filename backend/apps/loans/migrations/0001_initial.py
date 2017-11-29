# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-29 13:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('amount', models.FloatField()),
                ('rate', models.FloatField()),
                ('term', models.PositiveSmallIntegerField()),
                ('date', models.DateTimeField()),
                ('balance', models.FloatField()),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('payment', models.CharField(choices=[(b'made', b'Payment as been made'), (b'missed', b'Missed payment')], max_length=5)),
                ('amount', models.FloatField()),
                ('date', models.DateTimeField()),
                ('loan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='loans.Loan')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
    ]