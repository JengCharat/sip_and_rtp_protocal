import socket

# ตั้งค่า SIP Server และพอร์ต
SIP_SERVER = "192.168.11.252"  # เปลี่ยนเป็น IP ของ SIP Server
SIP_PORT = 5060
CLIENT_IP = "192.168.11.252"  # IP ของเครื่อง Client
CLIENT_PORT = 5061  # ใช้พอร์ตที่ต่างจากเซิร์ฟเวอร์

# สร้าง UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((CLIENT_IP, CLIENT_PORT))

# สร้างข้อความ SIP REGISTER
sip_register = f"""REGISTER sip:{SIP_SERVER} SIP/2.0
Via: SIP/2.0/UDP {CLIENT_IP}:{CLIENT_PORT};branch=z9hG4bK776asdhds
Max-Forwards: 70
To: <sip:jeng@{SIP_SERVER}>
From: <sip:jeng@{CLIENT_IP}>;tag=1928301774
Call-ID: 12345678@{CLIENT_IP}
CSeq: 1 REGISTER
Contact: <sip:jeng@{CLIENT_IP}>
Expires: 3600
Content-Length: 0

"""

try:
    # ส่ง REGISTER request ไปยัง SIP Server
    sock.sendto(sip_register.encode(), (SIP_SERVER, SIP_PORT))
    print("📨 SIP REGISTER request sent.")

    # รับคำตอบจากเซิร์ฟเวอร์
    response, _ = sock.recvfrom(1024)  # กำหนด buffer size 1024 bytes
    print("📩 Response from server:")
    print(response.decode())

except Exception as e:
    print(f"❌ Error: {e}")
finally:
    sock.close()
