from django.db import models

from authors.util import AuthorUtil
from mysocial.settings import base


class Follow(models.Model):
    """
    actor follows target
    """
    FIELD_NAME_HAS_ACCEPTED = 'hasAccepted'

    actor = models.URLField(validators=[AuthorUtil.validate_author_url], max_length=1000)
    target = models.URLField(validators=[AuthorUtil.validate_author_url], max_length=1000)
    has_accepted = models.BooleanField(default=False)

    """
    remote_url is the url pointing to a related and more authoritative Follow object
    If this is not empty, the other Follow object is our source of truth
    If this is empty, this is the source of truth and you may disregard the other object
    """
    remote_url = models.URLField(blank=True, max_length=1000)

    class Meta:
        unique_together = (('actor', 'target'),)
        get_latest_by = 'id'

    def get_local_url(self):
        """
        Returns the url to get this Follow object
        """
        return f"http://{base.CURRENT_DOMAIN}/follows/{self.id}"

    @staticmethod
    def get_serializer_field_name():
        return "Follow"

    def __str__(self):
        actor, _ = AuthorUtil.from_author_url_to_author(self.actor)
        actor_name = ""
        if actor is not None:
            actor_name = str(actor)
        target, _ = AuthorUtil.from_author_url_to_author(self.target)
        target_name = ""
        if target is not None:
            target_name = str(target)
        status = 'follows' if self.has_accepted else 'wants to follow'
        return f'{actor_name} {status} {target_name}'
