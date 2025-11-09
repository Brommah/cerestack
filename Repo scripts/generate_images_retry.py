#!/usr/bin/env python3
"""
Retry-enabled image generation script for Cere Stack article
This version handles quota errors and can resume where it left off
"""

import os
import json
import time
from datetime import datetime
from google import genai
from google.genai import types
from PIL import Image

# Configuration
API_KEY = "AIzaSyAxmDebE_c-LDZ-CCPVTbiiDojuXlj45JA"
IMAGES_DIR = "generated_images"
STATUS_FILE = os.path.join(IMAGES_DIR, "generation_status.json")

# Create directory
os.makedirs(IMAGES_DIR, exist_ok=True)

# Image configurations (same as before but stored for retry logic)
image_configs = {
    "01_cerebellum_to_cephalum": {
        "prompt": "Split-screen technical illustration: left shows human cerebellum neural pathways, right shows digital architecture with Cere layers 1-3 and CEF layers 4-7, connected by data flow transitions",
        "aspect_ratio": "16:9"
    },
    "02_blockchain_foundation": {
        "prompt": "Isometric blockchain foundation: substrate bedrock, 60 validator node pillars, transparent OpenGov dome, golden CERE token flows",
        "aspect_ratio": "4:3"
    },
    "03_ddc_global_network": {
        "prompt": "World map with 63 glowing nodes, data streams, erasure coding inset, metrics: 99.9% uptime, 114ms response, cost comparison DDC vs AWS",
        "aspect_ratio": "16:9"
    },
    "04_data_processing_pipeline": {
        "prompt": "Factory cutaway: Event Service gateway, ETL processing floor with Kafka streams, DSC warehouse with ElasticSearch and PostgreSQL",
        "aspect_ratio": "16:9"
    },
    "05_ai_orchestration_center": {
        "prompt": "AI mission control: ROB drag-drop interface, Rule Service platform, Docker container pods, NFT agent marketplace",
        "aspect_ratio": "16:9"
    },
    "06_token_economics_flow": {
        "prompt": "Circular DAC system with 10-minute clock, Merkle trees, sentinel validators, automatic token distribution flows",
        "aspect_ratio": "1:1"
    },
    "07_infrastructure_stack": {
        "prompt": "Technical stack layers: hardware, Kubernetes, Kafka, microservices, monitoring, with 50k ops/sec gauge",
        "aspect_ratio": "4:3"
    },
    "08_developer_journey": {
        "prompt": "Developer timeline path: 0min start, 30min SDK integration, 60min deployment, with progress markers and achievements",
        "aspect_ratio": "16:9"
    },
    "09_paradigm_shift": {
        "prompt": "Before/after comparison: Traditional Cloud (dark pyramid) vs Cere Stack (bright network), transformation benefits",
        "aspect_ratio": "16:9"
    }
}

def load_status():
    """Load generation status from file"""
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, 'r') as f:
            return json.load(f)
    return {"generated": [], "failed": [], "last_attempt": None}

def save_status(status):
    """Save generation status to file"""
    status["last_attempt"] = datetime.now().isoformat()
    with open(STATUS_FILE, 'w') as f:
        json.dump(status, f, indent=2)

def generate_with_retry(client, filename, config, status, max_retries=3):
    """Generate single image with retry logic"""
    if filename in status["generated"]:
        print(f"✅ Already generated: {filename}")
        return True
    
    for attempt in range(max_retries):
        try:
            print(f"🔄 Generating {filename} (attempt {attempt + 1}/{max_retries})...")
            
            response = client.models.generate_content(
                model="gemini-2.5-flash-image",
                contents=[config["prompt"]],
                config=types.GenerateContentConfig(
                    response_modalities=['Image'],
                    image_config=types.ImageConfig(
                        aspect_ratio=config["aspect_ratio"],
                    )
                )
            )
            
            # Save the image
            for part in response.parts:
                if part.inline_data is not None:
                    image = part.as_image()
                    filepath = os.path.join(IMAGES_DIR, f"{filename}.png")
                    image.save(filepath)
                    
                    status["generated"].append(filename)
                    if filename in status["failed"]:
                        status["failed"].remove(filename)
                    save_status(status)
                    
                    print(f"✅ Saved: {filepath}")
                    return True
            
        except Exception as e:
            error_str = str(e)
            if "429" in error_str or "quota" in error_str.lower():
                print(f"⏳ Quota exceeded. Waiting 60 seconds before retry...")
                time.sleep(60)
            else:
                print(f"❌ Error: {error_str}")
                if attempt == max_retries - 1:
                    status["failed"].append(filename)
                    save_status(status)
    
    return False

def main():
    """Main generation function with resume capability"""
    print(f"📁 Images directory: {os.path.abspath(IMAGES_DIR)}")
    
    # Load previous status
    status = load_status()
    
    # Show current status
    print(f"\n📊 Current Status:")
    print(f"   ✅ Generated: {len(status['generated'])}")
    print(f"   ❌ Failed: {len(status['failed'])}")
    print(f"   ⏳ Remaining: {len(image_configs) - len(status['generated'])}")
    
    if status['last_attempt']:
        print(f"   🕒 Last attempt: {status['last_attempt']}")
    
    # Initialize client
    try:
        client = genai.Client(api_key=API_KEY)
    except Exception as e:
        print(f"❌ Failed to initialize Gemini client: {e}")
        return
    
    # Generate images
    success_count = 0
    for filename, config in image_configs.items():
        if generate_with_retry(client, filename, config, status):
            success_count += 1
        
        # Rate limiting between successful generations
        if success_count > 0 and filename != list(image_configs.keys())[-1]:
            print("⏳ Waiting 30 seconds before next image...")
            time.sleep(30)
    
    # Final summary
    print(f"\n✨ Generation Session Complete!")
    print(f"📊 Final Status:")
    print(f"   ✅ Total Generated: {len(status['generated'])}/{len(image_configs)}")
    print(f"   ❌ Failed: {len(status['failed'])}")
    
    if len(status['generated']) == len(image_configs):
        print(f"🎉 All images generated successfully!")
        create_gallery(status['generated'])

def create_gallery(filenames):
    """Create HTML gallery for generated images"""
    html = """<!DOCTYPE html>
<html>
<head>
    <title>Cere Stack - Generated Images</title>
    <style>
        body { background: #0B1929; color: white; font-family: Arial; padding: 20px; }
        h1 { color: #00D4FF; text-align: center; }
        .gallery { display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 20px; margin-top: 30px; }
        .image-card { background: rgba(255,255,255,0.05); border-radius: 8px; padding: 15px; }
        .image-card img { width: 100%; border-radius: 4px; }
        .status { text-align: center; margin: 20px; padding: 10px; background: rgba(0,212,255,0.1); border-radius: 5px; }
    </style>
</head>
<body>
    <h1>Cere Stack Article - Image Gallery</h1>
    <div class="status">Generated {count} images on {date}</div>
    <div class="gallery">
""".format(count=len(filenames), date=datetime.now().strftime('%Y-%m-%d %H:%M'))
    
    for filename in sorted(filenames):
        title = filename.replace('_', ' ').title()
        html += f"""
        <div class="image-card">
            <img src="{filename}.png" alt="{title}">
            <h3>{title}</h3>
        </div>
"""
    
    html += "</div></body></html>"
    
    gallery_path = os.path.join(IMAGES_DIR, "gallery.html")
    with open(gallery_path, 'w') as f:
        f.write(html)
    
    print(f"📸 Gallery created: {os.path.abspath(gallery_path)}")

if __name__ == "__main__":
    main()
