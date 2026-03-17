"""Quick validation script for the automated pipeline agents."""
import sys, os, io

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, os.path.dirname(__file__))

def test_quote_curator():
    print("=" * 50)
    print("TEST 1: QuoteCurator (fallback mode)")
    print("=" * 50)
    from agents.quote_curator import QuoteCurator
    qc = QuoteCurator()
    quotes = qc.curate("stoicism")
    assert len(quotes) == 5, f"Expected 5 quotes, got {len(quotes)}"
    for i, q in enumerate(quotes, 1):
        print(f"  [{i}] \"{q['quote']}\" — {q['author']} ({q['mood']})")
    assert all(k in quotes[0] for k in ("quote", "author", "mood", "theme")), "Missing keys"
    print("  ✅ PASS: Got 5 quotes with correct structure\n")

def test_media_sourcer():
    print("=" * 50)
    print("TEST 2: MediaSourcer (fallback mode)")
    print("=" * 50)
    from agents.media_sourcer import MediaSourcer
    ms = MediaSourcer()
    result = ms.source(mood="melancholic", theme="solitude")
    assert "images_path" in result, "Missing images_path"
    assert "audio_path" in result, "Missing audio_path"
    assert os.path.exists(result["audio_path"]), f"Audio not found: {result['audio_path']}"
    print(f"  Images: {result['images_path']}")
    print(f"  Audio:  {result['audio_path']}")
    print("  ✅ PASS: Media sourced successfully\n")

def test_caption_generator():
    print("=" * 50)
    print("TEST 3: CaptionGenerator (fallback mode)")
    print("=" * 50)
    from agents.caption_generator import CaptionGenerator
    cg = CaptionGenerator()
    caption = cg.generate(
        quote="We suffer more often in imagination than in reality.",
        author="Seneca",
        mood="reflective"
    )
    assert len(caption) > 50, "Caption too short"
    assert "@quill_of_humanity" in caption, "Missing account handle"
    assert "#quotes" in caption, "Missing hashtags"
    print(f"  Caption length: {len(caption)} chars")
    print(f"  First line: {caption.split(chr(10))[0]}")
    print("  ✅ PASS: Caption generated with handle + hashtags\n")

def test_input_builder():
    print("=" * 50)
    print("TEST 4: Input Builder (refactored input.py)")
    print("=" * 50)
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "execution"))
    from input import build_input, input_dict
    
    # Test build_input
    cfg = build_input(quote="Test quote", author="Test Author")
    assert cfg["quote"] == "Test quote"
    assert cfg["author"] == "Test Author"
    assert cfg["outputName"] == "output.mp4"
    print(f"  build_input: {list(cfg.keys())}")
    
    # Test backward compat
    assert "quote" in input_dict, "input_dict missing quote"
    print(f"  input_dict backward compat: OK (quote='{input_dict['quote'][:40]}...')")
    print("  ✅ PASS: Config builder works correctly\n")

def test_pipeline_import():
    print("=" * 50)
    print("TEST 5: Pipeline module imports")
    print("=" * 50)
    from pipeline import run_pipeline, display_quotes, get_user_choice
    print("  Imported: run_pipeline, display_quotes, get_user_choice")
    print("  ✅ PASS: All pipeline imports resolve\n")

if __name__ == "__main__":
    print("\n🔬 AUTOMATED PIPELINE VALIDATION\n")
    test_quote_curator()
    test_media_sourcer()
    test_caption_generator()
    test_input_builder()
    test_pipeline_import()
    print("=" * 50)
    print("🎉 ALL 5 TESTS PASSED!")
    print("=" * 50)
