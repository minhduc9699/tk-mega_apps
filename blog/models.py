from django.db import models
from django.contrib.auth.models import User, Permission
from django.db.models.signals import post_save
from django.dispatch import receiver
from ckeditor.fields import RichTextField
from datetime import datetime
from urllib.parse import urlparse
# Create your models here.


ROLE_CHOICES = (("viewer", "Viewer"),
                ("contributor", "Contributor"),
                ("editor", "Editor"),
                ("manager", "Manager")
                )

STATE_CHOICES = (("approve", "Approve"),
                 ("approve with edit", "Approve With edit"),
                 ("not approve", "Not approve"),
                 )


class UserProfile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
  role = models.CharField(max_length=255, choices=ROLE_CHOICES, default="viewer")
  kudo = models.FloatField(default=0)

  def __str__(self):
    if self.user.first_name and self.user.last_name:
        return '%s %s' % (self.user.first_name, self.user.last_name)
    else:
        return self.user.username


class Oil(models.Model):
  date = models.DateField(default=datetime.now)
  tag = models.CharField(max_length=255)
  title = models.CharField(max_length=255)
  question = RichTextField()
  anwser = RichTextField()
  resource = models.URLField(max_length=400, blank=True, default="")
  contributor = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="contributor")
  editor = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True, related_name="editor")
  state = models.CharField(max_length=250, choices=STATE_CHOICES, default="not approve")
  kudo = models.FloatField(default=0)
  on_payroll = models.BooleanField(default=False)

  def __str__(self):
    return self.title

  def url_text(self):
    try:
      parsed_url = urlparse(self.resource)
      return parsed_url.hostname.replace("www.", "") + "/..."
    except BaseException:
      pass


class LikeOil(models.Model):
  user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_like')
  oil_like = models.ForeignKey(Oil, on_delete=models.CASCADE, related_name='oil_like')

  def __str__(self):
    return '%s like %s' % (self.user, self.oil_like)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)
    instance.userprofile.save()


@receiver(post_save, sender=Oil)
def update_user_kudo(sender, instance, created, **kwargs):
    if instance.state == "approve" or instance.state == "need edit":
      instance.contributor.kudo += instance.kudo
      instance.contributor.save()


ADMIN_PERMISSION = ['Can add oil',
                    'Can change oil',
                    'Can delete oil',
                    'Can add user profile',
                    'Can change user profile',
                    'Can delete user profile',
                    ]

MANAGER_PERMISSION = ['Can add oil',
                      'Can change oil',
                      'Can delete oil',
                      'Can change user profile',
                      ]

EDITOR_PERMISSION = ['Can add oil',
                     'Can change oil',
                     'Can delete oil',
                     ]

CONTRIBUTOR_PERMISSION = ['Can add oil']


def set_user_permiss(instance, role_permission):
     for permiss in role_permission:
        permission = Permission.objects.get(name=permiss)
        instance.user.user_permissions.add(permission)


def remove_user_permiss(instance):
    for permiss in ADMIN_PERMISSION:
            permission = Permission.objects.get(name=permiss)
            try:
                instance.user.user_permissions.remove(permission)
            except BaseException:
                pass


@receiver(post_save, sender=UserProfile)
def update_user_role(sender, instance, created, **kwargs):
    if instance.role == "viewer":
        remove_user_permiss(instance)
    elif instance.role == "contributor":
        remove_user_permiss(instance)
        set_user_permiss(instance, CONTRIBUTOR_PERMISSION)
    elif instance.role == "editor":
        remove_user_permiss(instance)
        set_user_permiss(instance, EDITOR_PERMISSION)
    elif instance.role == "manager":
        remove_user_permiss(instance)
        set_user_permiss(instance, MANAGER_PERMISSION)
