import numpy as np
from keras.losses import binary_crossentropy
from matplotlib import pyplot as plt

y_true = np.array([0, 1, 1, 0, 1, 0, 1, 1])
y_pred = np.array([0.1, 0.9, 0.8, 0.2, 0.7, 0.3, 0.6, 0.4])

def binary_cross_entropy(y_true, y_pred):
    eps = 1e-15  # to avoid log(0)
    y_pred = np.clip(y_pred, eps, 1 - eps)  # clip predictions
    bce = -np.mean(y_true * np.log(y_pred) + (1-y_true) * np.log(1-y_pred))
    return bce

losses = []
for epoch in range(1, 21):
    noise = np.random.normal(0, 0.02, size=y_pred.shape)
    y_pred_noisy = np.clip(y_pred + (0.05/epoch) - noise, 0.01, 0.99)  # ensure predictions are within [0, 1]
    bce_loss = binary_cross_entropy(y_true, y_pred_noisy)
    losses.append(bce_loss)

plt.plot(range(1, 21), losses, label='Custom BCE', marker='o')
plt.title('Binary Cross-Entropy Loss Over Epochs')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.grid(True)
plt.show()

bce_loss = binary_cross_entropy(y_true, y_pred)
print("Binary Cross-Entropy Loss:", bce_loss)

bce_loss_keras = binary_crossentropy(y_true, y_pred).numpy()
print("Binary Cross-Entropy Loss (Keras):", bce_loss_keras)


