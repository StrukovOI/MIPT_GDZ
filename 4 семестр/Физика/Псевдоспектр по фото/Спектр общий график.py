import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import sys
import os

class SkySpectrumAnalyzer:
    def __init__(self, image_path):
        self.image_path = image_path
        self.load_image()
        
        # Параметры рамок (x, y, width, height)
        h, w = self.img_rgb.shape[:2]
        
        # Адаптивный размер рамки (примерно 10% от ширины экрана)
        box_w = max(50, int(w * 0.01))
        box_h = max(50, int(h * 0.01))
        
        self.rois = []
        # Распределяем 5 рамок по вертикали или горизонтали в зависимости от ориентации
        if w > h: # Альбомная
            start_x = int(w * 0.1)
            step_x = int((w - 2*start_x) / 4)
            for i in range(5):
                x = start_x + i * step_x
                y = int(h / 2)
                self.rois.append([x, y, box_w, box_h])
        else: # Портретная
            start_y = int(h * 0.1)
            step_y = int((h - 2*start_y) / 4)
            for i in range(5):
                x = int(w / 2)
                y = start_y + i * step_y
                self.rois.append([x, y, box_w, box_h])
            
        self.colors = ['#FF0000', '#00FF00', '#0000FF', '#FFA500', '#800080'] # Red, Green, Blue, Orange, Purple
        self.labels = [f'Area {i+1}' for i in range(5)]

        self.setup_gui()

    def load_image(self):
        try:
            img_pil = Image.open(self.image_path)
            img_pil = img_pil.convert('RGB')
            self.img_rgb = np.array(img_pil)
            print(f"Image loaded. Shape: {self.img_rgb.shape}")
        except Exception as e:
            print(f"Error loading image: {e}")
            sys.exit(1)

    def setup_gui(self):
        self.fig = plt.figure(figsize=(14, 7))
        
        # Left: Image
        self.ax_img = plt.subplot(1, 2, 1)
        self.ax_img.imshow(self.img_rgb)
        self.ax_img.set_title('Click and Drag boxes to move them')
        self.ax_img.axis('off')
        
        # Right: Spectra
        self.ax_spec = plt.subplot(1, 2, 2)
        self.ax_spec.set_title('Pseudo-Spectra (Normalized RGB)')
        self.ax_spec.set_xlabel('Wavelength (nm) [Approx]')
        self.ax_spec.set_ylabel('Normalized Intensity')
        self.ax_spec.set_xlim(400, 700)
        self.ax_spec.set_ylim(0, 1.1)
        self.ax_spec.grid(True, linestyle='--', alpha=0.5)
        
        # Legend
        self.ax_spec.plot([], [], color='red', label='Red (~650 nm)')
        self.ax_spec.plot([], [], color='green', label='Green (~550 nm)')
        self.ax_spec.plot([], [], color='blue', label='Blue (~450 nm)')
        self.ax_spec.legend(loc='upper right')

        # Create rectangles
        self.rect_patches = []
        for i in range(5):
            rect = plt.Rectangle(
                (self.rois[i][0], self.rois[i][1]), 
                self.rois[i][2], self.rois[i][3],
                linewidth=2, edgecolor=self.colors[i], facecolor='none',
                picker=True # Включаем возможность выбора
            )
            self.ax_img.add_patch(rect)
            self.rect_patches.append(rect)
            
            # Label
            self.ax_img.text(
                self.rois[i][0], self.rois[i][1] - 10, 
                f'{i+1}', color=self.colors[i], fontsize=12, weight='bold',
                bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', pad=1)
            )

        # Connect events for dragging
        self.fig.canvas.mpl_connect('pick_event', self.on_pick)
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.fig.canvas.mpl_connect('button_release_event', self.on_release)
        
        self.active_rect = None
        self.press_data = None
        
        self.update_spectra()
        plt.tight_layout()
        plt.show()

    def on_pick(self, event):
        if isinstance(event.artist, plt.Rectangle):
            self.active_rect = event.artist
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
        
        # Boundaries check
        h, w = self.img_rgb.shape[:2]
        rw, rh = self.active_rect.get_width(), self.active_rect.get_height()
        
        new_x = max(0, min(new_x, w - rw))
        new_y = max(0, min(new_y, h - rh))
        
        self.active_rect.set_xy((new_x, new_y))
        self.fig.canvas.draw_idle()

    def on_release(self, event):
        if self.active_rect:
            self.active_rect = None
            self.update_spectra()

    def get_roi_data(self, rect):
        x = int(rect.get_x())
        y = int(rect.get_y())
        w = int(rect.get_width())
        h = int(rect.get_height())
        
        roi = self.img_rgb[y:y+h, x:x+w]
        
        mean_r = np.mean(roi[:, :, 0])
        mean_g = np.mean(roi[:, :, 1])
        mean_b = np.mean(roi[:, :, 2])
        
        return mean_r, mean_g, mean_b

    def update_spectra(self):
        self.ax_spec.clear()
        self.ax_spec.set_title('Pseudo-Spectra (Normalized RGB)')
        self.ax_spec.set_xlabel('Wavelength (nm) [Approx]')
        self.ax_spec.set_ylabel('Normalized Intensity')
        self.ax_spec.set_xlim(400, 700)
        self.ax_spec.set_ylim(0, 1.1)
        self.ax_spec.grid(True, linestyle='--', alpha=0.5)
        
        lambdas = [450, 550, 650] 
        
        for i in range(5):
            r, g, b = self.get_roi_data(self.rect_patches[i])
            max_val = max(r, g, b)
            if max_val == 0: max_val = 1
            
            norm_r, norm_g, norm_b = r/max_val, g/max_val, b/max_val
            
            self.ax_spec.plot(lambdas, [norm_b, norm_g, norm_r], 
                              marker='o', color=self.colors[i], 
                              label=f'Area {i+1}', linewidth=2, markersize=8)

        self.ax_spec.legend(loc='best', fontsize='small')
        self.fig.canvas.draw_idle()

if __name__ == '__main__':
    # ЗАМЕНИТЕ ЭТО НА ПУТЬ К ВАШЕМУ ФОТО
    photo_path = 'C:/Users/olezh/OneDrive/Рабочий стол/4.jpg' 
    
    # Если файла нет, создадим тестовый градиент
    if not os.path.exists(photo_path):
        print("File not found. Generating test gradient image...")
        w, h = 800, 600
        y_coords = np.linspace(0, 1, h).reshape(-1, 1)
        
        # Gradient: Blue at top (y=0), Red at bottom (y=1)
        R = (255 * y_coords).astype(np.uint8)
        G = (200 * np.ones_like(y_coords)).astype(np.uint8)
        B = (255 * (1 - y_coords)).astype(np.uint8)
        
        img_test = np.concatenate([R, G, B], axis=1) # Wrong shape fix below
        # Correct stacking for RGB image (H, W, 3)
        img_test = np.zeros((h, w, 3), dtype=np.uint8)
        img_test[:, :, 0] = R
        img_test[:, :, 1] = G
        img_test[:, :, 2] = B
        
        img_pil = Image.fromarray(img_test)
        img_pil.save('test_sky.jpg')
        photo_path = 'test_sky.jpg'

    app = SkySpectrumAnalyzer(photo_path)