#!/usr/bin/env python3
"""
Generate images for Cere Stack article using Google Gemini API
"""

import os
from google import genai
from google.genai import types
from PIL import Image
from datetime import datetime
import time

# Configure the API key
API_KEY = "AIzaSyAxmDebE_c-LDZ-CCPVTbiiDojuXlj45JA"
client = genai.Client(api_key=API_KEY)

# Create images directory
IMAGES_DIR = "generated_images"
os.makedirs(IMAGES_DIR, exist_ok=True)

print(f"📁 Images will be saved to: {os.path.abspath(IMAGES_DIR)}")

# Define all image prompts based on the infographic guide
image_prompts = {
    "intro_cerebellum": {
        "prompt": (
            "Create a high-quality technical illustration showing a split-screen comparison: "
            "On the left side, show a detailed anatomical view of the human cerebellum with glowing neural pathways. "
            "On the right side, show a modern digital architecture diagram with layers 1-3 labeled as 'Cere' at the bottom "
            "(shown as infrastructure blocks) and layers 4-7 labeled as 'CEF' at the top (shown as intelligence modules). "
            "Connect both sides with flowing data streams that transition from organic neurons to digital data packets. "
            "Use a color gradient from warm biological colors (oranges/reds) on the left to cool digital colors (blues/cyans) on the right. "
            "Professional technical illustration style, clean and modern."
        ),
        "filename": "01_cerebellum_to_cephalum.png",
        "aspect_ratio": "16:9"
    },
    
    "layer1_blockchain": {
        "prompt": (
            "Create an isometric 3D technical diagram of a blockchain foundation architecture: "
            "Show a solid substrate base as dark blue bedrock with the text 'Substrate Blockchain' embossed on it. "
            "Rising from this foundation, depict 60 glowing validator nodes as illuminated crystal pillars of varying heights. "
            "Above the pillars, show a transparent dome representing OpenGov with visible voting flows inside. "
            "Add golden CERE token particles flowing between the pillars like energy streams. "
            "Include labels: 'Validators: 50-70 nodes', 'Delegated Proof of Stake', 'OpenGov Governance'. "
            "Use a dark background with blue and gold color scheme. Ultra-detailed, professional infographic style."
        ),
        "filename": "02_blockchain_foundation.png",
        "aspect_ratio": "4:3"
    },
    
    "layer2_ddc": {
        "prompt": (
            "Create a world map visualization showing the DDC (Decentralized Data Clusters) global network: "
            "Display a dark world map with exactly 63 bright cyan nodes distributed across all continents. "
            "Connect the nodes with animated-looking data stream lines that glow. "
            "Include a detailed inset diagram in the top corner showing erasure coding: data being split into fragments. "
            "Add performance metrics overlay: '99.9% Uptime', '114ms Response Time', 'Billions of Transactions'. "
            "Bottom corner should show cost comparison bar chart: 'DDC: $0.01/GB' vs 'AWS S3: $0.07/GB'. "
            "Label prominently: 'Dragon 1 Production Cluster - 63 Global Nodes'. "
            "Dark theme with cyan and white accents, professional dashboard style."
        ),
        "filename": "03_ddc_global_network.png",
        "aspect_ratio": "16:9"
    },
    
    "layer3_pipeline": {
        "prompt": (
            "Create a detailed factory-style cutaway diagram showing the data processing pipeline with three distinct stages: "
            "Stage 1 (Event Service): Show a large funnel labeled 'REST API Gateway' with data packets entering, "
            "include a security checkpoint for 'Signature Validation' and an 'Enrichment Station' adding metadata. "
            "Stage 2 (ETL Service): Display a complex processing floor with branching conveyor belts - one path labeled "
            "'Batch Processing' and another 'Real-time Events'. Show Kafka streams as glowing pipes connecting sections. "
            "Stage 3 (DSC): Illustrate a massive warehouse with two sections - 'ElasticSearch' (unstructured data filing cabinets) "
            "and 'PostgreSQL' (structured storage shelves). Show 'Rafts' as indexed data containers. "
            "Include performance gauges showing 'Sub-second latency' and '100 events/batch'. "
            "Industrial blueprint style with cutaway view, blue and orange color scheme."
        ),
        "filename": "04_data_processing_pipeline.png",
        "aspect_ratio": "16:9"
    },
    
    "layer4_ai_control": {
        "prompt": (
            "Create a futuristic AI mission control center with multiple interconnected panels: "
            "Center screen: Large holographic display showing 'ROB - Real-time Orchestration Builder' with visible drag-and-drop "
            "workflow interface, agents being connected with glowing lines. "
            "Left panel: 'Rule Service Conductor' platform with event pattern matching visualizations and trigger flows. "
            "Right panel: 'Agent Runtime' showing isolated Docker containers as glowing pods, each with resource meters "
            "(CPU, GPU, RAM usage bars). Include temporary EDEK keys floating between pods. "
            "Top panel: 'Agent Registry Marketplace' displaying agents as NFT cards with performance metrics and star ratings. "
            "Bottom: Show 'Cubbies' as encrypted shared memory spaces connecting agents. "
            "Sci-fi holographic interface style, dark background with neon blue and purple accents."
        ),
        "filename": "05_ai_orchestration_center.png",
        "aspect_ratio": "16:9"
    },
    
    "layer5_economics": {
        "prompt": (
            "Create a circular economic flow diagram centered around the DAC (Data Activity Capture) system: "
            "Center: Large circular hub labeled 'DAC System' with a prominent 10-minute countdown clock. "
            "Inner ring: Show Merkle tree formations aggregating data activities into cryptographic proofs. "
            "Middle ring: 'Sentinel Validators' as watchtowers with scanning beams doing spot-checks on operations. "
            "Outer ring: Show automatic token flows - green streams flowing to 'Node Operators', 'Validators', "
            "and 'Developers' based on contributions. Red lightning bolts for 'Slashing Events' when misbehavior detected. "
            "Include sections for 'Treasury Fees', 'Cluster Reserves', and 'Staking Rewards'. "
            "Bottom: Real-time dashboard showing 'Micro-payments: $0.001/operation' and transaction throughput. "
            "Circular infographic style with clockwise flow, green/red/gold color scheme on dark background."
        ),
        "filename": "06_token_economics_flow.png",
        "aspect_ratio": "1:1"
    },
    
    "layer6_infrastructure": {
        "prompt": (
            "Create a technical infrastructure stack diagram showing layers from bottom to top: "
            "Base layer: Server hardware rack with specifications '8+ CPU cores, NVMe storage, 10Gbps network'. "
            "Layer 2: Kubernetes orchestration plane with container pods and service mesh. "
            "Layer 3: Kafka messaging backbone shown as interconnected data pipelines. "
            "Layer 4: Microservices constellation with labeled services: 'WebSocket Service', 'AI Gateway', "
            "'DDV Viewer', 'Blockchain Indexer'. "
            "Layer 5: Monitoring plane with Grafana dashboards showing real-time metrics. "
            "Side panel: Large speedometer showing '50,000 ops/sec' performance metric. "
            "Include labels for 'CI/CD Pipeline', 'Better Stack', 'Sentry' monitoring tools. "
            "Technical blueprint style, clean lines, blue and gray color scheme with orange highlights."
        ),
        "filename": "07_infrastructure_stack.png",
        "aspect_ratio": "4:3"
    },
    
    "layer7_developer": {
        "prompt": (
            "Create a developer journey timeline path illustration: "
            "Starting point (0 min): Developer at laptop with 'Download SDK' hover animation. "
            "15 min mark: 'Wallet SDK Integration' milestone showing key generation visualization. "
            "30 min mark: 'Building & Coding' phase with floating code snippets and API calls. "
            "45 min mark: 'Testing & Debugging' with error handling examples. "
            "60 min mark: 'Production Deployment' with success checkmark and confetti. "
            "Along the path show SDK icons: 'Cere Wallet SDK', 'Media SDK', 'DDC SDK'. "
            "Include achievement badges at each milestone and a progress bar at bottom. "
            "Side annotations: 'Multi-chain Support', 'Client-side Encryption', 'Zero to Hero in 1 Hour'. "
            "Friendly, gamified style with bright colors, isometric view of the journey path."
        ),
        "filename": "08_developer_journey.png",
        "aspect_ratio": "16:9"
    },
    
    "conclusion_paradigm": {
        "prompt": (
            "Create a powerful before/after comparison infographic titled 'The Paradigm Shift': "
            "Left side labeled 'Traditional Cloud': Show a dark pyramid with 'Corporate Control' at top, "
            "'Black Box Operations', 'Trust Us' messaging, locked data silos, centralized servers. "
            "Right side labeled 'Cere Stack': Show a bright distributed network with 'User Sovereignty', "
            "'Transparent Operations', 'Verifiable Proofs', interconnected data flows, decentralized nodes. "
            "Center: Large arrow showing transformation with floating benefits: '7x Cheaper', '99.9% Uptime', "
            "'1-Hour Deployment', 'Complete Privacy', 'Fair Economics'. "
            "Bottom: Dragon 1 production stats dashboard and call-to-action 'Join the Revolution at cere.network'. "
            "Use contrasting colors - dark/red for traditional, bright/green for Cere Stack. "
            "Professional infographic style with clear visual hierarchy."
        ),
        "filename": "09_paradigm_shift.png",
        "aspect_ratio": "16:9"
    }
}

