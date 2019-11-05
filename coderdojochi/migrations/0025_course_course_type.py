# Generated by Django 2.2.2 on 2019-07-01 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coderdojochi', '0024_session_cost'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='course_type',
            field=models.CharField(choices=[('WE', 'Weekend'), ('CA', 'Camp')], default='WE', max_length=2, verbose_name='type'),
        ),
    ]
