# Generated by Django 5.1.6 on 2025-03-03 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("portal", "0008_alter_workerinthefarmtbl_additional_tasks_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="workerinthefarmtbl",
            name="additional_tasks",
            field=models.CharField(
                choices=[("01", "Yes"), ("02", "No")],
                verbose_name="Does the worker perform tasks for you or your family members other than those agreed upon?",
            ),
        ),
        migrations.AlterField(
            model_name="workerinthefarmtbl",
            name="recruited_workers",
            field=models.CharField(
                choices=[("01", "Yes"), ("02", "No")],
                verbose_name="Have you recruited at least one worker during the past year?",
            ),
        ),
        migrations.AlterField(
            model_name="workerinthefarmtbl",
            name="tasks_clarified",
            field=models.CharField(
                choices=[("01", "Yes"), ("02", "No")],
                verbose_name="Were the tasks to be performed by the worker clarified during recruitment?",
            ),
        ),
    ]
