import numpy as np
import tensorflow as tf
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from .forms import FileFieldForm
from .models import IMAGE

MODEL_PATH = 'models/model_2_finetuned.h5'
model = tf.keras.models.load_model(MODEL_PATH)
model.summary()

CLASS_LABELS = [
    'airplane', 'automobile', 'bird', 'cat', 'deer',
    'dog', 'frog', 'horse', 'ship', 'truck'
]


def preprocess_image(image):
    image_content = image.read()
    if not image_content:
        raise ValueError("Image content is empty")

    image = tf.image.decode_image(image_content, channels=3)

    image = tf.image.resize(image, [56, 56])

    image = image / 255.0
    image = tf.expand_dims(image, axis=0)

    return image


def classify_image(image):
    try:
        preprocessed_image = preprocess_image(image)

        predictions = model.predict(preprocessed_image)

        if predictions.size == 0:
            raise ValueError("No predictions were made.")

        predicted_class = CLASS_LABELS[np.argmax(predictions)]
        return predicted_class
    except Exception as e:
        print(f"Error in classify_image: {e}")
        return "Error in classification"


@login_required
def upload_image(request):
    if request.method == 'POST':
        form = FileFieldForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('file_field')
            image_documents = []
            predictions = []

            for file in files:
                image_document = IMAGE(file=file, user=request.user, original_name=file.name)

                try:
                    predicted_class = classify_image(file)
                    image_document.predicted_class = predicted_class
                    image_document.save()

                    image_documents.append(image_document)
                    predictions.append(predicted_class)
                except ValueError as e:
                    return render(request, 'image_process/upload_image.html', {'form': form, 'error': str(e)})
                except Exception as e:
                    return render(request, 'image_process/upload_image.html',
                                  {'form': form, 'error': 'An error occurred during image processing'})

            return render(request, 'image_process/upload_success.html', {
                'images': zip(image_documents, predictions)
            })
    else:
        form = FileFieldForm()
    return render(request, 'image_process/upload_image.html', {'form': form})


def upload_success(request):
    return render(request, 'image_process/upload_success.html')


@login_required
def my_images(request):
    images = IMAGE.objects.filter(user=request.user)
    return render(request, 'image_process/my_images.html', {'images': images})


@login_required
def classify_image_view(request, image_id):
    image = get_object_or_404(IMAGE, id=image_id, user=request.user)

    try:
        predicted_class = classify_image(image.file)
        return render(request, 'image_process/classification_result.html', {
            'image': image,
            'predicted_class': predicted_class
        })
    except ValueError as e:
        return render(request, 'image_process/classification_result.html', {
            'image': image,
            'error': str(e)
        })
    except Exception as e:
        return render(request, 'image_process/classification_result.html', {
            'image': image,
            'error': 'An error occurred during image processing'
        })
