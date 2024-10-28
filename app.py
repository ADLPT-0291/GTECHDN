import paho.mqtt.client as mqtt
import ssl
import json  # Sử dụng thư viện json để tạo chuỗi JSON
import subprocess

# Thông tin kết nối MQTT Broker
broker_address = "dcab58eb6e6a48f48c506685c17bbb52.s1.eu.hivemq.cloud"
broker_port = 8883  # Cổng MQTT cho kết nối bảo mật (TLS)
username = "gtechdn"
password = "gtechdn123"

import subprocess

# Biến toàn cục để lưu tiến trình DarkIce
darkice_process = None

def turn_on_darkice():
    global darkice_process
    if darkice_process is None or darkice_process.poll() is not None:
        try:
            darkice_process = subprocess.Popen(['darkice'])
            print("darkice đã được bật!")
        except Exception as e:
            print(f"Lỗi khi khởi động darkice: {e}")
    else:
        print("darkice đang chạy!")

def turn_off_darkice():
    global darkice_process
    if darkice_process is not None and darkice_process.poll() is None:
        try:
            darkice_process.terminate()
            darkice_process = None
            print("darkice đã được tắt!")
        except Exception as e:
            print(f"Lỗi khi dừng darkice: {e}")
    else:
        print("darkice không chạy!")


# Hàm callback khi kết nối thành công
def on_connect(client, userdata, flags, rc):
    print(f"Đã kết nối tới broker với mã trạng thái {rc}")
    if rc == 0:
        client.subscribe("gtechdn/test")
        print("Đã đăng ký vào topic 'gtechdn/test'")
    else:
        print(f"Không thể kết nối, mã lỗi: {rc}")

# Hàm callback khi nhận được một thông điệp
def on_message(client, userdata, message):
    try:
        # Giải mã thông điệp JSON
        payload = message.payload.decode()
        data = json.loads(payload)
        
        # Kiểm tra lệnh và thực hiện bật/tắt darkice
        if "command" in data:
            if data["command"] =="1":
                 print("Đã nhận được lệnh")
                 turn_on_darkice()
            elif data["command"] =="2":
                 turn_off_darkice()
                 print("Chưa nhận được lệnh")
            else:
                print(f"Nhận lệnh không xác định: {data['command']}")
        else:
            print("Thông điệp không chứa lệnh hợp lệ.")
    except json.JSONDecodeError:
        print("Không thể giải mã thông điệp JSON.")

# Tạo client MQTT
client = mqtt.Client("gtechdn")

# Cài đặt thông tin xác thực
client.username_pw_set(username, password)

# Cài đặt kết nối bảo mật TLS
client.tls_set(ca_certs=None, certfile=None, keyfile=None, tls_version=ssl.PROTOCOL_TLS)

# Gán callback functions cho các sự kiện
client.on_connect = on_connect
client.on_message = on_message

# Kết nối tới MQTT broker
try:
    client.connect(broker_address, broker_port)
except Exception as e:
    print(f"Lỗi kết nối: {e}")
    exit(1)

# Vòng lặp để duy trì kết nối và nhận thông điệp
client.loop_forever()
