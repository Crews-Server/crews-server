from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from table.models import Apply


@receiver(post_save, sender=Apply)
def update_applicants_count_on_apply(sender, instance, created, **kwargs):
    if created:
        instance.post.applicants_count += 1
        instance.post.save(update_fields=['applicants_count'])

@receiver(post_delete, sender=Apply)
def update_applicants_count_on_unapply(sender, instance, **kwargs):
    instance.post.applicants_count -= 1
    instance.post.save(update_fields=['applicants_count'])