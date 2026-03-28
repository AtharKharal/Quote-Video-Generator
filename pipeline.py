#!/usr/bin/env python3
"""
Automated Quote Video Pipeline — Compact Orchestrator
"""

import sys, os, argparse, io
from agents import QuoteCurator, MediaSourcer, CaptionGenerator
from execution import VideoGenerator, VideoPublisher

# Fix Windows console encoding
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def pick_quote(quotes):
    print("\n" + "=" * 40 + "\n🎬 PICK YOUR QUOTE\n" + "=" * 40)
    for i, q in enumerate(quotes, 1):
        print(f"[{i}] \"{q['quote']}\" — {q['author']}")
    while True:
        try:
            choice = int(input("\nChoice (1-5): "))
            if 1 <= choice <= 5: return quotes[choice-1]
        except (ValueError, EOFError): pass
        print("Invalid choice.")

def run_pipeline(theme="philosophy", dry_run=False):
    print(f"🔍 Step 1: Curating '{theme}'...")
    quotes = QuoteCurator().curate(theme=theme)
    chosen = pick_quote(quotes)
    
    print("📸 Step 2: Sourcing media...")
    sourcer = MediaSourcer()
    media = sourcer.source(mood=chosen['mood'], theme=chosen['theme'])
    
    print("🎬 Step 3: Generating video...")
    VideoGenerator(
        quote=chosen['quote'], author_name=chosen['author'],
        output_name="output.mp4", imagesPath=media['images_path'],
        font="fonts/font.ttf", audio_path=media['audio_path'], randomImages=False
    ).generate()

    print("✍️  Step 4: Generating caption...")
    caption = CaptionGenerator().generate(quote=chosen['quote'], author=chosen['author'], mood=chosen['mood'])
    
    if dry_run:
        print("\n🏁 Dry run complete! Output: output.mp4")
    else:
        print("📤 Publishing to Instagram...")
        status = VideoPublisher(caption=caption, file_path="./output.mp4").publish_video()
        print(f"🎉 Success! Status: {status}")

    sourcer.cleanup()
    print("\n✅ Done!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--theme", default="philosophy")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    run_pipeline(theme=args.theme, dry_run=args.dry_run)
