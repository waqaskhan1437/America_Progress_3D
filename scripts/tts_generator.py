import json
import os
import sys
import asyncio

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

        api_key = os.environ.get("ELEVENLABS_API_KEY", "")

        if not api_key:
            print("WARNING: ELEVENLABS_API_KEY not found. Falling back to edge-tts.")
            tts_type = "opensource"
        else:
            for idx, scene in enumerate(data.get("scenes", [])):
                text = scene.get("description", "")
                if not text:
                    continue

                print(f"Generating ElevenLabs audio for Scene {idx + 1}...")

                voice_id = "21m00Tcm4TlvDq8ikWAM"
                url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

                headers = {
                    "Accept": "audio/mpeg",
                    "Content-Type": "application/json",
                    "xi-api-key": api_key,
                }

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
                        scene["voiceUrl"] = f"/voices/scene_{idx}.mp3"
                        print(f"  -> Saved {out_file}")
                    else:
                        print(f"  -> Failed for scene {idx}: {response.status_code} {response.text[:200]}")
                except Exception as e:
                    print(f"  -> Error: {e}")

    if tts_type == "opensource":
        print("Using edge-tts (Microsoft Edge Text-to-Speech)...")
        try:
            import edge_tts
        except ImportError:
            print("ERROR: edge-tts not installed. Run: pip install edge-tts")
            sys.exit(1)

        # Professional voice choices
        voice = "en-US-GuyNeural"  # Deep male professional voice
        # Other good options:
        # "en-US-JennyNeural" - Female
        # "en-US-AriaNeural"  - Female casual
        # "en-GB-RyanNeural"  - British male

        async def generate_all():
            for idx, scene in enumerate(data.get("scenes", [])):
                text = scene.get("description", "")
                if not text:
                    continue

                print(f"Generating edge-tts audio for Scene {idx + 1}: {text[:60]}...")
                out_file = f"public/voices/scene_{idx}.mp3"

                try:
                    communicate = edge_tts.Communicate(text, voice, rate="-5%", pitch="+0Hz")
                    await communicate.save(out_file)
                    scene["voiceUrl"] = f"/voices/scene_{idx}.mp3"
                    print(f"  -> Saved {out_file}")
                except Exception as e:
                    print(f"  -> Error generating scene {idx}: {e}")

        asyncio.run(generate_all())

    # Save the updated script back with voiceUrl paths
    with open(script_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

    print("TTS Generation Complete.")

if __name__ == "__main__":
    main()
