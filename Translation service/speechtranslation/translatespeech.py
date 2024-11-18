from dotenv import load_dotenv
import os
import azure.cognitiveservices.speech as speech_sdk

def main():
    try:
        # Load environment variables
        load_dotenv()
        ai_key = os.getenv('SPEECH_KEY')
        ai_region = os.getenv('SPEECH_REGION')

        # Define languages
        from_language = 'en-US'  # Source language (the language you speak)
        to_language = 'fr'       # Target language (translation language)

        # Configure translation
        translation_config = speech_sdk.translation.SpeechTranslationConfig(
            subscription=ai_key, region=ai_region)
        translation_config.speech_recognition_language = from_language
        translation_config.add_target_language(to_language)

        # Set up microphone for audio input
        audio_config = speech_sdk.AudioConfig(use_default_microphone=True)
        translation_recognizer = speech_sdk.translation.TranslationRecognizer(
            translation_config=translation_config, audio_config=audio_config)

        print(f'Speak now in "{from_language}". Your speech will be translated to "{to_language}".')

        # Perform translation
        result = translation_recognizer.recognize_once()
        print(process_result(result, from_language, to_language))

    except Exception as ex:
        print("Error:", ex)

def process_result(result, from_language, to_language):
    if result.reason == speech_sdk.ResultReason.TranslatedSpeech:
        return (f'Recognized ({from_language}): {result.text}\n' +
                f'Translated ({to_language}): {result.translations[to_language]}')
    elif result.reason == speech_sdk.ResultReason.RecognizedSpeech:
        return f'Recognized: "{result.text}" (No translation available)'
    elif result.reason == speech_sdk.ResultReason.NoMatch:
        return "No speech could be recognized."
    elif result.reason == speech_sdk.ResultReason.Canceled:
        cancellation = result.cancellation_details
        return (f"Speech Recognition canceled: {cancellation.reason}\n" +
                f"Error details: {cancellation.error_details}")
    else:
        return "Unknown error during translation."

if __name__ == "__main__":
    main()
