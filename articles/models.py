from django.db import models
import datetime
from django.utils import timezone

class Article(models.Model):
    article_title = models.CharField('название статьи', max_length=200)
    author_name = models.CharField('имя автора', max_length=50, default='anon')
    article_text = models.TextField('текст статьи')
    pub_date = models.DateTimeField('дата публикации', default = timezone.now())


    def __str__(self):
        return self.article_title


    def was_published_recently(self):
        return self.pub_date >= (timezone.now() - datetime.timedelta(days=7))


    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    author_name = models.CharField('имя автора', max_length=50, default = 'anon')
    comment_text = models.CharField('текст комментария', max_length=200)
    pub_date = models.DateTimeField('дата публикации', default=timezone.now())

    def __str__(self):
        return self.author_name

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

