import os
import pathlib

import numpy as np
import tensorflow as tf
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from tensorflow.keras.preprocessing import image

from .forms import FileFieldForm, EditImageNameForm
from .models import IMAGE

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'model_3_finetuned.h5')
model = tf.keras.models.load_model(MODEL_PATH)
model.summary()

class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']


def get_file_name(file_path):
    file_path_components = file_path.split('/')
    file_name_and_extension = file_path_components[-1].rsplit('.', 1)
    return file_name_and_extension[0]


@login_required
def upload_image(request):
    error_message = None
    if request.method == 'POST':
        form = FileFieldForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('file_field')
            image_documents = []
            predictions = []

            for file in files:
                file_extension = pathlib.Path(file.name).suffix
                if file_extension in [".jpg", ".jpeg", ".webp", ".bmp", ".png"]:
                    image_document = IMAGE(file=file, user=request.user, original_name=file.name)
                    img = image.load_img(file.file, target_size=(128, 128))
                    img_array = image.img_to_array(img)
                    img_array = np.expand_dims(img_array, axis=0)
                    img_array = img_array / 255.0

                    predictions = model.predict(img_array)
                    predicted_class = np.argmax(predictions[0])
                    predicted_class = class_names[predicted_class]

                    image_document.predicted_class = predicted_class
                    image_document.save()
                    image_documents.append(image_document)

                else:
                    error_message = 'Only image files are allowed'

            if error_message:
                return render(request, 'image_process/upload_image.html',
                              {'form': form, "error_message": error_message})

                    # form.add_error(None, "Only image files are allowed.")
                    # return render(request, 'image_process/upload_image.html', {'form': form})

            # return render(request, 'image_process/upload_success.html', {
            #     'images': zip(image_documents, predictions)
            # })

    else:
        form = FileFieldForm()
    return render(request, 'image_process/upload_image.html', {'form': form})


def upload_success(request):
    return render(request, 'image_process/upload_success.html')


@login_required
def my_images(request):
    search_query = request.GET.get('search', '')
    images = IMAGE.objects.filter(user=request.user)

    if search_query:
        images = images.filter(
            original_name__icontains=search_query
        ) | images.filter(
            predicted_class__icontains=search_query
        )

    return render(request, 'image_process/my_images.html', {'images': images, 'search_query': search_query})


@login_required
def classify_image_view(request, image_id):
    image = get_object_or_404(IMAGE, id=image_id, user=request.user)

    try:
        predicted_class = classify_image(image.file)
        return render(request, 'image_process/edit_image.html', {
            'image': image,
            'predicted_class': predicted_class
        })
    except ValueError as e:
        return render(request, 'image_process/edit_image.html', {
            'image': image,
            'error': str(e)
        })
    except Exception as e:
        return render(request, 'image_process/edit_image.html', {
            'image': image,
            'error': 'An error occurred during image processing'
        })


@login_required
def delete_image(request, image_id):
    image = get_object_or_404(IMAGE, id=image_id, user=request.user)
    image.delete()
    return redirect('image_process:my_images')


@login_required
def edit_image_name(request, image_id):
    image = get_object_or_404(IMAGE, id=image_id, user=request.user)

    if request.method == 'POST':
        form = EditImageNameForm(request.POST, instance=image)
        if form.is_valid():
            form.save()
            return redirect('image_process:my_images')
    else:
        form = EditImageNameForm(instance=image)

    return render(request, 'image_process/edit_image_name.html', {'form': form, 'image': image})
