import requests
import os
import sys

def download_models(token):
    # (Civitai Model ID, Folder in ComfyUI/models/)
    models = [
        (2047770, "checkpoints"), # Illustrious NSFW from Hades
        (1359028, "checkpoints"), # Bismuth Illustrious Mix
        (1602909, "loras"), # Asura Style
        (996220, "loras"), # Ri Mix
        (1837939, "loras"), # Whyd5424
        (2006381, "loras"), # RTF Style
        (1659625, "loras"), # DC Tomorrowverse
        (1729904, "loras"), # Azz Style
        (1646900, "loras"), # Mapp Style
        (1256683, "loras"), # Disney Animation
        (1477075, "loras"), # Ting An Cosplay
        (1385116, "loras"), # Tizi
        (553648, "loras"), # Wai Ani Hentai (Note: Pony LoRA on Illustrious)
        (779355, "loras"), # Western Comic
    ]
    
    base_path = "/workspace/ComfyUI/models"
    
    for model_id, model_type in models:
        try:
            # Fetch model metadata from Civitai API
            url = f"https://civitai.com/api/v1/models/{model_id}"
            resp = requests.get(url)
            resp.raise_for_status()
            data = resp.json()
            
            # Get the latest version
            version = data['modelVersions'][0]
            version_id = version['id']
            filename = version['files'][0]['name']
            
            # Construct authenticated download URL
            download_url = f"https://civitai.com/api/download/models/{version_id}?token={token}"
            save_dir = os.path.join(base_path, model_type)
            os.makedirs(save_dir, exist_ok=True)
            save_path = os.path.join(save_dir, filename)
            
            print(f"⬇️ Downloading {filename}...")
            with requests.get(download_url, stream=True) as r:
                r.raise_for_status()
                with open(save_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            print(f"✅ Saved {filename}")
        except Exception as e:
            print(f"❌ Failed {model_id}: {e}")

if __name__ == "__main__":
    token = os.environ.get("CIVITAI_TOKEN")
    if not token:
        print("❌ ERROR: CIVITAI_TOKEN environment variable is not set!")
        sys.exit(1)
    download_models(token)
