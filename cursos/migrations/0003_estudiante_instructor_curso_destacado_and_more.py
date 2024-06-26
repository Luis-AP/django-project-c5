# Generated by Django 5.0.3 on 2024-03-26 01:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cursos", "0002_categoria_curso_duracion_curso_estado_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Estudiante",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nombre", models.CharField(max_length=150)),
                ("email", models.EmailField(max_length=254, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Instructor",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nombre", models.CharField(max_length=100)),
                ("bio", models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name="curso",
            name="destacado",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="curso",
            name="requisitos",
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name="curso",
            name="categoria",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="cursos.categoria",
            ),
        ),
        migrations.AlterField(
            model_name="curso",
            name="estado",
            field=models.CharField(
                blank=True,
                choices=[
                    ("borrador", "Borrador"),
                    ("publicado", "Publicado"),
                    ("archivado", "Archivado"),
                ],
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="curso",
            name="instructor",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="cursos.instructor",
            ),
        ),
    ]
