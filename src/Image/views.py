from django.shortcuts import render, get_object_or_404
from .models import Image
from .forms import ImageCreateForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.http import HttpResponseRedirect
from PIL import Image as Image_
import imagehash
from django.core.exceptions import ValidationError

class ImageListView(ListView):
	queryset = Image.objects.all()

class ImageDetailView(DetailView):
	queryset = Image.objects.all()

	def resize_image(self, width, height, q):
		image = Image_.open(self.object.image_file)
		extension = self.object.image_file.url.split('.')[-1]
		w, h = image.size
		if not width:
				width = w
		elif not height:
			height = h
		resized_image = image.resize((int(width),int(height)), Image_.LANCZOS)
		resized_image.save(self.object.image_file.path, optimize=True, quality = q)

	def get_context_data(self, *args, **kwargs):
		context = super(ImageDetailView, self).get_context_data(**kwargs)
		width = self.request.GET.get('width')
		height = self.request.GET.get('height')
		size = self.request.GET.get('size')
		if width or height:
			quality = 95
			self.resize_image(width, height, quality)
			if size:
				while self.object.image_file.size > int(size):
					if quality > 10:
						quality-=10
						self.resize_image(width, height, quality)
					else:
						raise ValidationError("This so small for this image.")		
		return context

class ImageCreateView(CreateView):
	template_name = 'form.html'
	form_class = ImageCreateForm

	def get_context_data(self, *args, **kwargs):
		context = super(ImageCreateView, self).get_context_data(**kwargs)
		if self.request.POST:
			context['form'] = ImageCreateForm(self.request.POST, self.request.FILES)
		else:
			context['form'] = ImageCreateForm()
		return context

	def form_valid(self, form):
		if form.is_valid():
			self.object = form.save()
			self.object.slug = imagehash.average_hash(Image_.open(self.object.image_file.path))
			form.save()
			return super().form_valid(form)
		else:
			return self.render_to_response(self.get_context_data(form=form))


