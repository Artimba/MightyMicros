import requests
from tqdm import tqdm
from pathlib import Path
import importlib.resources as pkg

def download_from_drive(file_id='1EqGxndfMEqUc26kndfm95jjQg9dEOLXY', destination=None):
    
    if destination is None:
        with pkg.path('src.pipeline.weights', '') as weights_path:
            print(f"Searching for detection model at {str(weights_path)}...")
            model_path = Path(weights_path, 'model.pt')
            if model_path.exists():
                print(f"Model found at {model_path}")
                return weights_path  # Assuming you want to return the path
            else:
                print(f"Downloading file from Google Drive with id {file_id} to {str(weights_path)}")
        
    URL = f"https://drive.google.com/uc?export=download"
    
    session = requests.Session()
    response = session.get(URL, params={'id': file_id}, stream=True)
    token = get_confirm_token(response)
    
    if token:
        print("Warning found. Bypassing.")
        params = {'id': file_id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)
    
    save_response_content(response, str(model_path))

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value
    
    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768
    
    with open(destination, "wb") as f, tqdm(
        unit="B", unit_scale=True, unit_divisor=1024, total=int(response.headers.get('content-length', 0))
    ) as bar:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
                bar.update(len(chunk))