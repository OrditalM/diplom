import tensorflow as tf
from tensorflow import keras
import numpy as np
import cv2 as cv

# Создайте сверточную нейронную сеть
model = keras.models.Sequential()
# ... (Архитектура нейронной сети, как в предыдущем ответе)

# Компилируем модель
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Вывести информацию о модели
model.summary()

# Загрузите и подготовьте данные
def load_data(image_paths, mask_paths):
    images = []
    masks = []

    for img_path, mask_path in zip(image_paths, mask_paths):
        image = Image.open(img_path)
        image = image.resize((width, height))
        image = np.array(image) / 255.0

        mask = Image.open(mask_path)
        mask = mask.convert('L')  # Преобразовать маску в оттенки серого
        mask = mask.resize((width, height))
        mask = np.array(mask) / 255.0
        mask = np.expand_dims(mask, axis=-1)

        images.append(image)
        masks.append(mask)

    return np.array(images), np.array(masks)

# Примеры путей к изображениям и маскам
image_paths = ['image1.jpg', 'image2.jpg', ...]
mask_paths = ['mask1.jpg', 'mask2.jpg', ...]

# Загрузите данные
images, masks = load_data(image_paths, mask_paths)

# Разделите данные на обучающий и проверочный наборы
train_ratio = 0.8
split_index = int(len(images) * train_ratio)

train_images, train_masks = images[:split_index], masks[:split_index]
val_images, val_masks = images[split_index:], masks[split_index:]

# Создайте генераторы для аугментации данных
train_datagen = keras.preprocessing.image.ImageDataGenerator(
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True,
    vertical_flip=True
)

val_datagen = keras.preprocessing.image.ImageDataGenerator()

# Обучите модель
batch_size = 16
epochs = 10

train_generator = train_datagen.flow(train_images, train_masks, batch_size=batch_size)
val_generator = val_datagen.flow(val_images, val_masks, batch_size=batch_size)

model.fit(train_generator, steps_per_epoch=len(train_images) // batch_size, epochs=epochs, validation_data=val_generator, validation_steps=len(val_images) // batch_size)
