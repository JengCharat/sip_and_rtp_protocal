import socket

# ตั้งค่า SIP Server และพอร์ต
SIP_SERVER = "0.0.0.0"
SIP_PORT = 5060

# สร้างข้อความ SIP INVITE
sip_invite = """INVITE sip:jeng2@192.168.10.97 SIP/2.0
Via: SIP/2.0/UDP 192.168.10.97;branch=z9hG4bK776asdhds
Max-Forwards: 70
To: jeng2 <sip:jeng2@192.168.10.97>
From: jeng <sip:jeng@192.168.11.252>;tag=1928301774
Call-ID: a84b4c76e66710@192.168.10.97
CSeq: 314159 INVITE
Contact: <sip:jeng@192.168.11.252>
Content-Type: application/sdp
Content-Length: 142

"""

# สร้าง UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    # ส่งข้อมูลไปยัง SIP Server
    sock.sendto(sip_invite.encode(), (SIP_SERVER, SIP_PORT))
    print("SIP INVITE request sent successfully.")

    # รับคำตอบจากเซิร์ฟเวอร์ (ถ้ามี)
    response, _ = sock.recvfrom(1024)  # กำหนด buffer size 1024 bytes
    print("Response from server:")
    print(response.decode())
except Exception as e:
    print(f"Error: {e}")
finally:
    sock.close()
