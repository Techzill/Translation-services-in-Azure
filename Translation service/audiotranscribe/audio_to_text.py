from dotenv import load_dotenv
import os
import azure.cognitiveservices.speech as speech_sdk
from playsound import playsound
import threading

def main():
    try:
        # Load configuration settings
        load_dotenv()
        ai_key = os.getenv('SPEECH_KEY')
        ai_region = os.getenv('SPEECH_REGION')

        # Configure the speech service with a specified language
        speech_config = speech_sdk.SpeechConfig(subscription=ai_key, region=ai_region)
        speech_config.speech_recognition_language = "en-US"  # Set language to English (US)
        print("Ready to use speech service in:", speech_config.region)

        # Specify the audio file path
        audio_file_path = "book_audio.wav"

        # Start playing the audio in a separate thread
        audio_thread = threading.Thread(target=playsound, args=(audio_file_path,))
        audio_thread.start()

        # Transcribe the audio
        TranscribeAudioFile(speech_config, audio_file_path)

        # Wait for the audio to finish playing
        audio_thread.join()

    except Exception as ex:
        print("An error occurred:", ex)

def TranscribeAudioFile(speech_config, audio_file_path):
    # Configure the audio file for recognition
    audio_config = speech_sdk.AudioConfig(filename=audio_file_path)
    speech_recognizer = speech_sdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    print(f"Transcribing from audio file: {audio_file_path}")

    # Event handler for recognized speech
    def handle_final_result(evt):
        if evt.result.reason == speech_sdk.ResultReason.RecognizedSpeech:
            print("Recognized:", evt.result.text)  # Print recognized text directly to the console
        elif evt.result.reason == speech_sdk.ResultReason.NoMatch:
            print("No recognizable speech found.")
        elif evt.result.reason == speech_sdk.ResultReason.Canceled:
            cancellation = evt.result.cancellation_details
            print("Cancellation reason:", cancellation.reason)
            print("Error details:", cancellation.error_details)

    # Connect the event handler
    speech_recognizer.recognized.connect(handle_final_result)

    # Start continuous recognition
    done = False
    def stop_cb(evt):
        nonlocal done
        done = True

    # Connect the stop event
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    # Start recognition
    speech_recognizer.start_continuous_recognition()
    print("Processing audio...")

    # Wait for completion
    while not done:
        pass

    # Stop recognition after processing is complete
    speech_recognizer.stop_continuous_recognition_async().get()

    print("Transcription complete.")

if __name__ == "__main__":
    main()
