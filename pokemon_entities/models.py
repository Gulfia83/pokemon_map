from django.db import models  # noqa F401

class PokemonElementType(models.Model):
    title = models.CharField(max_length=200,
                             verbose_name='Стихии')
    img = models.ImageField(null=True,
                            blank=True,
                            verbose_name='Изображение стихии')
    strong_against = models.ManyToManyField("self",
                                            symmetrical=False,
                                            verbose_name='Силен против',
                                            null=True,
                                            blank=True)
    
    def __str__(self):
        return self.title
    

class Pokemon(models.Model):
    title = models.CharField(max_length=200,
                             verbose_name='Название покемона')
    title_en = models.CharField(max_length=200,
                                verbose_name='Название покемона на английском', 
                                null=True,
                                blank=True)
    title_jp = models.CharField(max_length=200,
                                verbose_name='Название покемона на японском', 
                                null=True,
                                blank=True)
    photo = models.ImageField(null=True,
                              blank=True,
                              upload_to='pokemons',
                              verbose_name='Изображение покемона')
    description = models.TextField(verbose_name='Описание покемона',
                                   null=True,
                                   blank=True)
    previous_evolution = models.ForeignKey("self",
                                           on_delete=models.SET_NULL,
                                           null=True,
                                           blank=True,
                                           verbose_name='Из кого эволюционировал',
                                           related_name='next_evolutions')
    element_type = models.ManyToManyField(PokemonElementType)
    
    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon,
                                on_delete=models.CASCADE,
                                verbose_name='Покемон',
                                related_name='entities')
    lat = models.FloatField(verbose_name='Широта',
                            null=True)
    lon = models.FloatField(verbose_name='Долгота',
                            null=True)
    appeared_at = models.DateTimeField(verbose_name='Появился',
                                       null=True,
                                       blank=True)
    disappeared_at = models.DateTimeField(verbose_name='Исчез',
                                          null=True,
                                          blank=True)
    level = models.IntegerField(verbose_name='Уровень',
                                null=True,
                                blank=True)
    health = models.IntegerField(verbose_name='Здоровье',
                                 null=True,
                                 blank=True)
    strength = models.IntegerField(verbose_name='Сила',
                                   null=True,
                                   blank=True)
    defense = models.IntegerField(verbose_name='Защита',
                                  null=True,
                                  blank=True)
    stamina = models.IntegerField(verbose_name='Выносливость',
                                  null=True,
                                  blank=True)

    def __str__(self):
        return self.pokemon.title
    

