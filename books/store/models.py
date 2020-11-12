from django.contrib.auth.models import User
from django.db import models


class Book(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Цена")
    author_name = models.CharField(max_length=255, verbose_name="Имя Автора(ов)", default='')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Владелец",
                              related_name="my_books")
    readers = models.ManyToManyField(User, through='UserBookRelation', verbose_name="Читатели", related_name="books")
    rating = models.DecimalField(max_digits=3, decimal_places=2, verbose_name="рейтинг", default=None, null=True)

    def __str__(self):
        return f'ID {self.id}: {self.name}'


class UserBookRelation(models.Model):
    RATE_CHOICES = (
        (1, 'Ok'),
        (2, 'Fire'),
        (3, 'Good'),
        (4, 'Amazing'),
        (5, 'Incredible')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="Книга")
    like = models.BooleanField(default=False, verbose_name="Лайк")
    in_bookmarks = models.BooleanField(default=False, verbose_name="В закладках")
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES, verbose_name="Рейтинг", null=True)

    def save(self, *args, **kwargs):
        from store.logic import set_rating

        creating = not self.pk
        old_rating = self.rate

        super().save(*args, **kwargs)

        new_rating = self.rate
        if old_rating != new_rating or creating:
            set_rating(self.book)
