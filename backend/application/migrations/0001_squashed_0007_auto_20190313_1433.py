# Generated by Django 2.1.7 on 2019-03-23 15:12

import application.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [("hacker", "0001_initial")]

    operations = [
        migrations.CreateModel(
            name="Application",
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
                ("phone", models.CharField(max_length=20, null=True)),
                (
                    "gender",
                    models.CharField(
                        choices=[
                            ("M", "Masculino"),
                            ("F", "Feminino"),
                            ("O", "Outro"),
                            ("NA", "Prefiro não dizer"),
                        ],
                        max_length=2,
                    ),
                ),
                (
                    "age",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(
                                5, "A idade mínima é 5 anos."
                            )
                        ]
                    ),
                ),
                (
                    "enroll_year",
                    models.IntegerField(
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(
                                1900, "Hmm, como?"
                            ),
                            django.core.validators.MaxValueValidator(
                                2020, "Hmm, como?"
                            ),
                        ],
                    ),
                ),
                (
                    "cv_type",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("LI", "LinkedIn"),
                            ("GH", "GitHub"),
                            ("WS", "Website"),
                            ("UP", "Upload"),
                            ("OT", "Outro"),
                        ],
                        max_length=3,
                        null=True,
                    ),
                ),
                ("cv", models.CharField(blank=True, max_length=300, null=True)),
                (
                    "cv2_type",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("LI", "LinkedIn"),
                            ("GH", "GitHub"),
                            ("WS", "Website"),
                            ("OT", "Outro"),
                        ],
                        max_length=3,
                        null=True,
                    ),
                ),
                ("cv2", models.CharField(blank=True, max_length=300, null=True)),
                (
                    "hacker",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to="hacker.Hacker"
                    ),
                ),
                ("can_move", models.BooleanField(blank=True, default=False)),
                ("city", models.CharField(blank=True, max_length=200, null=True)),
                (
                    "country",
                    models.CharField(
                        blank=True,
                        choices=[
                            ["Afeganistão", "Afeganistão"],
                            ["África do Sul", "África do Sul"],
                            ["Albânia", "Albânia"],
                            ["Alemanha", "Alemanha"],
                            ["Andorra", "Andorra"],
                            ["Angola", "Angola"],
                            ["Anguilla", "Anguilla"],
                            ["Antártida", "Antártida"],
                            ["Antígua & Barbuda", "Antígua & Barbuda"],
                            ["Arábia Saudita", "Arábia Saudita"],
                            ["Argélia", "Argélia"],
                            ["Argentina", "Argentina"],
                            ["Armênia", "Armênia"],
                            ["Aruba", "Aruba"],
                            ["Austrália", "Austrália"],
                            ["Áustria", "Áustria"],
                            ["Azerbaijão", "Azerbaijão"],
                            ["Bahamas", "Bahamas"],
                            ["Bahrein", "Bahrein"],
                            ["Bangladesh", "Bangladesh"],
                            ["Barbados", "Barbados"],
                            ["Belarus", "Belarus"],
                            ["Bélgica", "Bélgica"],
                            ["Belize", "Belize"],
                            ["Benin", "Benin"],
                            ["Bermudas", "Bermudas"],
                            ["Bolívia", "Bolívia"],
                            [
                                "Bonaire, St. Eustatius & Saba",
                                "Bonaire, St. Eustatius & Saba",
                            ],
                            ["Bósnia-Herzegovina", "Bósnia-Herzegovina"],
                            ["Botsuana", "Botsuana"],
                            ["Brasil", "Brasil"],
                            ["Brunei", "Brunei"],
                            ["Bulgária", "Bulgária"],
                            ["Burkina Faso", "Burkina Faso"],
                            ["Burundi", "Burundi"],
                            ["Butão", "Butão"],
                            ["Cabo Verde", "Cabo Verde"],
                            ["Camarões", "Camarões"],
                            ["Camboja", "Camboja"],
                            ["Canadá", "Canadá"],
                            ["Cazaquistão", "Cazaquistão"],
                            ["Chade", "Chade"],
                            ["Chile", "Chile"],
                            ["China", "China"],
                            ["Chipre", "Chipre"],
                            ["Cingapura", "Cingapura"],
                            ["Colômbia", "Colômbia"],
                            ["Congo", "Congo"],
                            ["Coréia do Norte", "Coréia do Norte"],
                            ["Coréia do Sul", "Coréia do Sul"],
                            ["Costa do Marfim", "Costa do Marfim"],
                            ["Costa Rica", "Costa Rica"],
                            ["Croácia", "Croácia"],
                            ["Cuba", "Cuba"],
                            ["Curaçao", "Curaçao"],
                            ["Dinamarca", "Dinamarca"],
                            ["Djibuti", "Djibuti"],
                            ["Dominica", "Dominica"],
                            ["Egito", "Egito"],
                            ["El Salvador", "El Salvador"],
                            ["Emirados Árabes Unidos", "Emirados Árabes Unidos"],
                            ["Equador", "Equador"],
                            ["Eritréia", "Eritréia"],
                            ["Eslováquia", "Eslováquia"],
                            ["Eslovênia", "Eslovênia"],
                            ["Espanha", "Espanha"],
                            ["Estados Unidos", "Estados Unidos"],
                            ["Estônia", "Estônia"],
                            ["Etiópia", "Etiópia"],
                            ["Federação Russa", "Federação Russa"],
                            ["Fiji", "Fiji"],
                            ["Filipinas", "Filipinas"],
                            ["Finlândia", "Finlândia"],
                            ["França", "França"],
                            ["Gabão", "Gabão"],
                            ["Gâmbia", "Gâmbia"],
                            ["Gana", "Gana"],
                            ["Geórgia", "Geórgia"],
                            ["Gibraltar", "Gibraltar"],
                            [
                                "Grã-Bretanha (Reino Unido)",
                                "Grã-Bretanha (Reino Unido)",
                            ],
                            ["Granada", "Granada"],
                            ["Grécia", "Grécia"],
                            ["Groelândia", "Groelândia"],
                            ["Guadalupe", "Guadalupe"],
                            [
                                "Guam (Território dos Estados Unidos)",
                                "Guam (Território dos Estados Unidos)",
                            ],
                            ["Guatemala", "Guatemala"],
                            ["G|Guernsey", "G|Guernsey"],
                            ["Guiana", "Guiana"],
                            ["Guiana Francesa", "Guiana Francesa"],
                            ["Guiné", "Guiné"],
                            ["Guiné Equatorial", "Guiné Equatorial"],
                            ["Guiné-Bissau", "Guiné-Bissau"],
                            ["Haiti", "Haiti"],
                            ["Holanda", "Holanda"],
                            ["Honduras", "Honduras"],
                            ["Hong-Kong", "Hong-Kong"],
                            ["Hungria", "Hungria"],
                            ["Iêmen", "Iêmen"],
                            [
                                "Ilha Bouvet (Território da Noruega)",
                                "Ilha Bouvet (Território da Noruega)",
                            ],
                            ["Ilha do Homem", "Ilha do Homem"],
                            ["Ilha Natal", "Ilha Natal"],
                            ["Ilha Pitcairn", "Ilha Pitcairn"],
                            ["Ilha Reunião", "Ilha Reunião"],
                            ["Ilhas Aland", "Ilhas Aland"],
                            ["Ilhas Cayman", "Ilhas Cayman"],
                            ["Ilhas Cocos", "Ilhas Cocos"],
                            ["Ilhas Comores", "Ilhas Comores"],
                            ["Ilhas Cook", "Ilhas Cook"],
                            ["Ilhas Faroes", "Ilhas Faroes"],
                            ["Ilhas Falkland (Malvinas)", "Ilhas Falkland (Malvinas)"],
                            [
                                "Ilhas Geórgia do Sul e Sandwich do Sul",
                                "Ilhas Geórgia do Sul e Sandwich do Sul",
                            ],
                            [
                                "Ilhas Heard e McDonald (Território da Austrália)",
                                "Ilhas Heard e McDonald (Território da Austrália)",
                            ],
                            ["Ilhas Marianas do Norte", "Ilhas Marianas do Norte"],
                            ["Ilhas Marshall", "Ilhas Marshall"],
                            [
                                "Ilhas Menores dos Estados Unidos",
                                "Ilhas Menores dos Estados Unidos",
                            ],
                            ["Ilhas Norfolk", "Ilhas Norfolk"],
                            ["Ilhas Seychelles", "Ilhas Seychelles"],
                            ["Ilhas Solomão", "Ilhas Solomão"],
                            [
                                "Ilhas Svalbard & Jan Mayen",
                                "Ilhas Svalbard & Jan Mayen",
                            ],
                            ["Ilhas Tokelau", "Ilhas Tokelau"],
                            ["Ilhas Turks e Caicos", "Ilhas Turks e Caicos"],
                            [
                                "Ilhas Virgens (Estados Unidos)",
                                "Ilhas Virgens (Estados Unidos)",
                            ],
                            [
                                "Ilhas Virgens (Inglaterra)",
                                "Ilhas Virgens (Inglaterra)",
                            ],
                            ["Ilhas Wallis & Futuna", "Ilhas Wallis & Futuna"],
                            ["Índia", "Índia"],
                            ["Indonésia", "Indonésia"],
                            ["Irã", "Irã"],
                            ["Iraque", "Iraque"],
                            ["Irlanda", "Irlanda"],
                            ["Islândia", "Islândia"],
                            ["Israel", "Israel"],
                            ["Itália", "Itália"],
                            ["Jamaica", "Jamaica"],
                            ["Japão", "Japão"],
                            ["Jersey", "Jersey"],
                            ["Jordânia", "Jordânia"],
                            ["Kiribati", "Kiribati"],
                            ["Kuait", "Kuait"],
                            ["Laos", "Laos"],
                            ["Látvia", "Látvia"],
                            ["Lesoto", "Lesoto"],
                            ["Líbano", "Líbano"],
                            ["Libéria", "Libéria"],
                            ["Líbia", "Líbia"],
                            ["Liechtenstein", "Liechtenstein"],
                            ["Lituânia", "Lituânia"],
                            ["Luxemburgo", "Luxemburgo"],
                            ["Macau", "Macau"],
                            [
                                "Macedônia (República Yugoslava)",
                                "Macedônia (República Yugoslava)",
                            ],
                            ["Madagascar", "Madagascar"],
                            ["Malásia", "Malásia"],
                            ["Malaui", "Malaui"],
                            ["Maldivas", "Maldivas"],
                            ["Mali", "Mali"],
                            ["Malta", "Malta"],
                            ["Marrocos", "Marrocos"],
                            ["Martinica", "Martinica"],
                            ["Maurício", "Maurício"],
                            ["Mauritânia", "Mauritânia"],
                            ["Mayotte", "Mayotte"],
                            ["México", "México"],
                            ["Micronésia", "Micronésia"],
                            ["Moçambique", "Moçambique"],
                            ["Moldova", "Moldova"],
                            ["Mônaco", "Mônaco"],
                            ["Mongólia", "Mongólia"],
                            ["Montenegro", "Montenegro"],
                            ["Montserrat", "Montserrat"],
                            ["Myanmar", "Myanmar"],
                            ["Namíbia", "Namíbia"],
                            ["Nauru", "Nauru"],
                            ["Nepal", "Nepal"],
                            ["Nicarágua", "Nicarágua"],
                            ["Níger", "Níger"],
                            ["Nigéria", "Nigéria"],
                            ["Niue", "Niue"],
                            ["Noruega", "Noruega"],
                            ["Nova Caledônia", "Nova Caledônia"],
                            ["Nova Zelândia", "Nova Zelândia"],
                            ["Omã", "Omã"],
                            ["Palau", "Palau"],
                            ["Panamá", "Panamá"],
                            ["Papua-Nova Guiné", "Papua-Nova Guiné"],
                            ["Paquistão", "Paquistão"],
                            ["Paraguai", "Paraguai"],
                            ["Peru", "Peru"],
                            ["Polinésia Francesa", "Polinésia Francesa"],
                            ["Polônia", "Polônia"],
                            ["Porto Rico", "Porto Rico"],
                            ["Portugal", "Portugal"],
                            ["Qatar", "Qatar"],
                            ["Quênia", "Quênia"],
                            ["Quirguistão", "Quirguistão"],
                            ["República Centro-Africana", "República Centro-Africana"],
                            [
                                "República Democrática do Congo",
                                "República Democrática do Congo",
                            ],
                            ["República Dominicana", "República Dominicana"],
                            ["República Tcheca", "República Tcheca"],
                            ["Romênia", "Romênia"],
                            ["Ruanda", "Ruanda"],
                            ["Saara Ocidental", "Saara Ocidental"],
                            [
                                "Saint Vincent e Granadinas",
                                "Saint Vincent e Granadinas",
                            ],
                            ["Samoa Ocidental", "Samoa Ocidental"],
                            ["Samoa Ocidental", "Samoa Ocidental"],
                            ["San Marino", "San Marino"],
                            ["Santa Helena", "Santa Helena"],
                            ["Santa Lúcia", "Santa Lúcia"],
                            ["São Bartolomeu", "São Bartolomeu"],
                            ["São Cristóvão e Névis", "São Cristóvão e Névis"],
                            ["San Martin", "San Martin"],
                            ["São Tomé e Príncipe", "São Tomé e Príncipe"],
                            ["Senegal", "Senegal"],
                            ["Sierra Leoa", "Sierra Leoa"],
                            ["Sérvia", "Sérvia"],
                            ["Síria", "Síria"],
                            ["Somália", "Somália"],
                            ["Sri Lanka", "Sri Lanka"],
                            ["St. Maarten", "St. Maarten"],
                            ["St.Pierre & Miquelon", "St.Pierre & Miquelon"],
                            ["Suazilândia", "Suazilândia"],
                            ["Sudão", "Sudão"],
                            ["Sudão do Sul", "Sudão do Sul"],
                            ["Suécia", "Suécia"],
                            ["Suíça", "Suíça"],
                            ["Suriname", "Suriname"],
                            ["Tadjiquistão", "Tadjiquistão"],
                            ["Tailândia", "Tailândia"],
                            ["Taiwan", "Taiwan"],
                            ["Tanzânia", "Tanzânia"],
                            [
                                "Território Britânico do Oceano Índico",
                                "Território Britânico do Oceano Índico",
                            ],
                            [
                                "Territórios do Sul da França",
                                "Territórios do Sul da França",
                            ],
                            [
                                "Territórios Palestinos Ocupados",
                                "Territórios Palestinos Ocupados",
                            ],
                            ["Timor Leste", "Timor Leste"],
                            ["Togo", "Togo"],
                            ["Tonga", "Tonga"],
                            ["Trinidad & Tobago", "Trinidad & Tobago"],
                            ["Tunísia", "Tunísia"],
                            ["Turcomenistão", "Turcomenistão"],
                            ["Turquia", "Turquia"],
                            ["Tuvalu", "Tuvalu"],
                            ["Ucrânia", "Ucrânia"],
                            ["Uganda", "Uganda"],
                            ["Uruguai", "Uruguai"],
                            ["Uzbequistão", "Uzbequistão"],
                            ["Vanuatu", "Vanuatu"],
                            ["Vaticano", "Vaticano"],
                            ["Venezuela", "Venezuela"],
                            ["Vietnã", "Vietnã"],
                            ["Zâmbia", "Zâmbia"],
                            ["Zimbábue", "Zimbábue"],
                        ],
                        max_length=200,
                        null=True,
                    ),
                ),
                ("course", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "cpf",
                    models.CharField(
                        default="",
                        max_length=20,
                        validators=[application.models.CPFValidator(0, "CPF inválido")],
                    ),
                ),
                (
                    "dream_company",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("education", models.CharField(default="", max_length=20)),
                (
                    "english_level",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("basic", "Básico"),
                            ("intermediate", "Intermediário"),
                            ("advanced", "Avançado"),
                        ],
                        max_length=20,
                        null=True,
                    ),
                ),
                (
                    "excel_level",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("basic", "Básico"),
                            ("intermediate", "Intermediário"),
                            ("advanced", "Avançado"),
                        ],
                        max_length=20,
                        null=True,
                    ),
                ),
                ("extra_courses", models.TextField(blank=True, null=True)),
                ("first_timer", models.BooleanField(default=True)),
                ("interests", models.CharField(default="", max_length=200)),
                (
                    "other_languages",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                ("referrer", models.CharField(default="", max_length=100)),
                ("school", models.CharField(blank=True, max_length=100, null=True)),
                ("state", models.CharField(blank=True, max_length=200, null=True)),
                ("time_slots", models.CharField(blank=True, max_length=200, null=True)),
            ],
        )
    ]
