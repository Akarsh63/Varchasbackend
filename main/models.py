from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models.signals import pre_save
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


class OurTeam(models.Model):
    POSITION_CHOICES = (
        (1, 'Festival Chief'),
        (2, 'Finance Head'),
        (3, 'Creativity'),
        (4, 'Informals'),
        (5, 'Marathon'),
        (6, 'Marketing'),
        (7, 'Public Relations and Hospitality'),
        (8, 'Publicity and Media'),
        (9, 'Pronite'),
        (10, 'Resources'),
        (11, 'Security'),
        (12, 'SOCH'),
        (13, 'Sport Coordinator'),
        (14, 'Transport'),
        (15, 'Web and APP'),
        (16, 'Vice President - Board of Student Sports'),
    )
    contact = RegexValidator(r'^[0-9]{10}$', message='Not a valid number!')
    email = models.EmailField(blank=True)
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10, validators=[contact])
    position = models.IntegerField(choices=POSITION_CHOICES,default=1)
    picture = models.ImageField(
        upload_to='teamPics/', blank=True, null=True, default="teamPics/default.jpg")
    insta = models.URLField(max_length=100, null=True, blank=True)
    fp = models.URLField(max_length=100, null=True, blank=True)
    linkedIn = models.URLField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['position']

class HomeEventCard(models.Model):
    name = models.CharField(max_length=64)
    image = models.ImageField(
        upload_to='homepage-events', blank=True, null=True)
    link = models.URLField()

    def __str__(self):
        return self.name

class NavBarSubOptions(models.Model):
    title = models.CharField(max_length=64)
    description = RichTextUploadingField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    use_custom_html = models.BooleanField(default=False)
    custom_html = models.CharField(max_length=64, blank=True, null=True)

    def clean(self):
        if self.use_custom_html and not self.custom_html:
            raise ValidationError(
                'Custom HTML should be present with Use custom html option')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('main:navbarsuboptionpage', kwargs={'slug': self.slug})


class NavBarOptions(models.Model):
    title = models.CharField(max_length=64)
    sub_options = models.ManyToManyField(NavBarSubOptions)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


def event_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)


pre_save.connect(event_pre_save_receiver, sender=NavBarSubOptions)
