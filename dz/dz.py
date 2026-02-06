import tkinter as tk
from time import sleep
import threading

class TrafficLight:
    def __init__(self, root):
        self.root = root
        self.root.title("Светофор")
        self.root.geometry("200x450")
        self.root.resizable(False, False)
        
        # Текущий активный сигнал (0 - красный, 1 - желтый, 2 - зеленый)
        self.current_light = 0
        
        # Создаем холст для рисования светофора
        self.canvas = tk.Canvas(root, width=200, height=400, bg="gray")
        self.canvas.pack()
        
        # Рисуем корпус светофора
        self.canvas.create_rectangle(50, 20, 150, 370, fill="black", outline="white", width=2)
        
        # Рисуем сигналы светофора (изначально выключены)
        self.red_light = self.canvas.create_oval(60, 30, 140, 110, fill="gray", outline="white", width=2)
        self.yellow_light = self.canvas.create_oval(60, 120, 140, 200, fill="gray", outline="white", width=2)
        self.green_light = self.canvas.create_oval(60, 210, 140, 290, fill="gray", outline="white", width=2)
        
        # Кнопки управления
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=10)
        
        self.start_button = tk.Button(self.button_frame, text="Старт", command=self.start_traffic_light, width=10)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = tk.Button(self.button_frame, text="Стоп", command=self.stop_traffic_light, width=10)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        self.manual_button = tk.Button(root, text="Ручное управление", command=self.toggle_manual, width=20)
        self.manual_button.pack(pady=5)
        
        # Флаг для работы/остановки светофора
        self.running = False
        self.manual_mode = False
        
        # Кнопки для ручного режима
        self.manual_frame = tk.Frame(root)
        self.red_button = tk.Button(self.manual_frame, text="Красный", command=lambda: self.set_light(0), width=8)
        self.yellow_button = tk.Button(self.manual_frame, text="Желтый", command=lambda: self.set_light(1), width=8)
        self.green_button = tk.Button(self.manual_frame, text="Зеленый", command=lambda: self.set_light(2), width=8)
        
        # Надпись состояния
        self.status_label = tk.Label(root, text="Светофор выключен", font=("Arial", 10))
        self.status_label.pack(pady=5)
        
        # Включаем красный свет при запуске
        self.set_light(0)
    
    def set_light(self, light_index):
        """Устанавливает указанный сигнал светофора"""
        # Выключаем все сигналы
        self.canvas.itemconfig(self.red_light, fill="gray")
        self.canvas.itemconfig(self.yellow_light, fill="gray")
        self.canvas.itemconfig(self.green_light, fill="gray")
        
        # Включаем нужный сигнал
        if light_index == 0:  # Красный
            self.canvas.itemconfig(self.red_light, fill="red")
            self.status_label.config(text="Красный - СТОП")
            self.current_light = 0
        elif light_index == 1:  # Желтый
            self.canvas.itemconfig(self.yellow_light, fill="yellow")
            self.status_label.config(text="Желтый - ВНИМАНИЕ")
            self.current_light = 1
        else:  # Зеленый
            self.canvas.itemconfig(self.green_light, fill="green")
            self.status_label.config(text="Зеленый - ИДТИ")
            self.current_light = 2
    
    def start_traffic_light(self):
        """Запускает автоматическую работу светофора"""
        if not self.running:
            self.running = True
            self.manual_mode = False
            self.manual_button.config(text="Ручное управление")
            self.manual_frame.pack_forget()
            self.status_label.config(text="Автоматический режим")
            
            # Запускаем цикл светофора в отдельном потоке
            thread = threading.Thread(target=self.traffic_light_cycle)
            thread.daemon = True
            thread.start()
    
    def stop_traffic_light(self):
        """Останавливает светофор"""
        self.running = False
        self.status_label.config(text="Светофор остановлен")
    
    def traffic_light_cycle(self):
        """Цикл автоматической работы светофора"""
        while self.running and not self.manual_mode:
            # Красный (5 секунд)
            self.root.after(0, self.set_light, 0)
            sleep(5)
            if not self.running or self.manual_mode:
                break
                
            # Желтый (2 секунды)
            self.root.after(0, self.set_light, 1)
            sleep(2)
            if not self.running or self.manual_mode:
                break
                
            # Зеленый (5 секунд)
            self.root.after(0, self.set_light, 2)
            sleep(5)
            if not self.running or self.manual_mode:
                break
            
            # Желтый (2 секунды) перед красным
            self.root.after(0, self.set_light, 1)
            sleep(2)
    
    def toggle_manual(self):
        """Переключает между ручным и автоматическим режимом"""
        self.manual_mode = not self.manual_mode
        
        if self.manual_mode:
            self.running = False
            self.manual_button.config(text="Автоматический режим")
            self.manual_frame.pack(pady=5)
            self.red_button.pack(side=tk.LEFT, padx=2)
            self.yellow_button.pack(side=tk.LEFT, padx=2)
            self.green_button.pack(side=tk.LEFT, padx=2)
            self.status_label.config(text="Ручной режим")
        else:
            self.manual_frame.pack_forget()
            self.manual_button.config(text="Ручное управление")
            self.status_label.config(text="Светофор выключен")

if __name__ == "__main__":
    root = tk.Tk()
    app = TrafficLight(root)
    root.mainloop()
