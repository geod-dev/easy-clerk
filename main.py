from pynput import keyboard

from Recorder import Recorder
from transcribe import transcribe

recorder = Recorder()
controller = keyboard.Controller()


def on_key_press(key):
    if key == keyboard.Key.f9 and not recorder.recording:
        print("F9 key pressed.")
        recorder.start_recording()


def on_key_release(key):
    if key == keyboard.Key.f9 and recorder.recording:
        print("F9 key released.")
        recorder.stop_recording()
        print("Saved successfully to:", recorder.output_path)
        print("Record duration:", recorder.last_record_duration)
        if recorder.last_record_duration < 0.5:
            print("too short. cancelled.")
            return
        transcription = transcribe(recorder.output_path)
        print("transcription:", transcription)
        controller.type(transcription)


# Collect events until released
with keyboard.Listener(on_press=on_key_press, on_release=on_key_release) as listener:
    listener.join()
