# Generated by Django 2.1.7 on 2019-03-24 00:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [("hacker", "0004_auto_20190321_0826")]

    operations = [
        migrations.CreateModel(
            name="Checkout",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "code",
                    models.CharField(
                        blank=True,
                        help_text="Código gerado para redirecionamento.",
                        max_length=100,
                        verbose_name="código",
                    ),
                ),
                (
                    "date",
                    models.DateTimeField(
                        help_text="Data em que o checkout foi realizado.",
                        verbose_name="Data",
                    ),
                ),
                (
                    "success",
                    models.BooleanField(
                        db_index=True,
                        default=False,
                        help_text="O checkout foi feito com sucesso?",
                        verbose_name="Sucesso",
                    ),
                ),
                (
                    "message",
                    models.TextField(
                        blank=True,
                        help_text="Mensagem apresentada no caso de erro no checkout.",
                        verbose_name="Mensagem de erro",
                    ),
                ),
            ],
            options={
                "ordering": ["-date"],
                "verbose_name": "Checkout",
                "verbose_name_plural": "Checkouts",
            },
        ),
        migrations.CreateModel(
            name="Transaction",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "code",
                    models.CharField(
                        db_index=True,
                        help_text=b"O c\xc3\xb3digo da transa\xc3\xa7\xc3\xa3o.",
                        max_length=100,
                        unique=True,
                        verbose_name=b"c\xc3\xb3digo",
                    ),
                ),
                (
                    "reference",
                    models.CharField(
                        blank=True,
                        db_index=True,
                        help_text=b"A refer\xc3\xaancia passada na transa\xc3\xa7\xc3\xa3o.",
                        max_length=200,
                        verbose_name=b"refer\xc3\xaancia",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            (b"aguardando", b"Aguardando"),
                            (b"em_analise", b"Em an\xc3\xa1lise"),
                            (b"pago", b"Pago"),
                            (b"disponivel", b"Dispon\xc3\xadvel"),
                            (b"em_disputa", b"Em disputa"),
                            (b"devolvido", b"Devolvido"),
                            (b"cancelado", b"Cancelado"),
                        ],
                        db_index=True,
                        help_text=b"Status atual da transa\xc3\xa7\xc3\xa3o.",
                        max_length=20,
                        verbose_name=b"Status",
                    ),
                ),
                (
                    "date",
                    models.DateTimeField(
                        help_text=b"Data em que a transa\xc3\xa7\xc3\xa3o foi criada.",
                        verbose_name=b"Data",
                    ),
                ),
                (
                    "last_event_date",
                    models.DateTimeField(
                        help_text=b"Data da \xc3\xbaltima altera\xc3\xa7\xc3\xa3o na transa\xc3\xa7\xc3\xa3o.",
                        verbose_name=b"\xc3\x9altima altera\xc3\xa7\xc3\xa3o",
                    ),
                ),
                (
                    "content",
                    models.TextField(
                        help_text=b"Transa\xc3\xa7\xc3\xa3o no formato json.",
                        verbose_name=b"Transa\xc3\xa7\xc3\xa3o",
                    ),
                ),
            ],
            options={
                "ordering": ["-date"],
                "verbose_name": "Transação",
                "verbose_name_plural": "Transações",
            },
        ),
        migrations.CreateModel(
            name="TransactionHistory",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("aguardando", "Aguardando"),
                            ("em_analise", "Em análise"),
                            ("pago", "Pago"),
                            ("disponivel", "Disponível"),
                            ("em_disputa", "Em disputa"),
                            ("devolvido", "Devolvido"),
                            ("cancelado", "Cancelado"),
                        ],
                        help_text="Status da transação.",
                        max_length=20,
                        verbose_name="Status",
                    ),
                ),
                ("date", models.DateTimeField(verbose_name="Data")),
                (
                    "transaction",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="pagseguro.Transaction",
                        verbose_name="Transação",
                    ),
                ),
            ],
            options={
                "ordering": ["date"],
                "verbose_name": "Histórico da transação",
                "verbose_name_plural": "Históricos de transações",
            },
        ),
        migrations.AlterField(
            model_name="transaction",
            name="code",
            field=models.CharField(
                db_index=True,
                help_text="O código da transação.",
                max_length=100,
                unique=True,
                verbose_name="código",
            ),
        ),
        migrations.AlterField(
            model_name="transaction",
            name="content",
            field=models.TextField(
                help_text="Transação no formato json.", verbose_name="Transação"
            ),
        ),
        migrations.AlterField(
            model_name="transaction",
            name="date",
            field=models.DateTimeField(
                help_text="Data em que a transação foi criada.", verbose_name="Data"
            ),
        ),
        migrations.AlterField(
            model_name="transaction",
            name="last_event_date",
            field=models.DateTimeField(
                help_text="Data da última alteração na transação.",
                verbose_name="Última alteração",
            ),
        ),
        migrations.AlterField(
            model_name="transaction",
            name="reference",
            field=models.CharField(
                blank=True,
                db_index=True,
                help_text="A referência passada na transação.",
                max_length=200,
                verbose_name="referência",
            ),
        ),
        migrations.AlterField(
            model_name="transaction",
            name="status",
            field=models.CharField(
                choices=[
                    ("aguardando", "Aguardando"),
                    ("em_analise", "Em análise"),
                    ("pago", "Pago"),
                    ("disponivel", "Disponível"),
                    ("em_disputa", "Em disputa"),
                    ("devolvido", "Devolvido"),
                    ("cancelado", "Cancelado"),
                ],
                db_index=True,
                help_text="Status atual da transação.",
                max_length=20,
                verbose_name="Status",
            ),
        ),
        migrations.AddField(
            model_name="transaction",
            name="hacker",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="transactions",
                to="hacker.Hacker",
            ),
        ),
    ]