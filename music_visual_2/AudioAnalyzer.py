import librosa.display
import numpy as np


class AudioAnalyzer(object):
    """音频解析器
    """
    def __init__(self, filename):
        time_series, sample_rate = librosa.load(filename)
        stft = np.abs(librosa.stft(time_series, hop_length=512, n_fft=2048*4))

        # freq-time 频谱
        self.__spectrogram = librosa.amplitude_to_db(stft, ref=np.max)

        frequencies = librosa.core.fft_frequencies(n_fft=2048*4)
        times = librosa.core.frames_to_time(np.arange(self.__spectrogram.shape[1]), sr=sample_rate, hop_length=512, n_fft=2048*4)

        # idx/freq
        self.__idx_time = len(times)/times[-1]
        self.__idx_freq = len(frequencies)/frequencies[-1]

    def get_dB(self, target_time, target_freq):
        """返回相应时刻、相应频率的dB值
        """
        return self.__spectrogram[int(target_freq * self.__idx_freq)][int(target_time * self.__idx_time)]


class AudioBar(object):
    """音频条
    """
    def __init__(self, x, y, freq_list, width=50, min_height=2, max_height=100, min_dB=-80, max_dB=0):
        for k, v in locals().items():
            if k != 'self':
                setattr(self, k, v)

        self.__height = min_height
        self.__height_dB = (self.max_height - self.min_height)/(self.max_dB - self.min_dB)
        self.points = []
        self.mirror_points = []

    def update(self, dt, time, analyzer):
        """更新矩形条的高度
        """
        avg_dB = np.mean([analyzer.get_dB(time, freq) for freq in self.freq_list])
        desired_height = avg_dB * self.__height_dB + self.max_height  # 因为dB是负值
        self.__height += (desired_height - self.__height) * (dt / 0.1)  # 通过乘dt/0.1来减缓幅值的变化
        self.__height = min([self.max_height, max([self.min_height, self.__height])])

        # 矩形的四个顶点
        self.points = [
            (self.x, self.y),
            (self.x + self.width, self.y),
            (self.x + self.width, self.y - self.__height),
            (self.x, self.y - self.__height)
        ]

        self.mirror_points = [
            (self.x, self.y),
            (self.x + self.width, self.y),
            (self.x + self.width, self.y + self.__height),
            (self.x, self.y + self.__height)
        ]
