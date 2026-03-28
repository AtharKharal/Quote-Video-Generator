"""
Updated validation script for the compact automated pipeline structure.
"""
import os, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, os.path.dirname(__file__))

from agents import QuoteCurator, MediaSourcer, CaptionGenerator
from pipeline import run_pipeline

def test_all():
    print("🔬 TESTING COMPACT PIPELINE AGENTS\n" + "="*40)
    
    # 1. QuoteCurator
    qc = QuoteCurator()
    quotes = qc.curate("stoicism")
    assert len(quotes) == 5, "Should have 5 quotes"
    print(f"✅ QuoteCurator: Got {len(quotes)} quotes.")

    # 2. MediaSourcer
    ms = MediaSourcer()
    media = ms.source(mood="melancholic", theme="nature")
    assert os.path.exists(media["images_path"]), "Images path missing"
    assert os.path.exists(media["audio_path"]), f"Audio {media['audio_path']} missing"
    print(f"✅ MediaSourcer: Images in {media['images_path']}, Audio: {media['audio_path']}")
    ms.cleanup()

    # 3. CaptionGenerator
    cg = CaptionGenerator()
    caption = cg.generate(quote="Test", author="Test Author", mood="calm")
    assert "@quill_of_humanity" in caption or "#quotes" in caption, "Caption invalid"
    print(f"✅ CaptionGenerator: Generated '{caption.splitlines()[0]}...'")

    print("="*40 + "\n🎉 ALL TESTS PASSED!")

if __name__ == "__main__":
    test_all()
