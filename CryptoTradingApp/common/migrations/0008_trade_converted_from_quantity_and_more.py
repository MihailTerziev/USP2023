# Generated by Django 4.1.4 on 2022-12-11 16:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("common", "0007_rename_payment_method_balanceincrease_transaction_method"),
    ]

    operations = [
        migrations.AddField(
            model_name="trade",
            name="converted_from_quantity",
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="trade",
            name="converted_to_quantity",
            field=models.FloatField(
                default=1, validators=[django.core.validators.MinValueValidator(1e-07)]
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="balanceincrease",
            name="transaction_method",
            field=models.CharField(
                choices=[
                    ("crypto_wallet", "Crypto wallet balance"),
                    ("mobile_payment", "Mobile payment"),
                    ("bank_transfer", "Electronic bank transfer"),
                    ("credit_card", "Credit Card"),
                    ("debit_card", "Debit Card"),
                    ("paypal", "PayPal"),
                ],
                max_length=14,
            ),
        ),
        migrations.AlterField(
            model_name="purchase",
            name="currency",
            field=models.CharField(
                choices=[
                    ("TomatoCoin", "TomatoCoin"),
                    ("Ethereum", "Ethereum"),
                    ("Dogecoin", "Dogecoin"),
                    ("Bitcoin", "Bitcoin"),
                ],
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="purchase",
            name="payment_method",
            field=models.CharField(
                choices=[
                    ("crypto_wallet", "Crypto wallet balance"),
                    ("mobile_payment", "Mobile payment"),
                    ("bank_transfer", "Electronic bank transfer"),
                    ("credit_card", "Credit Card"),
                    ("debit_card", "Debit Card"),
                    ("paypal", "PayPal"),
                ],
                max_length=14,
            ),
        ),
        migrations.AlterField(
            model_name="trade",
            name="traded_currency_one",
            field=models.CharField(
                choices=[
                    ("TomatoCoin", "TomatoCoin"),
                    ("Ethereum", "Ethereum"),
                    ("Dogecoin", "Dogecoin"),
                    ("Bitcoin", "Bitcoin"),
                ],
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="trade",
            name="traded_currency_two",
            field=models.CharField(
                choices=[
                    ("TomatoCoin", "TomatoCoin"),
                    ("Ethereum", "Ethereum"),
                    ("Dogecoin", "Dogecoin"),
                    ("Bitcoin", "Bitcoin"),
                ],
                max_length=20,
            ),
        ),
    ]