import socket

# ตั้งค่าพอร์ตและโฮสต์ของ SIP Server
SERVER_HOST = "0.0.0.0"  # ให้รับการเชื่อมต่อจากทุก IP
SERVER_PORT = 5060  # พอร์ตของ SIP (โดยทั่วไป 5060 สำหรับ UDP)

# สร้าง UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((SERVER_HOST, SERVER_PORT))

print(f"SIP Server is running on {SERVER_HOST}:{SERVER_PORT}")

while True:
    try:
        # รับข้อมูลจาก client (SIP request)
        data, addr = sock.recvfrom(1024)  # ขนาดของ buffer 1024 bytes
        print(f"Received SIP request from {addr}:")
        print(data.decode())

        # ตัวอย่างการตอบกลับแบบ SIP 200 OK (สำหรับ REGISTER หรือ INVITE)
        response = """SIP/2.0 200 OK
Via: SIP/2.0/UDP 192.168.11.252:5060;branch=z9hG4bKcc8f709eb5c343758043ddaa5;rport
From: "jeng" <sip:jeng@192.168.10.97>;tag=c7f80183
To: "jeng2" <sip:jeng2@192.168.10.97>;tag=9dd61ff61e802d8e2bef5f14621ef3c2
Call-ID: 6b86b273ff34fce19d6b804eff5a4f58@192.168.11.252:5060
CSeq: 1 REGISTER
Contact: <sip:jeng@192.168.11.252:5060;transport=UDP>
Content-Length: 0
"""

        # ส่ง SIP Response กลับไปยัง client
        sock.sendto(response.encode(), addr)
        print("Sent SIP 200 OK response back to client")

    except Exception as e:
        print(f"Error: {e}")
