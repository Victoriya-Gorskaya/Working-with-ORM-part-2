from django.db import models
import datetime


class Article(models.Model):

    title = models.CharField(max_length=256, verbose_name='Название')
    text = models.TextField(verbose_name='Текст')
    published_at = models.DateTimeField(verbose_name='Дата публикации')
    image = models.ImageField(null=True, blank=True, verbose_name='Изображение')
    sections = models.ManyToManyField('Section', related_name='articles', blank=True, through='ArticleSection')
    main_section = models.ForeignKey('Section', on_delete=models.CASCADE, related_name='main_articles',
                                     blank=True, null=True)
    objects = models.Manager()

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-id']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.published_at:
            self.published_at = datetime.datetime.now()
        super().save(*args, **kwargs)


class Section(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'
        ordering = ['name']

    def __str__(self):
        return self.name


class ArticleSection(models.Model):
    article = models.ForeignKey('Article', on_delete=models.CASCADE)
    section = models.ForeignKey('Section', on_delete=models.CASCADE)
    is_main = models.BooleanField(default=False)
    objects = models.Manager()

    class Meta:
        verbose_name = 'Раздел статьи'
        verbose_name_plural = 'Разделы статьи'
        unique_together = ('article', 'section')
        ordering = ['section__name']

    def __str__(self):
        return f'{self.article} - {self.section}'

    @classmethod
    def get_sorted_sections(cls, article_id):
        return cls.objects.filter(article_id=article_id).order_by('-is_main', 'section__name')