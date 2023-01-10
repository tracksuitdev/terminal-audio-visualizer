import io
import sys
import unittest

from audiovisualizer import print_frame, graph_frames_from_audio, calc_data_for_visualization, \
    FrameLengthSmallerThanWidth


class TestPrintFrame(unittest.TestCase):

    def capture_output(self, frame, height, print_char):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        print_frame(frame, height, print_char)
        sys.stdout = sys.__stdout__
        return captured_output.getvalue()

    def test_all_elements_equal_to_height(self):
        # Test frame with all elements equal to height
        frame = [3, 3, 3]
        height = 3
        print_char = '*'
        expected_output = '***\n***\n***\n'
        self.assertEqual(self.capture_output(frame, height, print_char), expected_output)

    def test_elements_of_different_values(self):
        # Test frame with elements of different values
        frame = [2, 1, 3]
        height = 3
        print_char = '#'
        expected_output = '  #\n# #\n###\n'
        self.assertEqual(self.capture_output(frame, height, print_char), expected_output)

    def test_elements_set_to_0(self):
        # Test frame with elements set to 0
        frame = [0, 0, 0]
        height = 3
        print_char = '$'
        expected_output = '   \n   \n   \n'
        self.assertEqual(self.capture_output(frame, height, print_char), expected_output)

    def test_elements_less_than_height(self):
        # Test frame with elements less than height
        frame = [1, 1, 1]
        height = 3
        print_char = '%'
        expected_output = '   \n   \n%%%\n'
        self.assertEqual(self.capture_output(frame, height, print_char), expected_output)


class TestGraphFramesFromAudio(unittest.TestCase):

    def test_produces_arrays_of_size_width_by_interpolating_step_points(self):
        audio_frame = [1, 1, 1, 2, 2, 2, 3, 3, 3]
        step = 3
        width = 1

        self.assertEqual(list(graph_frames_from_audio(audio_frame, step, width, 1)), [[1], [2], [3]])

    def test_yields_the_last_partial_frame(self):
        audio_frame = [1, 1, 2]
        step = 1
        width = 2

        self.assertEqual(list(graph_frames_from_audio(audio_frame, step, width, 1)), [[1, 1], [2]])

    def test_yields_the_last_partial_point(self):
        audio_frame = [1, 1, 2]
        step = 2
        width = 1

        self.assertEqual(list(graph_frames_from_audio(audio_frame, step, width, 1)), [[1], [2]])


class TestCalcDataForVisualization(unittest.TestCase):
    def test_calc_data_for_visualization(self):
        data = [1, 2, 3, 4, 5]
        frame_rate = 5
        max_amp = 5
        width = 5
        fps = 1
        height = 5
        length, point_interval, last_frame_length, interval, divisor = calc_data_for_visualization(
            data, frame_rate, max_amp, width, fps, height
        )
        self.assertEqual(length, 5)
        self.assertEqual(point_interval, 1)
        self.assertEqual(last_frame_length, 1)
        self.assertEqual(interval, 1)
        self.assertEqual(divisor, 1)

    def test_calc_data_for_visualization_with_frame_length_smaller_than_width(self):
        data = [1, 2, 3, 4, 5]
        frame_rate = 5
        max_amp = 5
        width = 10
        fps = 5
        height = 5
        with self.assertRaises(FrameLengthSmallerThanWidth):
            calc_data_for_visualization(data, frame_rate, max_amp, width, fps, height)

