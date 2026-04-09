from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0016_inventarioherramienta_estado'),
    ]

    operations = [
        migrations.AddField(
            model_name='rol',
            name='permissions',
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AddField(
            model_name='usuario',
            name='extra_permissions',
            field=models.JSONField(blank=True, default=dict),
        ),
    ]
