import os
import requests
from api.src.core.config import settings

DEST_FOLDER = os.environ.get("VOICES_DIR", os.path.join("voices", "v1_0"))
os.makedirs(DEST_FOLDER, exist_ok=True)

print(f"✅ Saving voices to: {DEST_FOLDER}")

# List of tuples: (Google Drive URL, voice filename)
voices = [
    ('https://drive.google.com/uc?export=download&id=1S5Kn35IpJg0FF6LaF7zqgTbHd6CAkJJL', 'af_alloy.pt'),
    ('https://drive.google.com/uc?export=download&id=10tF0EV72LkSBTD3u4RSRLONhBvdUerou', 'af_aoede.pt'),
    ('https://drive.google.com/uc?export=download&id=17bvJQUtUGkWHXyBaisYH05H_dOQ2aHG5', 'af_bella.pt'),
    ('https://drive.google.com/uc?export=download&id=1_lfJDwD0fVORPOmDhNUOPZl1lsL-hZZf', 'af_heart.pt'),
    ('https://drive.google.com/uc?export=download&id=1JYsotLR5TC4HesWHdJIZlp1OF7ZS-a4R', 'af_jadzia.pt'),
    ('https://drive.google.com/uc?export=download&id=1hD4PHfRUmVjje2CL0fKR6wyTnOcNiIMa', 'af_jessica.pt'),
    ('https://drive.google.com/uc?export=download&id=1nLcjV8jTHmuXrTSfjCZ00g_XSnhJyvOp', 'af_kore.pt'),
    ('https://drive.google.com/uc?export=download&id=1rIKyUXrXe53WJpAk2e3v7nkjddL40k36', 'af_nicole.pt'),
    ('https://drive.google.com/uc?export=download&id=16gg3Yhmj1LvUI1Rim9-9cjGIdVkNNvg1', 'af_nova.pt'),
    ('https://drive.google.com/uc?export=download&id=1ooUCnKAXMRVZ9t0oJRpw82jmqzTcSRQZ', 'af_river.pt'),
    ('https://drive.google.com/uc?export=download&id=1_qQK41S-VCBMn9CmauPGaw38M6KH92fI', 'af_sarah.pt'),
    ('https://drive.google.com/uc?export=download&id=17p9oxvoNMucANd_FHqgXRPtCMu87cSPS', 'af_sky.pt'),
    ('https://drive.google.com/uc?export=download&id=1OaX8SrD1RI-fsZIa9jHTT8uL4x6IQjTi', 'af_vO.pt'),
    ('https://drive.google.com/uc?export=download&id=1uswnlYm7mBvTiacESv9cWP_DxDMk0bhm', 'af_vObella.pt'),
    ('https://drive.google.com/uc?export=download&id=1nNSXTUDoygBEK4QJ0RTjW0BhzoqpWDoT', 'af_vOirulan.pt'),
    ('https://drive.google.com/uc?export=download&id=1uH3F1rn3M15Nw8k86HejWJ28dic8qFZj', 'af_vOnicole.pt'),
    ('https://drive.google.com/uc?export=download&id=17kSNd-vINA9rJ0GamAHLbqj7ysvyhYgx', 'af_vOsarah.pt'),
    ('https://drive.google.com/uc?export=download&id=1sLoLdBxYin8cu2htJc2hh_4reC4fJJ8d', 'af_vOsky.pt'),
    ('https://drive.google.com/uc?export=download&id=1pA2GZXjIDBTcHN4zi9AMJEzPpmq9zcSE', 'am_adam.pt'),
    ('https://drive.google.com/uc?export=download&id=1yU-mKSrjYQZpq6ng094eMa0qld-7mY6h', 'am_echo.pt'),
    ('https://drive.google.com/uc?export=download&id=1x2jsm2cNlkV1EN9XwSuTi5IUKtpw3B0E', 'am_eric.pt'),
    ('https://drive.google.com/uc?export=download&id=1fd5owiKNONSoO2vzoBVzH2KvOXHxZvz-', 'am_fenrir.pt'),
    ('https://drive.google.com/uc?export=download&id=1OY26fuq6KE531ReysGdOv82YAVpaJKfX', 'am_liam.pt'),
    ('https://drive.google.com/uc?export=download&id=11DRpBzRmayBVuZpmWAe3RcNxbkAc7HCL', 'am_michael.pt'),
    ('https://drive.google.com/uc?export=download&id=1f99B6pDqv0sW0hmGnNQklv_1Zhd1R6PB', 'am_onyx.pt'),
    ('https://drive.google.com/uc?export=download&id=1tvpG8jfgBUXR56ks2nHKa-8O6zyj9VU_', 'am_puck.pt'),
    ('https://drive.google.com/uc?export=download&id=1HvgJaABNnIM5KZhqsbrl_xL9ADNgcGdJ', 'am_santa.pt'),
    ('https://drive.google.com/uc?export=download&id=1O76Kd7plq0sTZPAEvfE8O16L2T9KAuQS', 'am_vOadam.pt'),
    ('https://drive.google.com/uc?export=download&id=1nCb-gi29YwiA9Pi2hV-RJmKOaC_k5WeU', 'am_vOgurney.pt'),
    ('https://drive.google.com/uc?export=download&id=1oOTC4n3BgLfOiwaZeyyWnzvkvq7FNKR8', 'am_vOmichael.pt'),
    ('https://drive.google.com/uc?export=download&id=1OGn1wxlIpHjnqsu1lD95JdktYUWxedBg', 'bf_alice.pt'),
    ('https://drive.google.com/uc?export=download&id=1V9bxPnN-vaeqjWDf4X_E7vbiRkc8RTxS', 'bf_emma.pt'),
    ('https://drive.google.com/uc?export=download&id=141PDxpi7LDhHCDrUghzlg8M_OiifV7ZO', 'bf_lily.pt'),
    ('https://drive.google.com/uc?export=download&id=1iOFUmmSuwAG0vSihiwl8b1h5ceC5YzRo', 'bf_vOemma.pt'),
    ('https://drive.google.com/uc?export=download&id=1zTatpR4EsuEYeZavgjCI-0gJKufWvhwf', 'bf_vOisabella.pt'),
    ('https://drive.google.com/uc?export=download&id=1rgFm5o1Z66uW-R2rU10Q5ed3qzPG9NDJ', 'bm_daniel.pt'),
    ('https://drive.google.com/uc?export=download&id=1ysu41DFRaQYgEc-Kl0jOZLBJD2x1eSCz', 'bm_fable.pt'),
    ('https://drive.google.com/uc?export=download&id=1u3lFtGr35TDO0PzG6QvE9sK2O9ootVt4', 'bm_george.pt'),
    ('https://drive.google.com/uc?export=download&id=1Ujd4jhqoxf-0bIq_V-JIqgCAowhqPxhu', 'bm_lewis.pt'),
    ('https://drive.google.com/uc?export=download&id=1jjNUOEZpNWWLa2w_Hnbq_FXpajW5JliW', 'bm_vOgeorge.pt'),
    ('https://drive.google.com/uc?export=download&id=1elqlxz9P18YMW-6aC0_yumEULhmvNqnR', 'bm_vOlewis.pt'),
    ('https://drive.google.com/uc?export=download&id=1e60tDZsy-KhzadR8ER_-xoq8LFwFPtLL', 'ef_dora.pt'),
    ('https://drive.google.com/uc?export=download&id=1cygIvQf3fKyt0uBUtKRrp3Law27MBu42', 'em_alex.pt'),
    ('https://drive.google.com/uc?export=download&id=1TCIjSC3WRZ-G02j58Ko1lM0gevHWfBmL', 'em_santa.pt'),
    ('https://drive.google.com/uc?export=download&id=13xZ4PLspTGOC566D1CGsbXl84_EPrId5', 'ff_siwis.pt'),
    ('https://drive.google.com/uc?export=download&id=10K3WzG4CJHFnm9tZ1AF322YXavC0bMw9', 'hf_alpha.pt'),
    ('https://drive.google.com/uc?export=download&id=1R__A9J45_J1rnptJTFIBIjn15vX2DmqK', 'hf_beta.pt'),
    ('https://drive.google.com/uc?export=download&id=1DoYDWrl6fp7_l14BnIyKKhDycvyWnF8z', 'hm_omega.pt'),
    ('https://drive.google.com/uc?export=download&id=1EBzV4xt_fRscfyAZCc7QUFNQSXNCTaNh', 'hm_psi.pt'),
    ('https://drive.google.com/uc?export=download&id=13yZ-_CcbLzPy_iFg7776joxwBUJiqCwk', 'if_sarah.pt'),
    ('https://drive.google.com/uc?export=download&id=1Ax1Q-6ud8awmW4bmekvOm9QuoShxpd7-', 'im_nicola.pt'),
    ('https://drive.google.com/uc?export=download&id=1LVhFeGnf8_NZoyzTveD0kX__r03vqLSh', 'jf_alpha.pt'),
    ('https://drive.google.com/uc?export=download&id=1xAL8uk72FRohSyzi7YoPUGuuEgQhzUPX', 'jf_gongitsune.pt'),
    ('https://drive.google.com/uc?export=download&id=1_5mHtxVxlMr9F1rJlkU_MvQ7K4wyjrgq', 'jf_nezumi.pt'),
    ('https://drive.google.com/uc?export=download&id=1KylgFKnR3zy5ucOnCuBEKae6YGYKHUAC', 'jf_tebukuro.pt'),
    ('https://drive.google.com/uc?export=download&id=1ad7iWVK0qoNt-UPlBX_n1JJaBcDe1mm6', 'jm_kumo.pt'),
    ('https://drive.google.com/uc?export=download&id=1mAnSwEjbTYg3Nmds_f_0xSUbndAeWpgW', 'pf_dora.pt'),
    ('https://drive.google.com/uc?export=download&id=1xKZ6MKdzceT-HK4NZ05HYfRf0SvMCkYK', 'pm_alex.pt'),
    ('https://drive.google.com/uc?export=download&id=1zHUgMw7Ege7qIDF89KA7AIGf3uWX2WXr', 'pm_santa.pt'),
    ('https://drive.google.com/uc?export=download&id=1Vyz-vdzIsP6LhX-BbvVIDpg3FtxoPSVR', 'zf_xiaobei.pt'),
    ('https://drive.google.com/uc?export=download&id=1jP_rY1y6mCD2GRZaE60PQDNPlMFnXKE9', 'zf_xiaoni.pt'),
    ('https://drive.google.com/uc?export=download&id=1HHXiin4T0i7YrBXGYSySjNtg40IyAUix', 'zf_xiaoxiao.pt'),
    ('https://drive.google.com/uc?export=download&id=12gQedeAoDJJpet_03Ccw3KM2jURdYhbd', 'zf_xiaoyi.pt'),
    ('https://drive.google.com/uc?export=download&id=1QbyZt1pKlyy3m_dbuS7Q6xsr0d4b19XA', 'zm_yunjian.pt'),
    ('https://drive.google.com/uc?export=download&id=13voDtNrsthK8iTpoDxkorj7D05dwovEy', 'zm_yunxi.pt'),
    ('https://drive.google.com/uc?export=download&id=1JmF1bo_a6rkBzUd2uEr7KiWmw5Tkpkrv', 'zm_yunxia.pt'),
    ('https://drive.google.com/uc?export=download&id=123UaiRavJvA-vdhHUOFuaTUg4wH70erd', 'zm_yunyang.pt'),
]

downloaded = 0
skipped = 0

# Iterate through the list of (url, filename) pairs
for url, filename in voices:
    filepath = os.path.join(DEST_FOLDER, filename)
    
    if os.path.exists(filepath):
        print(f"{filename} already exists, skipping.")
        skipped += 1
        continue

    try:
        print(f"Downloading {filename}...")
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(filepath, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded {filename}")
        downloaded += 1
    except Exception as e:
        print(f"❌ Failed to download {filename}: {e}")

print(f"\n✅ Download complete. {downloaded} downloaded, {skipped} skipped.")
if downloaded == 0:
    print("All voice files already exist. No new files were downloaded.")