import requests
from tqdm import tqdm
from pathlib import Path
from src import PROJECT_ROOT

def download_from_drive(file_id='1thB3okTAkVC35DWRP68E3CR_feIavcov', destination=None):
    
    if destination is None:
        root_dir = Path(PROJECT_ROOT, 'pipeline', 'weights', 'model.pth')
    else:
        root_dir = Path(destination)
    print(f"Searching for detection model at {str(root_dir)}...")
    if root_dir.exists():
        print(f"Model found at {destination}")
        return
    else:
        print(f"Downloading file from Google Drive with id {file_id} to {str(root_dir)}")
        
    URL = f"https://drive.google.com/uc?export=download"
    
    session = requests.Session()
    response = session.get(URL, params={'id': file_id}, stream=True)
    token = get_confirm_token(response)
    
    if token:
        params = {'id': file_id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)
    
    save_response_content(response, str(root_dir))

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