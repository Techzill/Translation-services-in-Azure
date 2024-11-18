from dotenv import load_dotenv
import os
import azure.cognitiveservices.speech as speech_sdk

def main():
    try:
        # Load environment variables
        load_dotenv()
        ai_key = os.getenv('SPEECH_KEY')
        ai_region = os.getenv('SPEECH_REGION')

        # Configure the speech service
        global speech_config  # Declare as global here
        speech_config = speech_sdk.SpeechConfig(subscription=ai_key, region=ai_region)
        print('Ready to use speech service in:', speech_config.region)

        # Get spoken input from the microphone
        command = transcribe_command()
        print("You said:", command)

    except Exception as ex:
        print("Error:", ex)

def transcribe_command():
    # Set up microphone for speech recognition
    audio_config = speech_sdk.AudioConfig(use_default_microphone=True)
    speech_recognizer = speech_sdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    print('Speak now...')

    # Process speech input from the microphone
    speech = speech_recognizer.recognize_once_async().get()
    if speech.reason == speech_sdk.ResultReason.RecognizedSpeech:
        return speech.text
    else:
        print("Speech recognition error:", speech.reason)
        if speech.reason == speech_sdk.ResultReason.Canceled:
            cancellation = speech.cancellation_details
            print("Cancellation reason:", cancellation.reason)
            print("Error details:", cancellation.error_details)
        return "Unable to recognize speech"

if __name__ == "__main__":
    main()
