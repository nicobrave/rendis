# Generated by Django 5.1.2 on 2024-10-21 15:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rendiciones', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rendicion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen_factura', models.ImageField(upload_to='rendiciones/')),
                ('fecha_subida', models.DateTimeField(auto_now_add=True)),
                ('google_sheets_url', models.URLField()),
                ('google_sheets_sheet', models.CharField(max_length=100)),
                ('jefe_obra', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]