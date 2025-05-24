from django.db import models
from django.core.validators import FileExtensionValidator, MaxValueValidator


class Feedback(models.Model):
    FEEDBACK_TYPES = [
        ('wish', 'Пожелание'),
        ('problem', 'Проблема'),
        ('complaint', 'Претензия'),
        ('other', 'Другое'),
    ]

    feedback_type = models.CharField(
        max_length=20,
        choices=FEEDBACK_TYPES,
        verbose_name='Тип обращения'
    )
    description = models.TextField(verbose_name='Описание')
    attachment = models.FileField(
        upload_to='feedback_attachments/',
        null=True,
        blank=True,
        verbose_name='Прикрепленный файл',
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png']),
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратная связь'

    def __str__(self):
        return f'{self.get_feedback_type_display()} от {self.created_at.strftime("%d.%m.%Y %H:%M")}'