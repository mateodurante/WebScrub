# Generated by Django 3.2.12 on 2022-02-11 18:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('asn', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Netblock',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('network', models.CharField(max_length=15)),
                ('mask', models.IntegerField()),
                ('asn', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asn.asn')),
            ],
        ),
    ]
