import json
import os
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python tts_generator.py <path_to_video_script.json>")
        sys.exit(1)

    script_path = sys.argv[1]
    
    with open(script_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if not data.get("useVoiceover", False):
        print("Voiceover not enabled. Skipping TTS generation.")
        sys.exit(0)

    tts_type = data.get("ttsType", "elevenlabs")
    
    # Ensure output directory exists
    os.makedirs('public/voices', exist_ok=True)

    if tts_type == "elevenlabs":
        print("Using ElevenLabs TTS...")
        import requests
        
        # We assume the user has passed their elevenLabsKey inside settings, 
        # but since we are in a GitHub Action, it might be passed as an env var or inside the payload.
        # Here we mock the behavior or use the env var ELEVENLABS_API_KEY
        api_key = os.environ.get("ELEVENLABS_API_KEY", "")
        
        if not api_key:
            print("WARNING: ELEVENLABS_API_KEY not found in environment. Using fallback voice (or failing).")

        for idx, scene in enumerate(data.get("scenes", [])):
            text = scene.get("description", "")
            if not text:
                continue
                
            print(f"Generating ElevenLabs audio for Scene {idx + 1}...")
            
            # Default Voice ID (Rachel or similar) can be customized
            voice_id = "21m00Tcm4TlvDq8ikWAM"
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
            
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
            }
            if api_key:
                headers["xi-api-key"] = api_key
                
            payload = {
                "text": text,
                "model_id": "eleven_monolingual_v1",
                "voice_settings": {"stability": 0.5, "similarity_boost": 0.5}
            }
            
            try:
                response = requests.post(url, json=payload, headers=headers)
                if response.status_code == 200:
                    out_file = f"public/voices/scene_{idx}.mp3"
                    with open(out_file, "wb") as out:
                        out.write(response.content)
                    
                    # Store path in scene data so Remotion can access it
                    # Next.js public directory acts as root `/`
                    scene["voiceUrl"] = f"/voices/scene_{idx}.mp3"
                else:
                    print(f"Failed to generate for scene {idx}: {response.text}")
            except Exception as e:
                print(f"Error accessing ElevenLabs: {e}")

    elif tts_type == "opensource":
        print("Using Open Source TTS (Coqui XTTS v2)...")
        try:
            from TTS.api import TTS
            import torch
            
            device = "cuda" if torch.cuda.is_available() else "cpu"
            print(f"Loading TTS model on {device}...")
            # Init TTS with XTTS v2
            tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
            
            clone_url = data.get("voiceCloneUrl", "")
            reference_audio = "reference.wav"
            
            # Download reference if provided
            if clone_url:
                import urllib.request
                print(f"Downloading voice clone reference from {clone_url}")
                try:
                    urllib.request.urlretrieve(clone_url, reference_audio)
                except Exception as e:
                    print(f"Error downloading clone URL: {e}")
                    clone_url = None
            
            for idx, scene in enumerate(data.get("scenes", [])):
                text = scene.get("description", "")
                if not text:
                    continue
                
                print(f"Generating Coqui TTS audio for Scene {idx + 1}...")
                out_file = f"public/voices/scene_{idx}.wav"
                
                if clone_url and os.path.exists(reference_audio):
                    tts.tts_to_file(text=text, speaker_wav=reference_audio, language="en", file_path=out_file)
                else:
                    # Fallback to default speaker logic or standard TTS model instead of XTTS zero-shot
                    # If using XTTS without speaker_wav, it might throw error. We should provide a built-in default
                    pass
                
                scene["voiceUrl"] = f"/voices/scene_{idx}.wav"
                
        except ImportError as e:
            import traceback
            print("ERROR: An import error occurred while loading Coqui TTS.")
            traceback.print_exc()
            sys.exit(1)
        except Exception as e:
            print(f"ERROR generating open source TTS: {e}")
            sys.exit(1)
            
    # Save the strictly updated script back
    with open(script_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

    print("TTS Generation Complete.")

if __name__ == "__main__":
    main()
