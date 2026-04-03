# **📜 Primary Task: Quote2Vid Swarm Orchestration**

## **1\. Objective**

The mission of this swarm is to evolve the existing Quote2Vid CLI codebase into a commercially viable, high-performance automated content engine. The orchestration focuses on transitioning from a static script-based execution to a scalable, state-driven architecture suitable for a multi-tenant SaaS or professional GUI, while maintaining the integrity of the media generation pipeline.

## **2\. The Law (Nomological Constraints)**

The Law governs the behavior and decision-making boundaries of all Practitioners within the swarm.

* **Thematic Boundary**: Content generation is strictly limited to the niche of **Wisdom and Timeless Quotes**. No expansion into other niches is permitted.  
* **Architectural Continuity**: The **GitHub-Base64-to-CDN** methodology for media ingestion must be maintained for the MVP phase. Direct cloud storage migrations are prohibited until the MVP is stabilized.  
* **Visual Standards**: All output must adhere to strict aspect ratios (9:16 for Reels, 1:1 for Posts) and include the mandatory @quill\_of\_humanity watermark.  
* **Asset Logic**: Background visual dimming and text legibility are non-negotiable quality constraints.  
* **Rate Compliance**: All interactions with external APIs (ZenQuotes, Wikipedia, Facebook Graph) must implement exponential backoff and respect rate limits.

## **3\. The Practitioners (Agentic Roles)**

* **The Systems Architect**: Responsible for refactoring the state management logic. Tasks include moving from input\_parameters.py to a more robust data ingestion pattern.  
* **The Media Engineer**: Specializes in the MoviePy and PIL pipelines. Primary focus is on "SmartCrop" utilities and transition effects (e.g., cross-fades, Ken Burns effect).  
* **The Cognitive Specialist**: Manages the AI Enrichment layer. Handles Gemini API prompts for sentiment-based styling, audio selection, and contextual captions.  
* **The Publisher Bot**: Manages the publication lifecycle, including the GitHub upload hack and the Instagram Graph API polling loop.

## **4\. The Apparatus (Technical Interface)**

* **Core Codebase**: Direct write-access to the Python source files in the existing directory structure.  
* **AI Models**: Access to Gemini 2.5 Flash for reasoning and sentiment analysis.  
* **Third-Party APIs**: ZenQuotes (content), Wikipedia (thumbnails), and Facebook Graph API (distribution).  
* **Execution Environment**: Python 3.x with dependencies: moviepy, Pillow, requests, and google-generativeai.

## **5\. Success Metrics**

* Reliable generation of quote-accurate vertical videos and square posts.  
* Successful automated publishing to Instagram via the GitHub CDN bypass.  
* Refactored code structure that supports easy integration with a future Streamlit or Gradio interface.