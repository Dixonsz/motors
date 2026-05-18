from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("agenda", "0003_configuracion_horario_laboral"),
    ]

    operations = [
        migrations.AlterField(
            model_name="configuracioncalendario",
            name="fecha_inicio",
            field=models.DateField(blank=True, null=True),
        ),
    ]
