from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Instructor


@receiver(post_delete, sender=User)
def delete_instructor_on_user_delete(sender, instance, **kwargs):
    if hasattr(instance, "instructor") and not instance.instructor._is_deleting:
        instance.instructor._is_deleting = True
        instance.instructor.delete()


@receiver(post_delete, sender=Instructor)
def delete_related_user(sender, instance, **kwargs):
    """
    Elimina el usuario relacionado cuando se elimina un Instructor.
    """
    if instance.user and not instance._is_deleting:
        instance._is_deleting = True
        instance.user.delete()
