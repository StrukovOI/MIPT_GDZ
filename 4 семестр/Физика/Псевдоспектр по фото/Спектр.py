import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import sys
import os

class SkySpectrumAnalyzer:
    def __init__(self, image_path):
        self.image_path = image_path
        self.load_image()
        self.setup_layout()
        self.setup_gui()

    def load_image(self):
        try:
            img_pil = Image.open(self.image_path).convert('RGB')
            self.img_rgb = np.array(img_pil)
            print(f"✅ Изображение загружено. Размер: {self.img_rgb.shape}")
        except Exception as e:
            print(f"❌ Ошибка загрузки: {e}")
            sys.exit(1)

    def setup_layout(self):
        h, w = self.img_rgb.shape[:2]
        # Адаптивный размер квадратика (~8% от меньшей стороны)
        size = min(w, h) * 0.02
        self.box_w = int(max(40, size))
        self.box_h = int(max(40, size))

        # Начальные позиции
        self.rois = []
        if w > h:  # Альбомная ориентация
            start_x = int(w * 0.15)
            step_x = int((w - 2 * start_x) / 4)
            for i in range(5):
                self.rois.append([start_x + i * step_x, h // 2, self.box_w, self.box_h])
        else:      # Портретная ориентация
            start_y = int(h * 0.1)
            step_y = int((h - 2 * start_y) / 4)
            for i in range(5):
                self.rois.append([w // 2, start_y + i * step_y, self.box_w, self.box_h])

        self.colors = ['red', 'green', 'blue', 'orange', 'purple']
        self.labels = [f'Area {i+1}' for i in range(5)]

    def setup_gui(self):
        self.fig = plt.figure(figsize=(16, 9))
        # Сетка: 5 строк, 2 колонки. Левая колонка шире, правая уже.
        gs = self.fig.add_gridspec(5, 2, width_ratios=[1.3, 1], hspace=0.25, wspace=0.25)

        # 🖼️ ЛЕВАЯ ЧАСТЬ: Изображение (занимает все 5 строк)
        self.ax_img = self.fig.add_subplot(gs[:, 0])
        self.ax_img.imshow(self.img_rgb)
        self.ax_img.set_title('🖱️ Зажмите и перетащите квадратик | Цифры двигаются вместе')
        self.ax_img.axis('off')

        # 📊 ПРАВАЯ ЧАСТЬ: 5 отдельных графиков
        self.ax_specs = []
        for i in range(5):
            ax = self.fig.add_subplot(gs[i, 1])
            ax.set_xlim(400, 700)
            ax.set_ylim(0, 1.1)
            ax.set_title(f'Area {i+1}')
            ax.set_ylabel('Norm. Intensity')
            ax.grid(True, linestyle='--', alpha=0.5)
            if i == 4:
                ax.set_xlabel('Wavelength (nm) [Approx]')
            self.ax_specs.append(ax)

        # 🟦 Создаём квадратики и подписи
        self.rect_patches = []
        self.text_labels = []
        for i in range(5):
            rect = plt.Rectangle(
                (self.rois[i][0], self.rois[i][1]),
                self.rois[i][2], self.rois[i][3],
                linewidth=2, edgecolor=self.colors[i], facecolor='none',
                picker=True
            )
            self.ax_img.add_patch(rect)
            self.rect_patches.append(rect)

            # Подпись с белой подложкой для читаемости на любом фоне
            txt = self.ax_img.text(
                self.rois[i][0], self.rois[i][1] - 10,
                f'{i+1}', color=self.colors[i], fontsize=14, weight='bold',
                bbox=dict(facecolor='white', alpha=0.85, edgecolor='none', pad=2)
            )
            self.text_labels.append(txt)

        # 🔌 Подключаем события мыши
        self.fig.canvas.mpl_connect('pick_event', self.on_pick)
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.fig.canvas.mpl_connect('button_release_event', self.on_release)

        self.active_rect = None
        self.press_data = None
        self.active_idx = -1

        self.update_spectra()
        plt.show()

    def on_pick(self, event):
        if isinstance(event.artist, plt.Rectangle):
            self.active_rect = event.artist
            self.active_idx = self.rect_patches.index(event.artist)
            self.press_data = {
                'xy': (event.mouseevent.xdata, event.mouseevent.ydata),
                'rect_xy': (self.active_rect.get_x(), self.active_rect.get_y())
            }

    def on_motion(self, event):
        if self.active_rect is None or event.inaxes != self.active_rect.axes:
            return
            
        dx = event.xdata - self.press_data['xy'][0]
        dy = event.ydata - self.press_data['xy'][1]
        new_x = self.press_data['rect_xy'][0] + dx
        new_y = self.press_data['rect_xy'][1] + dy

        # Ограничиваем границами изображения
        h, w = self.img_rgb.shape[:2]
        rw, rh = self.active_rect.get_width(), self.active_rect.get_height()
        new_x = max(0, min(new_x, w - rw))
        new_y = max(0, min(new_y, h - rh))

        self.active_rect.set_xy((new_x, new_y))
        # ️ Двигаем подпись вместе с квадратиком
        self.text_labels[self.active_idx].set_position((new_x, new_y - 10))
        self.fig.canvas.draw_idle()

    def on_release(self, event):
        if self.active_rect:
            self.active_rect = None
            self.update_spectra()

    def get_roi_data(self, rect):
        x, y = int(rect.get_x()), int(rect.get_y())
        w, h = int(rect.get_width()), int(rect.get_height())
        roi = self.img_rgb[y:y+h, x:x+w]
        return np.mean(roi[:, :, 0]), np.mean(roi[:, :, 1]), np.mean(roi[:, :, 2])

    def update_spectra(self):
        for i in range(5):
            ax = self.ax_specs[i]
            ax.clear()
            ax.set_title(f'Area {i+1}')
            ax.set_xlim(400, 700)
            ax.set_ylim(0, 1.1)
            ax.grid(True, linestyle='--', alpha=0.5)
            if i == 4:
                ax.set_xlabel('Wavelength (nm) [Approx]')
            ax.set_ylabel('Norm. Intensity')

            r, g, b = self.get_roi_data(self.rect_patches[i])
            max_val = max(r, g, b) or 1.0
            nr, ng, nb = r/max_val, g/max_val, b/max_val

            # Строим спектр
            ax.plot([450, 550, 650], [nb, ng, nr], marker='o', color=self.colors[i],
                    linewidth=2, markersize=8)
            # Выводим сырые значения для удобства
            ax.text(420, 0.95, f'R:{r:.0f}  G:{g:.0f}  B:{b:.0f}', fontsize=9, fontfamily='monospace')

        self.fig.canvas.draw_idle()

if __name__ == '__main__':
    # ЗАМЕНИТЕ ЭТО НА ПУТЬ К ВАШЕМУ ФОТО
    photo_path = 'C:/Users/olezh/OneDrive/Рабочий стол/Физика/Оптика/ВПВ/Небо/3.jpg' 
    
    # Если фото нет, создаём тестовый градиент "небо-закат"
    if not os.path.exists(photo_path):
        print(" Файл не найден. Генерирую тестовое изображение 'test_sky.jpg'...")
        w, h = 800, 600
        img = np.zeros((h, w, 3), dtype=np.uint8)
        y = np.linspace(0, 1, h).reshape(-1, 1)
        img[:, :, 0] = (255 * y).astype(np.uint8)          # Red: растёт вниз
        img[:, :, 1] = (200 * np.ones_like(y)).astype(np.uint8) # Green: константа
        img[:, :, 2] = (255 * (1 - y)).astype(np.uint8)    # Blue: убывает вниз
        Image.fromarray(img).save('test_sky.jpg')
        photo_path = 'test_sky.jpg'

    SkySpectrumAnalyzer(photo_path)