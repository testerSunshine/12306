# coding: utf-8
import TickerConfig
if TickerConfig.AUTO_CODE_TYPE == 2:
    import sys

    import cv2
    import numpy as np
    from keras import models
    from keras import layers
    from keras import optimizers
    from keras.applications import VGG16
    from keras.callbacks import ReduceLROnPlateau
    from keras.preprocessing.image import ImageDataGenerator


def preprocess_input(x):
    x = x.astype('float32')
    # 我是用cv2来读取的图片，其已经是BGR格式了
    mean = [103.939, 116.779, 123.68]
    x -= mean
    return x


def load_data():
    # 这是统计学专家提供的训练集
    data = np.load('captcha.npz')
    train_x, train_y = data['images'], data['labels']
    train_x = preprocess_input(train_x)
    # 由于是统计得来的信息，所以在此给定可信度
    sample_weight = train_y.max(axis=1) / np.sqrt(train_y.sum(axis=1))
    sample_weight /= sample_weight.mean()
    train_y = train_y.argmax(axis=1)

    # 这是人工提供的验证集
    data = np.load('captcha.test.npz')
    test_x, test_y = data['images'], data['labels']
    test_x = preprocess_input(test_x)
    return (train_x, train_y, sample_weight), (test_x, test_y)


def learn():
    (train_x, train_y, sample_weight), (test_x, test_y) = load_data()
    datagen = ImageDataGenerator(horizontal_flip=True,
                                 vertical_flip=True)
    train_generator = datagen.flow(train_x, train_y, sample_weight=sample_weight)
    base = VGG16(weights='imagenet', include_top=False, input_shape=(None, None, 3))
    for layer in base.layers[:-4]:
        layer.trainable = False
    model = models.Sequential([
        base,
        layers.BatchNormalization(),
        layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
        layers.GlobalAveragePooling2D(),
        layers.BatchNormalization(),
        layers.Dense(64, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.20),
        layers.Dense(80, activation='softmax')
    ])
    model.compile(optimizer=optimizers.RMSprop(lr=1e-5),
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    model.summary()
    reduce_lr = ReduceLROnPlateau(verbose=1)
    model.fit_generator(train_generator, epochs=400,
                        steps_per_epoch=100,
                        validation_data=(test_x[:800], test_y[:800]),
                        callbacks=[reduce_lr])
    result = model.evaluate(test_x, test_y)
    print(result)
    model.save('12306.image.model.h5', include_optimizer=False)


def predict(imgs):
    imgs = preprocess_input(imgs)
    model = models.load_model('12306.image.model.h5')
    labels = model.predict(imgs)
    return labels


def _predict(fn):
    imgs = cv2.imread(fn)
    imgs = cv2.resize(imgs, (67, 67))
    imgs.shape = (-1, 67, 67, 3)
    labels = predict(imgs)
    print(labels.max(axis=1))
    print(labels.argmax(axis=1))


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        _predict(sys.argv[1])
    else:
        learn()
