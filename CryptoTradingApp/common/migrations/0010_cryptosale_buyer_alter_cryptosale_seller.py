# Generated by Django 4.1.4 on 2022-12-11 19:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("common", "0009_cryptopurchase_cryptosale_cryptotrade_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="cryptosale",
            name="buyer",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.RESTRICT,
                related_name="buyer",
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="cryptosale",
            name="seller",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.RESTRICT,
                related_name="seller",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]