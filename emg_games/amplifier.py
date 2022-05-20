import time

import numpy as np
import scipy.signal as ss

from abc import ABC, abstractmethod
from multiprocessing import Process, Lock
from multiprocessing.sharedctypes import Array

from pylsl import StreamInlet, resolve_streams

# from multiprocessing import Process, Lock
# from multiprocessing.sharedctypes import Array
#
# import numpy as np
# import time
#
# import traceback
#
# from .utils import singleton
#
# import importlib


# # TODO need cleanup and other
# # @singleton
# class Amplifier:
#
#     def __init__(self, fs=512, samples=2*512, sleep_time=1, channels=(0, 1)):
#         TmsiCppAmplifier = getattr(importlib.import_module('obci_cpp_amplifiers.amplifiers'), 'TmsiCppAmplifier')
#
#         self._sleep_time = sleep_time
#
#         self.__data = Array('d', np.zeros(samples))
#
#         amplifiers = TmsiCppAmplifier.get_available_amplifiers('usb')
#         print('amplifiers:', *amplifiers)
#         if not amplifiers:
#             raise ValueError("Nie ma wzmacniacza")
#
#         if len(channels) != 2:
#             raise ValueError('Potrzebne są 2 kanały')
#         self.channels = channels
#         self.amplifier = TmsiCppAmplifier(amplifiers[0])
#
#         self.amplifier.sampling_rate = fs
#         self.gains = np.array(self.amplifier.current_description.channel_gains)
#         self.offsets = np.array(self.amplifier.current_description.channel_offsets)
#
#         self.__lock = Lock()
#         self.__process = Process(target=self.__run)
#         self.__process.start()
#         # self.__process.join()
#
#         self.id = np.random.randint(1, 1000000000)  # TODO remove later
#
#     def __get_data(self):
#         number_of_samples = 64  # TODO fix magic number
#         try:  # TODO
#             samples = self.amplifier.get_samples(number_of_samples).samples
#         except Exception as exception:
#             traceback.print_exc()
#             exit()
#
#         samples = samples * self.gains + self.offsets
#         samples = samples[:, self.channels[0]] - samples[:, self.channels[1]]
#         with self.__lock:
#             self.__data[:-number_of_samples] = self.__data[number_of_samples:]
#             self.__data[-number_of_samples:] = Array('d', samples)
#
#     @property
#     def data(self):
#         return self.__data
#
#     def __run(self):
#         self.amplifier.start_sampling()
#         # time.sleep(1)
#         while True:
#             self.__get_data()
#
#     def get_signal(self, sample_count=None):
#         max_samples_count = len(self.data)
#         if sample_count is None:
#             sample_count = max_samples_count
#         if not (1 <= sample_count <= max_samples_count):
#             # TODO warning
#             sample_count = min(1, max(sample_count, max_samples_count))
#         with self.__lock:
#             return self.data[-sample_count:]
#
#     def terminate(self):
#         self.__process.terminate()
#
#     @property
#     def lock(self):
#         return self.__lock
#
#


class LSLAmplifier(ABC):
    sleep_time = 0.05

    def __init__(self, *, name, channels, size=2048):

        streams = resolve_streams(wait_time=6)  # might not work
        if not streams:
            raise ValueError('could not find streamer')

        stream = next((stream for stream in streams if stream.name() == name), None)
        if not stream:
            raise ValueError(f'Could not find "{name}" stream')
        self._streamer = StreamInlet(stream)

        self._channels = channels
        self.__size = size

        self.__data = Array('d', np.zeros(size))

        Fs = stream.nominal_srate()
        Fnyq = Fs / 2
        Q = 30
        self._b, self._a = ss.butter(3, [0.1 / Fnyq, 45 / Fnyq], 'bandpass')
        self._bn, self._an = ss.iirnotch(50, Q, Fs)
        self._bnn, self._ann = ss.iirnotch(100, Q, Fs)
        self._filt = ss.lfilter_zi(self._b, self._a)
        self._filtn = ss.lfilter_zi(self._bn, self._an)
        self._filtnn = ss.lfilter_zi(self._bnn, self._ann)

        self.__lock = Lock()
        self.__process = Process(target=self.__run)
        self.__process.daemon = True
        self.__process.start()




        print('amplifier started')

    def get_data(self, size=None):
        with self.__lock:
            size = size | len(self.data)
            return self.data[-size:]

    @property
    def data(self):
        with self.__lock:
            return self.__data

    @property
    def lock(self):
        return self.__lock

    @abstractmethod
    def _make_montage(self, signal):
        return NotImplemented

    def __run(self):
        while True:
            sample, timestamp = self._streamer.pull_chunk(timeout=self.sleep_time, max_samples=len(self.data))
            if not sample:
                time.sleep(self.sleep_time)
                continue

            sample = np.array(sample)
            sample = self._make_montage(sample).flatten()

            number_of_samples = len(sample)
            number_of_samples = min(number_of_samples, len(self.data))

            filtered_sample, self._filtn = ss.lfilter(self._bn, self._an, sample, zi=self._filtn)
            filtered_sample, self._filtnn = ss.lfilter(self._bnn, self._ann, filtered_sample, zi=self._filtnn)
            filtered_sample, self._filt = ss.lfilter(self._b, self._a, filtered_sample, zi=self._filt)

            with self.__lock:
                self.__data[:-number_of_samples] = self.__data[number_of_samples:]
                self.__data[-number_of_samples:] = Array('d', filtered_sample)[-number_of_samples:]

            time.sleep(self.sleep_time)

    def terminate(self):
        self.__process.terminate()
        print('amplifier stopped')


class MonoAmplifier(LSLAmplifier):
    def __init__(self, *, name, channels, size=2048):
        if isinstance(channels, int):
            channels = [channels]
        if not len(channels) == 1:
            raise ValueError(f'"MonoAmplifier" uses only 1 channel, not {len(channels)}')

        super(MonoAmplifier, self).__init__(name=name, channels=channels, size=size)

    def _make_montage(self, signal):
        return signal[:, self._channels]


class BipolarAmplifier(LSLAmplifier):

    def __init__(self, *, name, channels, size=2048):
        if isinstance(channels, int):
            channels = channels[channels]
        if not len(channels) == 2:
            raise ValueError(f'"BipolarAmplifier" uses only 2 channel, not {len(channels)}')
        if channels[0] == channels[1]:
            raise ValueError(f'channels cannot be the same')

        super(BipolarAmplifier, self).__init__(name=name, channels=channels, size=size)

    def _make_montage(self, signal):
        sample = signal[:, self._channels]
        return sample[:, 0] - sample[:, 1]
