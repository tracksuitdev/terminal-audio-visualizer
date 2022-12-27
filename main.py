import sys
import time

from pydub import AudioSegment


def open_file(filename, file_type):
    if file_type == "mp3":
        return AudioSegment.from_mp3(filename)
    elif file_type == "wav":
        return AudioSegment.from_wav(filename)
    elif file_type == "flv":
        return AudioSegment.from_flv(filename)
    elif file_type == "ogg":
        return AudioSegment.from_ogg(filename)
    elif file_type == "raw":
        return AudioSegment.from_raw(filename)


def print_frame(frame, height, print_char):
    for i in range(height, 0, -1):
        for j in range(len(frame)):
            if i <= frame[j]:
                print(print_char, end='')
            else:
                print(' ', end='')
        print()


def clear_frame(height):
    for _ in range(height):
        sys.stdout.write("\033[F\033[K")


class FrameLengthSmallerThanWidth(Exception):
    def __init__(self, fps, width):
        super().__init__(f"Width of frame is lesser than width of print line. Increase fps({fps}) or decrease "
                         f"width({width})")


def graphic_frames_from_audio_frame(audio_frame, step, width, divisor):
    result = []
    point = 0
    current_sum = 0
    current_frame = []
    for x in audio_frame:
        current_sum += int((abs(x) // divisor))
        point += 1
        if point == step:
            current_frame.append(current_sum // point)
            point = 0
            current_sum = 0
        if len(current_frame) == width:
            result.append(current_frame)
            current_frame = []

    return result


def visualize(filename, file_type="mp3", fps=60, width=30, height=15, print_char="#"):
    audio = open_file(filename, file_type)
    arr = audio.get_array_of_samples()[0::2]
    audio_frame_width = audio.frame_rate // fps  # width of audio frame used to create a single graphical frame
    if audio_frame_width < width:
        raise FrameLengthSmallerThanWidth(fps, width)
    point_interval = audio_frame_width // width  # interval used for interpolation
    interval = 1.0 / fps
    print_frame([0] * width, height, " ")
    audio_start = time.time()
    for i in range(0, len(arr), audio.frame_rate):
        audio_frame = arr[i:i + audio.frame_rate]
        graphic_frames = graphic_frames_from_audio_frame(audio_frame, point_interval, width,
                                                         audio.max_possible_amplitude / height)
        for j in range(fps):
            clear_frame(height)
            print_frame(graphic_frames[j], height, print_char)
            seconds_elapsed = i // audio.frame_rate
            time_intervals_elapsed = (j + 1) * interval
            end_time = audio_start + seconds_elapsed + time_intervals_elapsed
            current_time = time.time()
            if end_time - current_time > 0:
                time.sleep(end_time - time.time())
            else:
                print("SKIPPED FRAME")


if __name__ == "__main__":
    visualize("/home/ivan/music-lib/CAMOUFLAGE - Love is a shield - 1989.mp3")

