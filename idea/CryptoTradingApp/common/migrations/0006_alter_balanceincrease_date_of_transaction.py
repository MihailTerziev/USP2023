# Generated by Django 4.1.4 on 2022-12-09 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("common", "0005_alter_balanceincrease_amount"),
    ]

    operations = [
        migrations.AlterField(
            model_name="balanceincrease",
            name="date_of_transaction",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]