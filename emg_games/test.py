from amplifier import MonoAmplifier, BipolarAmplifier

amp = MonoAmplifier(name='dupa', channels=[25])
# amp = BipolarAmplifier(name='ddd', channels=[0, 1])

import time
import ipdb; ipdb.set_trace()
time.sleep(10)
for i, x in enumerate(amp.data):
    print(i, x)


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