from AudioAnalyzer import AudioAnalyzer, AudioBar
import numpy as np
import pygame
import sys


class AudioPlayer(object):

    def __init__(self, config, audio_path):
        pygame.init()

        self.__screen, self.__screen_w, self.__screen_h = self.__init_UI()
        self.__audio_path = audio_path
        self.__analyzer = AudioAnalyzer(audio_path)
        self.__config = config

        self.__bands = [
            {"start": 20, "stop": 160, "num": 36},     # 低音区
            {"start": 160, "stop": 1280, "num": 135},   # 中音区
            {"start": 1280, "stop": 5120, "num": 36},  # 高音区
        ]
        self.__bars = self.__init_bars(self.__bands)

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
        bar_width = self.__screen_w / (sum([band['num'] for band in freq_bands]))
        idx = 0
        bars = []
        for band in freq_bands:
            l_points, step = np.linspace(band['start'], band['stop'], num=band['num'], endpoint=False, retstep=True, dtype=np.int)
            for l in l_points:
                bars.append(AudioBar(
                    x=bar_width * idx,
                    y=self.__screen_h / 2,
                    freq_list=np.arange(start=l, stop=l+step),
                    width=bar_width,
                    max_height=self.__screen_h / 2,
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

            for idx, bar in enumerate(self.__bars):
                bar.update(deltaTime, pygame.mixer.music.get_pos() / 1000.0, self.__analyzer)

            poly = []
            for bar in self.__bars:
                poly.extend([bar.points[0], bar.points[3], bar.points[2], bar.points[1]])
            for bar in reversed(self.__bars):
                poly.extend([bar.mirror_points[1], bar.mirror_points[2], bar.mirror_points[3], bar.mirror_points[0]])

            pygame.draw.polygon(self.__screen,
                                config['bar_color'],
                                poly)
            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    config = {
        'background_color': (255, 255, 255),
        'bar_color': (49, 94, 251),
    }
    audio_name = sys.argv[1] if len(sys.argv) > 1 else None
    if audio_name:
        print("Reading the audio....")
        app = AudioPlayer(config, audio_name)
        app.run()
    else:
        print("You should input the audio path as an argument.")
