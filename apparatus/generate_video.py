import sys
import os
import json

# Deterministic Mechanical Executor for Video Generation
# Layer III: The Apparatus

# Add the 'src' directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
src_path = os.path.join(project_root, 'src')
sys.path.append(src_path)

def execute_generation():
    """
    Blindly executes the generation logic defined by the Practitioners
    via the central controller.
    """
    try:
        from controller import QuoteEngine
        
        engine = QuoteEngine()
        result = engine.run_full_pipeline()
        
        video_path = result.get("video")
        
        if video_path and os.path.exists(os.path.join(project_root, video_path)):
            status = {
                "status": "SUCCESS",
                "exit_code": 0,
                "message": "Video generated successfully",
                "artifacts": {
                    "video": video_path,
                    "image": result.get("image")
                }
            }
        else:
            status = {
                "status": "FAILURE",
                "exit_code": 1,
                "message": "Video generation completed but output file not found."
            }
            
    except Exception as e:
        status = {
            "status": "ERROR",
            "exit_code": 1,
            "message": f"Execution failed with error: {str(e)}"
        }

    # Deterministic structured output for the Law to verify
    print(json.dumps(status, indent=2))
    return status["exit_code"]

if __name__ == "__main__":
    sys.exit(execute_generation())
