import os
import urllib.request

print("🚨 THIS IS THE RAILWAY DOWNLOAD SCRIPT")

voice_dir = 'api/src/voices/v1_0'
os.makedirs(voice_dir, exist_ok=True)

voice_links = {
    'af_alloy.pt': 'https://drive.google.com/uc?export=download&id=1S5Kn35IpJg0FF6LaF7zqgTbHd6CAkJJL',
    'af_aoede.pt': 'https://drive.google.com/uc?export=download&id=1GJHjPr8zicOWqBa9toK0r8bRhquNcFCJ',
    'af_bella.pt': 'https://drive.google.com/uc?export=download&id=1HR8xPfyty7B45xlo4bMFgr2xPYjllLq6',
    'af_heart.pt': 'https://drive.google.com/uc?export=download&id=1Qku2SH4KXeqYmTUEtcuKRbDDhmn9acFv',
    'af_jadzia.pt': 'https://drive.google.com/uc?export=download&id=1g0ODz6ld9GSft7j35E3O_A14GpbrRrse',
    'af_jessica.pt': 'https://drive.google.com/uc?export=download&id=1VZwYG0QpMZfJ3LBNABeIXPR_VRmeKXb1',
    'af_kore.pt': 'https://drive.google.com/uc?export=download&id=1NBJQyQK-Q8DXNSVrKpRP1euW6rxS_0J_',
    'af_nicole.pt': 'https://drive.google.com/uc?export=download&id=1sVqDLyJ1QUj7pZwFBcZVXykzxtgkcc_Y',
    'af_nova.pt': 'https://drive.google.com/uc?export=download&id=1XsZ1CvwT_YfR0ApbKopNEwJdFR41tnq3',
    'af_river.pt': 'https://drive.google.com/uc?export=download&id=1sH3yXU4t-jLhKIoJYiA5RZZc3cR39ss4',
    'af_sarah.pt': 'https://drive.google.com/uc?export=download&id=1hrFYeS-HjOtzgxXk2P_bZTghgsws9B3F',
    'af_sky.pt': 'https://drive.google.com/uc?export=download&id=1GmQO60OVvUWr0JPp4dRqxJhHTRP5CmZ0',
    'af_v0.pt': 'https://drive.google.com/uc?export=download&id=1bDwH9dLaHqKLx2e3BPRqj9HuP7rwiOgK',
    'af_v0bella.pt': 'https://drive.google.com/uc?export=download&id=1-DyiRxRRlm0g5jvq8KK-FenQ7lfGpfrZ',
    'af_v0nicole.pt': 'https://drive.google.com/uc?export=download&id=1LT1uEVeEdrTbK54sAPMw4Nph5SOjq5vJ',
    'af_v0sarah.pt': 'https://drive.google.com/uc?export=download&id=1OBBEa8bUPcG5jbhX7lguDXZ0muv3Vwlt',
    'af_v0sky.pt': 'https://drive.google.com/uc?export=download&id=1yArMOTNgMH2nqllOsvZyoUz2VB9LCIHX',
    'af_vo.pt': 'https://drive.google.com/uc?export=download&id=1m3FpcAz2iM-Lw6IQx6Si3rFuUIdjT2qZ',
    'af_vobella.pt': 'https://drive.google.com/uc?export=download&id=1vHt3WbRx_ePGaZlA4kNhTHpeZ1vM_hmE',
    'af_voirulan.pt': 'https://drive.google.com/uc?export=download&id=1na9FRkU9XPaQzkgPVq8f5O_wKtrjzzYw',
    'am_adam.pt': 'https://drive.google.com/uc?export=download&id=1H6Yt-w3t8kHaP1XpEV_aQ2a2n8llsE3g',
    'am_echo.pt': 'https://drive.google.com/uc?export=download&id=1mcFFKjvZZgqlJrfNusL3Sp5MzR3syFAp',
    'am_eric.pt': 'https://drive.google.com/uc?export=download&id=1Z_kebhF0QjZ9OXMnNqsv6qEdFVnbPEFb',
    'am_fennrir.pt': 'https://drive.google.com/uc?export=download&id=1AB9uMEepDydSxWddhd5q_kD5tAcR6pZk',
    'am_liam.pt': 'https://drive.google.com/uc?export=download&id=1dV0_djQEuM47kS7iPbspMfNzzRzqj-RH',
    'am_michael.pt': 'https://drive.google.com/uc?export=download&id=1c_5ZCU7LfG20KHNZ5HaGvEp0ISUVd3IQ',
}

print("🔊 Starting Kokoro voice file download...")

for filename, url in voice_links.items():
    safe_filename = filename.replace('.pt.pt', '.pt')  # In case the URL already ends with .pt
    out_path = os.path.join(voice_dir, safe_filename)
    print(f"⬇ Downloading: {safe_filename}")
    urllib.request.urlretrieve(url, out_path)
    print(f"✔ Downloaded: {safe_filename}")

print('✅ All voice files downloaded.')
