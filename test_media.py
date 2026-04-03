import os
import sys
from moviepy import AudioFileClip, ColorClip, CompositeVideoClip

def diagnostics():
    print("--- Quote2Vid Diagnostic Tool ---")
    
    # Check for basic assets
    assets = ["fonts/font.ttf", "audios/1.mp3", "images/images1"]
    for asset in assets:
        exists = os.path.exists(asset)
        print(f"Checking {asset}: {'EXISTS' if exists else 'MISSING'}")
        
    # Test MoviePy Audio Injection
    print("\nTesting MoviePy Audio Injection...")
    try:
        audio_file = "audios/10.mp3"
        if not os.path.exists(audio_file):
            audio_file = [f for f in os.listdir("audios") if f.endswith(".mp3")][0]
            audio_file = os.path.join("audios", audio_file)
            
        audio = AudioFileClip(audio_file)
        duration = min(3, audio.duration)
        
        # Create a simple 3-second red clip
        clip = ColorClip(size=(640, 480), color=(255, 0, 0), duration=duration)
        clip = clip.with_audio(audio.with_duration(duration))
        
        output = "diagnostic_test.mp4"
        clip.write_videofile(output, codec="libx264", audio_codec="aac", fps=24, logger=None)
        
        if os.path.exists(output):
            print(f"SUCCESS: Diagnostic video generated at {output}")
            print("Please check if THIS file has audio. If yes, the main generator should also work.")
        else:
            print("FAILURE: Diagnostic video was not created.")
            
    except Exception as e:
        print(f"ERROR: MoviePy diagnostic failed: {e}")

if __name__ == "__main__":
    diagnostics()
