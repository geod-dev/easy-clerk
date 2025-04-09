import os
import struct
import threading
import time
import wave

import pvrecorder


class Recorder:
    def __init__(self, output_path="temp.wav"):
        self.output_path = output_path
        self.recording = False
        self.file = None

        self.start_recording_time = 0
        self.last_record_duration = 0

        self.recorder = pvrecorder.PvRecorder(frame_length=512)
        threading.Thread(target=self._recording_loop).start()

    def stop_recording(self):
        self.recording = False
        self.file.close()
        self.file = None
        self.last_record_duration = time.time() - self.start_recording_time
        return self.output_path

    def start_recording(self):
        if self.recording:
            return
        self.recording = True

        if os.path.exists(self.output_path):
            os.remove(self.output_path)

        self.file = wave.open(self.output_path, "w")
        self.file.setparams((1, 2, self.recorder.sample_rate, self.recorder.frame_length, "NONE", "NONE"))
        self.start_recording_time = time.time()

    def _recording_loop(self):
        self.recorder.start()
        last_frames = []

        while True:
            frame = self.recorder.read()
            last_frames.append(frame)
            if self.recording:
                while len(last_frames):
                    self._add_frame(last_frames.pop(0))
            else:
                if len(last_frames) > 5:
                    last_frames = last_frames[-5:]

    def _add_frame(self, frame):
        self.file.writeframes(struct.pack("h" * len(frame), *frame))
