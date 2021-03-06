# Generated by Django 4.0.4 on 2022-05-27 13:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('car_model', models.CharField(max_length=255)),
                ('rent_cost_per_day', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='RentalDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_f_name', models.CharField(max_length=255)),
                ('client_l_name', models.CharField(max_length=255)),
                ('company_title', models.CharField(max_length=255)),
                ('rent_date_from', models.DateTimeField()),
                ('rent_date_to', models.DateTimeField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.car')),
            ],
        ),
    ]
