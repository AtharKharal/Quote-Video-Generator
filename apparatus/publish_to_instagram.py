import sys
import os
import json
import argparse

# Deterministic Mechanical Executor for Instagram Publication
# Layer III: The Apparatus

# Add the 'src' directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
src_path = os.path.join(project_root, 'src')
sys.path.append(src_path)

def execute_publication(file_path):
    """
    Blindly executes the publication logic as defined by the Practitioners.
    Handles the transition from local file -> GitHub CDN -> Instagram Graph API.
    """
    try:
        from publisher import Publisher
        from controller import QuoteEngine
        
        # Handle relative/absolute paths
        if not os.path.isabs(file_path):
            file_path = os.path.join(project_root, file_path)

        if not os.path.exists(file_path):
             return {
                 "status": "ERROR", 
                 "exit_code": 1, 
                 "message": f"File not found: {file_path}"
             }

        # Initialize engine and enrich content to get metadata
        # (This follows the Cognitive Specialist's protocols for captioning)
        engine = QuoteEngine()
        engine.enrich_content()
        
        caption = engine.input_dict.get("caption", "Wisdom for today.")
        hashtags = " ".join(engine.input_dict.get("hashtags", []))
        full_caption = f"{caption}\n\n{hashtags}\n\nfollow @quill_of_humanity for more!"

        publisher = Publisher(full_caption, file_path)
        
        # Determine publish type based on extension
        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".mp4":
            publish_type = "video"
        elif ext in [".png", ".jpg", ".jpeg"]:
            publish_type = "image"
        else:
            return {
                "status": "ERROR",
                "exit_code": 1,
                "message": f"Unsupported file type: {ext}"
            }

        print(f"Initiating {publish_type} publication for {os.path.basename(file_path)}...")
        status_code = publisher.publish(publish_type)
        
        # Standard Facebook Graph API success codes are 200/201
        if status_code in [200, 201]:
            return {
                "status": "SUCCESS",
                "exit_code": 0,
                "message": f"Published {publish_type} successfully to Instagram.",
                "response_code": status_code
            }
        else:
            return {
                "status": "FAILURE",
                "exit_code": 1,
                "message": f"Publication failed with status code: {status_code}"
            }
            
    except Exception as e:
        return {
            "status": "ERROR",
            "exit_code": 1,
            "message": f"Publication execution failed with critical error: {str(e)}"
        }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Apparatus for Instagram Publication")
    parser.add_argument("--file", required=True, help="Path to the video or image file to publish")
    args = parser.parse_args()
    
    result = execute_publication(args.file)
    # Output result as JSON for the Law's validation step
    print(json.dumps(result, indent=2))
    sys.exit(result["exit_code"])
