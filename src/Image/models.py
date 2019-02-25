from django.db import models
from django.urls import reverse
from django.db.models.signals import pre_save, post_save
from django.core.files import File
import os
from urllib.request import urlopen
from tempfile import NamedTemporaryFile
from PIL import Image as Image_
import imagehash


def upload_location(slug, filename):
	return '%s'%(filename) 

class Image(models.Model):
	image_file 		= models.ImageField(
		upload_to=upload_location,
		null=True,
		blank=True,
		width_field='width_field',
		height_field='height_field'
		)
	width_field		= models.IntegerField(blank=True, null=True)
	height_field 	= models.IntegerField(blank=True, null=True)
	image_url 		= models.URLField(blank=True, null=True)
	size 			= models.IntegerField(blank=True, null=True)
	timestamp		= models.DateTimeField(auto_now_add=True)
	updated			= models.DateTimeField(auto_now=True)
	slug 			= models.SlugField(blank=True, null=True)

	def __str__(self):
		return str(self.id)

	def get_absolute_url(self):
		return reverse('image:detail', kwargs = {'slug' : self.slug})

def tl_pre_save_receiver(sender, instance, *args, **kwargs):
	if instance.image_url and not instance.image_file:
		extension = instance.image_url.split('.')[-1]
		img_temp = NamedTemporaryFile(delete=True)
		img_temp.write(urlopen(instance.image_url).read())
		img_temp.flush()
		instance.image_file.save(f"image_.{extension}", File(img_temp))
	instance.size = instance.image_file.size	
	
pre_save.connect(tl_pre_save_receiver, sender=Image)

