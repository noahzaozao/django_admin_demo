from django.db import models
from django.contrib.auth.models import User, UserManager


class Origin(models.Model):
    origin_name = models.CharField(
        default='',
        max_length=50,
        verbose_name='渠道名称'
    )
    user = models.ForeignKey(
        "DemoUser",
        on_delete=models.SET_NULL,
        verbose_name="渠道所属用户",
        null=True,
        blank=True,
        related_name='origins'
    )

    class Meta:
        verbose_name = "渠道"
        verbose_name_plural = "渠道管理 - (Origin)"

    def __str__(self):
        return self.origin_name


class DemoUser(User):

    origin = models.ForeignKey(
        'Origin',
        default=None,
        null=True,
        verbose_name='渠道来源',
        related_name='users'
    )

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = "用户管理 - (DemoUser)"

    def __str__(self):
        return self.username
