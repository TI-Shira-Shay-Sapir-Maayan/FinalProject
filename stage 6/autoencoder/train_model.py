from dataloader import DataLoader
from autoencoder import AutoencoderModel
import numpy as np
import os

# Function to save results to a file
def save_results_to_file(file_name, results):
    with open(file_name, 'w', encoding='utf-8') as f:
        for line in results:
            f.write(line + '\n')

# Updated function to test the model every 10 samples as one group
def test_model_on_folder(autoencoder_model, folder_path, threshold, group_size=10):
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".csv"):
            file_path = os.path.join(folder_path, file_name)
            print(f"\nTesting file: {file_name}")

            # Load and preprocess the new data
            test_data_loader = DataLoader(folder_path)
            test_data_loader.load_single_file(file_path)
            X_test_new = test_data_loader.preprocess_data()

            results = [f"File: {file_name}"]

            # Group every 10 samples together
            num_groups = len(X_test_new) // group_size
            for i in range(num_groups):
                start_idx = i * group_size
                end_idx = start_idx + group_size
                group_samples = X_test_new[start_idx:end_idx]

                # Calculate reconstruction errors for the group
                errors = autoencoder_model.reconstruction_error(group_samples)
                median_error = np.median(errors)

                # Check movement based on median error of the group
                movement_detected = median_error > threshold

                if movement_detected:
                    results.append(f"🟢 Samples {start_idx+1}-{end_idx}: Movement Detected (Median Error: {median_error:.4f})")
                else:
                    results.append(f"🔴 Samples {start_idx+1}-{end_idx}: No Movement Detected (Median Error: {median_error:.4f})")

            # Check if any samples are left (not divisible by group_size)
            remainder = len(X_test_new) % group_size
            if remainder > 0:
                start_idx = num_groups * group_size
                group_samples = X_test_new[start_idx:]
                errors = autoencoder_model.reconstruction_error(group_samples)
                median_error = np.median(errors)
                movement_detected = median_error > threshold

                if movement_detected:
                    results.append(f"🟢 Samples {start_idx+1}-{len(X_test_new)}: Movement Detected (Median Error: {median_error:.4f})")
                else:
                    results.append(f"🔴 Samples {start_idx+1}-{len(X_test_new)}: No Movement Detected (Median Error: {median_error:.4f})")

            # Save results to file
            save_results_to_file(f"results_{file_name}.txt", results)

# Load training dataset
dataset_dir = 'dataset'
data_loader = DataLoader(dataset_dir)
data_loader.load_data()
X_processed = data_loader.preprocess_data()

# Split the data for training and testing
X_train, X_test = data_loader.split_data(X_processed)

# Build and train the model
input_shape = (X_train.shape[1],)
autoencoder_model = AutoencoderModel(input_shape=input_shape, latent_dim=32)
autoencoder_model.build_model()
autoencoder_model.train(X_train)

# Reconstruction errors for training data
errors_no_motion = autoencoder_model.reconstruction_error(X_test)

# Determine threshold (Using 95th percentile)
threshold = autoencoder_model.set_threshold(errors_no_motion, percentile=95)
print(f"Reconstruction error threshold set to: {threshold:.4f}")

# Save the model if needed
autoencoder_model.autoencoder.save("trained_autoencoder.h5")

# Test the model with the new data (grouped every 10 samples)
test_model_on_folder(autoencoder_model, 'dataset_withmoves', threshold, group_size=10)


