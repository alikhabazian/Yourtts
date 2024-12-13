import os
import requests
import tarfile
from tqdm import tqdm

proxies = {
    'http': 'socks5h://127.0.0.1:14000',
    'https': 'socks5h://127.0.0.1:14000',
}
# List of URLs to download
urls = [
    "https://www.openslr.org/resources/146/cml_tts_dataset_dutch_v0.1.tar.bz",
    "https://www.openslr.org/resources/146/cml_tts_dataset_french_v0.1.tar.bz",
    "https://www.openslr.org/resources/146/cml_tts_dataset_german_v0.1.tar.bz",
    "https://www.openslr.org/resources/146/cml_tts_dataset_italian_v0.1.tar.bz",
    "https://www.openslr.org/resources/146/cml_tts_dataset_polish_v0.1.tar.bz",
    "https://www.openslr.org/resources/146/cml_tts_dataset_portuguese_v0.1.tar.bz",
    "https://www.openslr.org/resources/146/cml_tts_dataset_spanish_v0.1.tar.bz",
    "https://www.openslr.org/resources/146/cml_tts_dataset_segments_v0.1.tar.bz"
    # Add more URLs here
]

# Base directory to save and extract datasets
base_dir = "dataset"
def get_cml_dataset():
    # Loop through each URL in the list
    for url in urls:
        # Extract the filename from the URL and set up directories
        filename = url.split('/')[-1]
        folder_name = filename.split(".tar.bz")[0]  # Get the base name for the folder
        download_dir = os.path.join(base_dir, folder_name)
        file_path = os.path.join(download_dir, filename)

        # Create the download directory if it doesn't exist
        os.makedirs(download_dir, exist_ok=True)

        # Download the file with progress bar
        print(f"Downloading {filename}...")
        response = requests.get(url, stream=True,proxies=proxies)
        if response.status_code == 200:
            total_size = int(response.headers.get('content-length', 0))
            with open(file_path, "wb") as file, tqdm(
                    desc=filename,
                    total=total_size,
                    unit='B',
                    unit_scale=True,
                    unit_divisor=1024,
            ) as bar:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)
                    bar.update(len(chunk))
            print(f"Download of {filename} completed.")
        else:
            print(f"Failed to download {filename}. Status code:", response.status_code)
            continue

        # Extract the file with progress bar
        print(f"Extracting {filename}...")
        if tarfile.is_tarfile(file_path):
            with tarfile.open(file_path, "r:bz2") as tar:
                members = tar.getmembers()
                with tqdm(total=len(members), desc=f"Extracting {filename}", unit="file") as bar:
                    for member in members:
                        tar.extract(member, path=download_dir)
                        bar.update(1)
            print(f"Extraction of {filename} completed.")
        else:
            print(f"The downloaded file {filename} is not a tar.bz archive.")

        # Optionally, delete the tar.bz file after extraction
        os.remove(file_path)
        print(f"{filename} removed after extraction.\n")
get_cml_dataset()
