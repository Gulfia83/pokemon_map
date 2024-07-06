# Generated by Django 3.2.12 on 2024-07-05 12:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0009_pokemon_previous_evolution'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemon',
            name='previous_evolution',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pokemon_entities.pokemon', verbose_name='Из кого эволюционировал'),
        ),
    ]
