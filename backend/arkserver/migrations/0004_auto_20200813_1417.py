# Generated by Django 2.2 on 2020-08-13 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arkserver', '0003_ubung4'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ubung4',
            name='row0',
        ),
        migrations.AddField(
            model_name='ubung4',
            name='row0',
            field=models.ManyToManyField(blank=True, null=True, related_name='row0', to='arkserver.Player'),
        ),
        migrations.RemoveField(
            model_name='ubung4',
            name='row1',
        ),
        migrations.AddField(
            model_name='ubung4',
            name='row1',
            field=models.ManyToManyField(blank=True, null=True, related_name='row1', to='arkserver.Player'),
        ),
        migrations.RemoveField(
            model_name='ubung4',
            name='row2',
        ),
        migrations.AddField(
            model_name='ubung4',
            name='row2',
            field=models.ManyToManyField(blank=True, null=True, related_name='row2', to='arkserver.Player'),
        ),
        migrations.RemoveField(
            model_name='ubung4',
            name='row3',
        ),
        migrations.AddField(
            model_name='ubung4',
            name='row3',
            field=models.ManyToManyField(blank=True, null=True, related_name='row3', to='arkserver.Player'),
        ),
        migrations.RemoveField(
            model_name='ubung4',
            name='row4',
        ),
        migrations.AddField(
            model_name='ubung4',
            name='row4',
            field=models.ManyToManyField(blank=True, null=True, related_name='row4', to='arkserver.Player'),
        ),
        migrations.RemoveField(
            model_name='ubung4',
            name='row5',
        ),
        migrations.AddField(
            model_name='ubung4',
            name='row5',
            field=models.ManyToManyField(blank=True, null=True, related_name='row5', to='arkserver.Player'),
        ),
    ]
