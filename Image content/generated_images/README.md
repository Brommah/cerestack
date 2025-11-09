# Generated Images for Cere Stack Article

## 📁 Storage Location
All images will be saved in this directory: `/Users/martijnblue/Article/generated_images/`

## 🖼️ Image Files (When Generated)

1. **01_cerebellum_to_cephalum.png** (16:9)
   - Split brain analogy showing cerebellum/cephalum parallel
   
2. **02_blockchain_foundation.png** (4:3)
   - Isometric view of blockchain infrastructure with validators
   
3. **03_ddc_global_network.png** (16:9)
   - World map with 63 nodes and performance metrics
   
4. **04_data_processing_pipeline.png** (16:9)
   - Factory cutaway of 3-stage data processing
   
5. **05_ai_orchestration_center.png** (16:9)
   - Mission control center with ROB interface
   
6. **06_token_economics_flow.png** (1:1)
   - Circular DAC system and token distribution
   
7. **07_infrastructure_stack.png** (4:3)
   - Technical layers from hardware to monitoring
   
8. **08_developer_journey.png** (16:9)
   - Timeline path from 0 to 60 minutes deployment
   
9. **09_paradigm_shift.png** (16:9)
   - Before/after comparison infographic

## 🎨 Gallery
- **gallery.html** - Visual gallery of all generated images

## 📊 Status Tracking
- **generation_status.json** - Tracks which images have been generated

## ⚠️ Current Status
The Gemini API key has exceeded its free tier quota. Options:
1. Wait for quota reset (daily limit)
2. Upgrade to paid tier
3. Use alternative image generation services

## 🔄 Retry Script
Use `generate_images_retry.py` to resume generation when quota is available:
```bash
python3 generate_images_retry.py
```

This script will:
- Track which images were already generated
- Handle quota errors gracefully
- Resume where it left off
- Create an HTML gallery when complete
