# Generated by Django 3.2.5 on 2021-07-15 16:02

import coderdojochi.models.user
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import stdimage.models


class Migration(migrations.Migration):

    dependencies = [
        ('coderdojochi', '0041_auto_20210715_0957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cdcuser',
            name='avatar',
            field=stdimage.models.StdImageField(blank=True, null=True, upload_to=coderdojochi.models.user.generate_filename),
        ),
        migrations.AlterField(
            model_name='cdcuser',
            name='avatar_approved',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='cdcuser',
            name='role',
            field=models.CharField(choices=[('mentor', 'mentor'), ('guardian', 'guardian')], default='', max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='guardian',
            field=models.ForeignKey(limit_choices_to={'user__role': 'guardian'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='student',
            name='guardian',
            field=models.ForeignKey(limit_choices_to={'user__role': 'guardian'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Guardian',
        ),
    ]
