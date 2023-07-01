from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, post_delete
from django.dispatch import Signal
from django.dispatch import receiver

email_changed = Signal()
password_changed = Signal()


@receiver(post_save, sender=get_user_model(), dispatch_uid="send user email verification link")
def send_email_verification_link(sender, instance, created=False, **kwargs):
    if created:
        instance.send_email_confirmation_link()


@receiver(post_delete, sender=get_user_model(), dispatch_uid="delete user avatar from storage")
def delete_avatar(sender, instance, **kwargs):
    instance.avatar.delete(False)


@receiver([email_changed, password_changed], sender=get_user_model(), dispatch_uid="revoke all user tokens")
def revoke_tokens(sender, instance, **kwargs):
    for token in instance.tokens.all():
        token.revoke()
