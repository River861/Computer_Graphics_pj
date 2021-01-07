from AudioAnalyzer import AudioAnalyzer, AudioBar
import numpy as np
import pygame
import sys
import random
import colorsys


class AudioPlayer(object):

    def __init__(self, config, audio_path):
        pygame.init()

        self.__screen, self.__screen_w, self.__screen_h = self.__init_UI()
        self.__audio_path = audio_path
        self.__analyzer = AudioAnalyzer(audio_path)
        self.__config = config

        self.__bands = [
            {"start": 20, "stop": 160, "num": 12},     # 低音区
            {"start": 160, "stop": 1280, "num": 45},   # 中音区
            {"start": 1280, "stop": 5120, "num": 12},  # 高音区
        ]
        self.__bars = self.__init_bars(self.__bands)

        # 与颜色机制相关的参数
        self.__bar_color = config['bar_color']
        self.__trigger_tick = 0

    def __init_UI(self):
        """初始化界面
        """
        pygame.display.set_caption('Audio Player')
        infoObject = pygame.display.Info()
        screen_w = int(infoObject.current_w * 0.7)
        screen_h = int(infoObject.current_h * 0.65)

        return pygame.display.set_mode((screen_w, screen_h)), screen_w, screen_h

    def __init_bars(self, freq_bands):
        """初始化音频条
        """
        bar_width = self.__screen_w / ((1+self.__config['interval_ratio']) * sum([band['num'] for band in freq_bands]))
        idx = 0
        bars = []
        for band in freq_bands:
            l_points, step = np.linspace(band['start'], band['stop'], num=band['num'], endpoint=False, retstep=True, dtype=np.int)
            for l in l_points:
                bars.append(AudioBar(
                    x=(bar_width*(1+self.__config['interval_ratio']))*idx,
                    y=self.__screen_h,
                    freq_list=np.arange(start=l, stop=l+step),
                    width=bar_width,
                    max_height=self.__screen_h
                ))
                idx += 1
        return bars

    def __is_running(self):
        """监听是否关闭
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True

    def run(self):
        """运行过程
        """
        pygame.mixer.music.load(self.__audio_path)
        pygame.mixer.music.play(0)

        last_tick = pygame.time.get_ticks()
        while self.__is_running():
            t = pygame.time.get_ticks()
            deltaTime = (t - last_tick) / 1000.0
            last_tick = t

            self.__screen.fill(self.__config['background_color'])

            avg_bass = 0  # 更新bar高度的同时计算一下中低音区的平均dB
            for idx, bar in enumerate(self.__bars):
                avg_dB = bar.update(deltaTime, pygame.mixer.music.get_pos() / 1000.0, self.__analyzer)
                if idx < self.__bands[0]['num']:
                    avg_bass += avg_dB
            avg_bass /= self.__bands[0]['num']

            poly = []
            for bar in self.__bars:
                poly.extend([bar.points[0], bar.points[3], bar.points[2], bar.points[1]])

            pygame.draw.polygon(self.__screen,
                                self.__get_bar_color(avg_bass),
                                poly)
            pygame.display.flip()

        pygame.quit()

    def __get_bar_color(self, avg_bass):
        """获取当前的bar颜色
        """
        if self.__trigger_tick == 0:
            self.__trigger_tick = pygame.time.get_ticks()

        # 每隔几秒更新一次颜色
        if (pygame.time.get_ticks() - self.__trigger_tick)/1000.0 > self.__config['color_last_time']:
            self.__bar_color = (
                self.__random_color()
                if avg_bass > self.__config['color_trigger_threshold']
                else self.__config['bar_color']
            )
            self.__trigger_tick = 0

            print(avg_bass)

        return self.__bar_color

    def __random_color(self):
        _h, _s, _l = random.random(), 0.5 + random.random() / 2.0, 0.4 + random.random() / 5.0
        return [int(256 * i) for i in colorsys.hls_to_rgb(_h, _l, _s)]


if __name__ == "__main__":
    config = {
        'background_color': (40, 40, 40),
        'bar_color': (255, 255, 255),
        'interval_ratio': 0.8,
        'color_trigger_threshold': -43,
        'color_last_time': 2.0,
    }
    audio_name = sys.argv[1] if len(sys.argv) > 1 else None
    if audio_name:
        print("Reading the audio....")
        app = AudioPlayer(config, audio_name)
        app.run()
    else:
        print("You should input the audio path as an argument.")
