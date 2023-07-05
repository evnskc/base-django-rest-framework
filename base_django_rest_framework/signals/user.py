from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import Signal
from django.dispatch import receiver

email_changed = Signal()
password_changed = Signal()


@receiver(post_save, sender=get_user_model(), dispatch_uid="send user email verification link")
def send_email_verification_link(sender, instance, created=False, **kwargs):
    if created:
        instance.send_email_confirmation_link()


@receiver(pre_save, sender=get_user_model(), dispatch_uid="delete user orphaned avatar from storage")
def delete_orphaned_avatar(sender, instance, **kwargs):
    try:
        with get_user_model().objects.get(id=instance.id).avatar as old_avatar:
            if instance.avatar != old_avatar:
                old_avatar.delete(False)
    except get_user_model().DoesNotExist:
        return


@receiver(post_delete, sender=get_user_model(), dispatch_uid="delete user avatar from storage")
def delete_avatar(sender, instance, **kwargs):
    instance.avatar.delete(False)


@receiver([email_changed, password_changed], sender=get_user_model(), dispatch_uid="revoke all user tokens")
def revoke_tokens(sender, instance, **kwargs):
    for token in instance.tokens.all():
        token.revoke()
