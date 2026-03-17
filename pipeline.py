#!/usr/bin/env python3
"""
Automated Quote Video Pipeline — Orchestrator

One command to rule them all:
    python pipeline.py                  # Full automated run
    python pipeline.py --dry-run        # Generate video but skip Instagram publish
    python pipeline.py --theme "stoicism"  # Curate quotes around a specific theme

Flow:
    1. Curate 5 viral quotes → present to user → HITL picks one
    2. Source stock photos (Pexels) + select mood-matched audio
    3. Generate video via VideoGenerator
    4. Generate viral caption + hashtags
    5. Publish to Instagram as Reel
"""

import sys, os, argparse, io

# Fix Windows console encoding for emoji support
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8', errors='replace')

# Ensure execution/ is on the path so VideoGenerator/Publisher imports work
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "execution"))

from agents.quote_curator import QuoteCurator
from agents.media_sourcer import MediaSourcer
from agents.caption_generator import CaptionGenerator
from execution.vid_generator import VideoGenerator
from execution.vid_publisher import VideoPublisher


def display_quotes(quotes):
    """Print 5 quotes for HITL selection."""
    print("\n" + "=" * 60)
    print("  🎬  QUOTE VIDEO GENERATOR — Pick Your Quote")
    print("=" * 60)
    for i, q in enumerate(quotes, 1):
        print(f"\n  [{i}]  \"{q['quote']}\"")
        print(f"        — {q['author']}  ({q['mood']}, {q['theme']})")
    print("\n" + "-" * 60)


def get_user_choice(quotes):
    """HITL: ask the user to pick a quote (1-5)."""
    while True:
        try:
            choice = input("\n  Enter your choice (1-5): ").strip()
            idx = int(choice) - 1
            if 0 <= idx < len(quotes):
                chosen = quotes[idx]
                print(f"\n  ✅ Selected: \"{chosen['quote']}\" — {chosen['author']}")
                return chosen
            else:
                print("  ⚠️  Please enter a number between 1 and 5.")
        except (ValueError, EOFError):
            print("  ⚠️  Please enter a valid number (1-5).")


def run_pipeline(theme="philosophy and life", dry_run=False):
    """Execute the full automated pipeline."""

    # ── Step 1: Curate Quotes ──────────────────────────────────
    print("\n🔍 Step 1/5: Curating quotes...")
    curator = QuoteCurator()
    quotes = curator.curate(theme=theme)
    display_quotes(quotes)

    # ── Step 2: HITL — Pick a quote ────────────────────────────
    chosen = get_user_choice(quotes)
    quote_text = chosen["quote"]
    author = chosen["author"]
    mood = chosen.get("mood", "reflective")
    quote_theme = chosen.get("theme", "philosophy")

    # ── Step 3: Source Media ───────────────────────────────────
    print("\n📸 Step 3/5: Sourcing images and audio...")
    sourcer = MediaSourcer()
    media = sourcer.source(mood=mood, theme=quote_theme)
    images_path = media["images_path"]
    audio_path = media["audio_path"]
    print(f"  Images: {images_path}")
    print(f"  Audio:  {audio_path}")

    # ── Step 4: Generate Video ─────────────────────────────────
    print("\n🎬 Step 4/5: Generating video...")
    output_name = "output.mp4"
    font = "fonts/font.ttf"

    vid_gen = VideoGenerator(
        quote=quote_text,
        author_name=author,
        output_name=output_name,
        imagesPath=images_path,
        font=font,
        audio_path=audio_path,
        randomImages=False,
    )
    vid_gen.generate()
    print(f"  ✅ Video saved: {output_name}")

    # ── Step 5: Generate Caption & Publish ─────────────────────
    print("\n✍️  Step 5/5: Generating caption...")
    caption_gen = CaptionGenerator()
    caption = caption_gen.generate(quote=quote_text, author=author, mood=mood)

    print("\n--- Preview Caption ---")
    print(caption)
    print("-" * 40)

    if dry_run:
        print("\n🏁 Dry run complete! Skipping Instagram publish.")
        print(f"   Video: {output_name}")
    else:
        print("\n📤 Publishing to Instagram...")
        publisher = VideoPublisher(caption=caption, file_path=f"./{output_name}")
        status_code = publisher.publish_video()
        print(f"\n🎉 Published! Status code: {status_code}")

    # Cleanup temp images
    sourcer.cleanup()

    print("\n✅ Pipeline complete!")


def main():
    parser = argparse.ArgumentParser(
        description="Automated Quote Video Generator & Instagram Publisher"
    )
    parser.add_argument(
        "--theme", type=str, default="philosophy and life",
        help="Theme/mood for quote curation (e.g., 'stoicism', 'dark motivation', 'love')"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Generate video but skip Instagram publishing"
    )

    args = parser.parse_args()
    run_pipeline(theme=args.theme, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
