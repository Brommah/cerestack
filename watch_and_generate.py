#!/usr/bin/env python3
"""
Watch for changes in article sections and automatically regenerate the full article.
This ensures the full article is always in sync with individual section edits.
"""

import os
import sys
import time
from pathlib import Path
from datetime import datetime

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
except ImportError:
    print("Error: watchdog module not installed.")
    print("Install it with: pip3 install watchdog")
    print("\nAlternatively, run generate_article.py manually after each edit.")
    sys.exit(1)

# Import the generate function from our other script
from generate_article import generate_full_article

class ArticleHandler(FileSystemEventHandler):
    """Handle file changes in article sections."""
    
    def __init__(self):
        self.section_files = {
            'introduction.md',
            'layer1-blockchain.md',
            'layer2-data-infrastructure.md',
            'layer3-data-processing.md',
            'layer4-ai-orchestration.md',
            'layer5-validation-economics.md',
            'layer6-infrastructure.md',
            'layer7-developer-tools.md',
            'conclusion.md'
        }
        self.last_update = 0
        self.update_delay = 1  # Debounce delay in seconds
    
    def on_modified(self, event):
        """Handle file modification events."""
        if event.is_directory:
            return
        
        filename = os.path.basename(event.src_path)
        
        # Check if it's one of our section files
        if filename in self.section_files:
            # Debounce rapid changes
            current_time = time.time()
            if current_time - self.last_update < self.update_delay:
                return
            
            self.last_update = current_time
            print(f"\n🔄 Detected change in: {filename}")
            print(f"   Regenerating full article...")
            
            try:
                generate_full_article()
                print(f"   ✅ Article regenerated at {datetime.now().strftime('%H:%M:%S')}")
            except Exception as e:
                print(f"   ❌ Error regenerating article: {e}")

def main():
    """Main watch loop."""
    print("📁 Cere Stack Article Watch Mode")
    print("================================")
    print("Watching for changes in article sections...")
    print("The full article will auto-regenerate when you save any section.")
    print("\nPress Ctrl+C to stop watching.\n")
    
    # Initial generation
    print("🚀 Generating initial full article...")
    generate_full_article()
    
    # Set up file watcher
    event_handler = ArticleHandler()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=False)
    
    # Start watching
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n\n👋 Stopped watching. Goodbye!")
    
    observer.join()

if __name__ == "__main__":
    # Change to the script's directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Start watching
    main()
