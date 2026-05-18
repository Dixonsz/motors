from django.db import migrations, models


def default_dias_laborales():
    return [0, 1, 2, 3, 4]


class Migration(migrations.Migration):

    dependencies = [
        ("agenda", "0002_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="configuracioncalendario",
            name="dias_laborales",
            field=models.JSONField(
                blank=True,
                null=True,
                default=default_dias_laborales,
                help_text="Dias laborales (0=Lunes, 6=Domingo)",
            ),
        ),
        migrations.AlterField(
            model_name="configuracioncalendario",
            name="tipo",
            field=models.CharField(
                max_length=20,
                choices=[
                    ("dia_completo", "Día completo"),
                    ("franja", "Franja horaria"),
                    ("laboral", "Horario laboral"),
                ],
            ),
        ),
    ]
