from django.db import models
from datetime import datetime
from django.core.urlresolvers import reverse
# Create your models here.
from django.utils.text import slugify
class Post(models.Model):
    company = models.CharField(max_length=20)
    flag = models.BooleanField(default=0, editable=False)
    receiver = models.CharField(max_length=40)
    item = models.CharField(max_length=20)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    room = models.CharField(max_length=10,default="None")
    hostelname = models.CharField(max_length=256, default="None",choices=[('Aibaan', 'Aibaan'), ('Beauki', 'Beauki'),('Chimair', 'Chimair'),
                                                                       ('Duven','Duven'),('Emiet','Emiet'),('Firpeal','Firpeal')])
    def __str__(self):
        return self.receiver+"-"+self.item

    '''def get_absolute_url(self):
        return reverse("post:detail", kwargs={"slug": self.slug})


   def create_slug(instance, new_slug=None):
        slug = slugify(instance.title)
        if new_slug is not None:
            slug = new_slug
        qs = Post.objects.filter(slug=slug).order_by("-id")
        exists = qs.exists()
        if exists:
            new_slug = "%s-%s" % (slug, qs.first().id)
            return create_slug(instance, new_slug=new_slug)
        return slug
'''

# Create your models here.
