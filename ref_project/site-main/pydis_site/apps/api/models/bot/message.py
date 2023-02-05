import datetime

from django.contrib.postgres import fields as pgfields
from django.core.validators import MinValueValidator
from django.db import models

from pydis_site.apps.api.models.bot.user import User
from pydis_site.apps.api.models.mixins import ModelReprMixin


class Message(ModelReprMixin, models.Model):
    """A message, sent somewhere on the Discord server."""

    id = models.BigIntegerField(
        primary_key=True,
        help_text="The message ID as taken from Discord.",
        validators=(
            MinValueValidator(
                limit_value=0,
                message="Message IDs cannot be negative."
            ),
        ),
        verbose_name="ID"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text="The author of this message."
    )
    channel_id = models.BigIntegerField(
        help_text=(
            "The channel ID that this message was "
            "sent in, taken from Discord."
        ),
        validators=(
            MinValueValidator(
                limit_value=0,
                message="Channel IDs cannot be negative."
            ),
        ),
        verbose_name="Channel ID"
    )
    content = models.CharField(
        max_length=4_000,
        help_text="The content of this message, taken from Discord.",
        blank=True
    )
    embeds = pgfields.ArrayField(
        models.JSONField(),
        blank=True,
        help_text="Embeds attached to this message."
    )
    attachments = pgfields.ArrayField(
        models.URLField(
            max_length=512
        ),
        blank=True,
        help_text="Attachments attached to this message."
    )

    @property
    def timestamp(self) -> datetime.datetime:
        """Attribute that represents the message timestamp as derived from the snowflake id."""
        return datetime.datetime.utcfromtimestamp(
            ((self.id >> 22) + 1420070400000) / 1000
        ).replace(tzinfo=datetime.timezone.utc)

    class Meta:
        """Metadata provided for Django's ORM."""

        abstract = True