def generate_images():
    """Generate all images using Gemini API"""
    
    print(f"\n🎨 Starting image generation for {len(image_prompts)} images...")
    print(f"⏱️  Estimated time: {len(image_prompts) * 15} seconds\n")
    
    generated_files = []
    
    for key, config in image_prompts.items():
        print(f"🔄 Generating {key}...")
        
        try:
            # Generate image with Gemini
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
            
            # Save the generated image
            for part in response.parts:
                if part.inline_data is not None:
                    image = part.as_image()
                    filepath = os.path.join(IMAGES_DIR, config["filename"])
                    image.save(filepath)
                    generated_files.append(filepath)
                    print(f"✅ Saved: {filepath}")
                    break
            
            # Rate limiting - be respectful of the API
            time.sleep(10)
            
        except Exception as e:
            print(f"❌ Error generating {key}: {str(e)}")
            continue
    
    return generated_files

def create_image_gallery_html(image_files):
    """Create an HTML gallery to view all generated images"""
    
    html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Cere Stack - Generated Images</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #0B1929;
            color: white;
            padding: 20px;
        }
        h1 {
            color: #00D4FF;
            text-align: center;
        }
        .gallery {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }
        .image-card {
            background: rgba(255,255,255,0.05);
            border-radius: 8px;
            padding: 15px;
            border: 1px solid rgba(0,212,255,0.3);
        }
        .image-card img {
            width: 100%;
            height: auto;
            border-radius: 4px;
        }
        .image-title {
            margin-top: 10px;
            color: #00D4FF;
            font-weight: bold;
        }
        .timestamp {
            text-align: center;
            color: #888;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <h1>Cere Stack Article - Generated Images</h1>
    <p class="timestamp">Generated on: {timestamp}</p>
    <div class="gallery">
"""
    
    for filepath in image_files:
        filename = os.path.basename(filepath)
        title = filename.replace('.png', '').replace('_', ' ').title()
        html_content += f"""
        <div class="image-card">
            <img src="{filename}" alt="{title}">
            <div class="image-title">{title}</div>
        </div>
"""
    
    html_content += """
    </div>
</body>
</html>
"""
    
    gallery_path = os.path.join(IMAGES_DIR, "gallery.html")
    with open(gallery_path, 'w') as f:
        f.write(html_content.format(timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    
    print(f"\n📸 Gallery created: {os.path.abspath(gallery_path)}")

if __name__ == "__main__":
    # Generate all images
    generated_files = generate_images()
    
    # Create gallery
    if generated_files:
        create_image_gallery_html(generated_files)
    
    # Summary
    print(f"\n✨ Generation Complete!")
    print(f"📁 Images saved to: {os.path.abspath(IMAGES_DIR)}")
    print(f"🖼️  Total images generated: {len(generated_files)}")
    print(f"\n📋 Generated files:")
    for f in generated_files:
        print(f"   - {f}")
