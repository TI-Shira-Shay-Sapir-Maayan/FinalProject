from tensorflow.keras import layers, models
from tensorflow.keras.callbacks import EarlyStopping
import numpy as np

class AutoencoderModel:
    def __init__(self, input_shape, latent_dim=32):
        """pip install tensorflow keras matplotlib
pip install jupyterlab
        Autoencoder Model for CSI data.
        """
        self.input_shape = input_shape
        self.latent_dim = latent_dim
        self.autoencoder = None

    def build_model(self):
        input_layer = layers.Input(shape=self.input_shape)

        # Encoder
        encoded = layers.Dense(128, activation='relu')(input_layer)
        encoded = layers.Dense(self.latent_dim, activation='relu')(encoded)

        # Decoder
        decoded = layers.Dense(128, activation='relu')(encoded)
        decoded = layers.Dense(self.input_shape[0], activation='linear')(decoded)

        self.autoencoder = models.Model(input_layer, decoded)
        self.autoencoder.compile(optimizer='adam', loss='mse')

        return self.autoencoder

    def train(self, X_train, epochs=50, batch_size=128, validation_split=0.2):
        early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
        self.autoencoder.fit(X_train, X_train, epochs=epochs, batch_size=batch_size, 
                             validation_split=validation_split, callbacks=[early_stopping])

    def evaluate(self, X_test):
        loss = self.autoencoder.evaluate(X_test, X_test)
        print(f"Test loss: {loss}")

    def predict(self, X_input):
        return self.autoencoder.predict(X_input)

    def reconstruction_error(self, X_input):
        reconstructed = self.predict(X_input)
        errors = np.mean(np.square(X_input - reconstructed), axis=1)
        return errors

    def set_threshold(self, errors, percentile=95):
        return np.percentile(errors, percentile)

    def detect_movement(self, error, threshold):
        return error > threshold

