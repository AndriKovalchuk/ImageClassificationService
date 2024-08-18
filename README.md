<div style="text-align: center;">
  <img src="readme_img/logo.png" style="width: 400px;" alt="Logo">
</div>

# Вебзастосунок <span style="color:purple">InfinityVision</span> класифікує завантажені в нього зображення за допомогою Convolutional Neural Network.
# Розроблений на базі фреймворку [Django](https://www.djangoproject.com/)
# Використовується модель "model_2_finetuned.h5".

## Model_2_finetuned

В моделі "model_2_finetuned.h5" використаний підхід донавчання (Fine-tuning) на попередньо навченій моделі "model_2_vgg16.h5":

<div style="text-align: left;">
  <img src="readme_img/acc_compare.png" style="width: 900px;" alt="Acc_Compare">
</div>

* Шари з блоків block4 і block5 VGG16 розморожуються для повторного навчання.
* На основі базової моделі додаються власні шари для класифікації.
* Модель дообучується з новими гіперпараметрами, використовуючи збільшення даних (аугментацію).

### Точність:

![accurasy_finetuned.png](readme_img/accurasy_finetuned.png)

### Історія тренування "model_2_finetuned.h5":

<div style="text-align: left;">
  <img src="readme_img/acc_loss_finetuned.png" style="width: 900px;" alt="Acc_Loss_finetuned">
</div>

### Матриця невідповідностей:

<div style="text-align: left;">
  <img src="readme_img/conf_mat_finetuned.png" style="width: 600px;" alt="Conf_Mat">
</div>


## Model_2_vgg16

Основна модель "model_2_vgg16"

### Гіперпараметри:
* img_size: Встановлює розмір зображень у 56x56 пікселів. CIFAR-10 спочатку має розмір зображень 32x32, тому вони збільшуються до 56x56.
* num_classes: Кількість класів для класифікації (10 класів у CIFAR-10).
* batch_size: Розмір батчу під час навчання (128).
* epochs: Кількість епох для навчання (10).

![GP.png](readme_img/GP.png)

### Гіперпараметри для аугментації зображень:
* rotation_range, width_shift_range, height_shift_range, shear_range, zoom_range, horizontal_flip, fill_mode

### Створення базової моделі VGG16:
* VGG16: Використовується попередньо навчена модель VGG16 (без верхніх шарів), яка завантажує попередньо навчені ваги з ImageNet.
* base_model.trainable встановлюється у True, що дозволяє повторно навчати всі шари базової моделі.

### Додавання класифікаційної частини:
* Flatten: Вихідні дані базової моделі згладжуються в один вектор.
* Dense (256 нейронів): Додається повнозв'язний шар з 256 нейронами та функцією активації ReLU.
* Dropout (0.5): Додається шар Dropout для запобігання перенавчанню.
* Dense (num_classes): Вихідний шар із 10 нейронами (по одному на кожен клас) та функцією активації Softmax.

### Компіляція моделі:
* Модель компілюється з оптимізатором Adam (з встановленим низьким рівнем навчання), функцією втрат categorical_crossentropy, та метрикою accuracy.

### Збільшення даних (Data Augmentation):
* ImageDataGenerator: Використовується для збільшення даних (аугментації) під час навчання. Параметри збільшення відповідають заданим гіперпараметрам.

### EarlyStopping колбек:
* EarlyStopping: Застосовується для зупинки навчання, якщо показник валідації не покращується протягом заданої кількості епох (5), з автоматичним відновленням найкращих ваг.

## Модель VGG16 загалом містить 21 шар:
* 13 згорткових шарів.
* 3 шари підвибірки (Max Pooling), по одному після кожного з блоків згорткових шарів.
* 3 повнозв’язних (Dense) шари: останні шари, які зазвичай використовуються для класифікації (у класичній VGG16 архітектурі). Однак, у цьому коді вони замінені на інші шари.
* 2 шари активації: для останнього вихідного шару використовується Softmax

### Точність:

![accurasy.png](readme_img/accurasy.png)

### Історія тренування:

<div style="text-align: left;">
  <img src="readme_img/acc-loss.png" style="width: 900px;" alt="Acc_Loss">
</div>

### Матриця невідповідностей:

<div style="text-align: left;">
  <img src="readme_img/conf_mat.png" style="width: 600px;" alt="Conf_Mat">
</div>

