import socket

# ตั้งค่า SIP Server และพอร์ต
SIP_SERVER = "192.168.10.97"
SIP_PORT = 5060

# สร้างข้อความ SIP REGISTER
sip_register = """REGISTER sip:192.168.10.97;transport=UDP SIP/2.0
Via: SIP/2.0/UDP 192.168.11.252:50955;branch=z9hG4bK-524287-1---f4ed12272415d2a9;rport
Max-Forwards: 70
Contact: <sip:jeng@192.168.11.252:50955;rinstance=fd382bde812fd899;transport=UDP>
To: <sip:jeng@192.168.10.97;transport=UDP>
From: <sip:jeng@192.168.10.97;transport=UDP>;tag=bf4e5101
Call-ID: DVY86cX2U5Jvqxrm48deJA..
CSeq: 14 REGISTER
Expires: 60
Allow: INVITE, ACK, CANCEL, BYE, NOTIFY, REFER, MESSAGE, OPTIONS, INFO, SUBSCRIBE
Supported: replaces, norefersub, extended-refer, timer, sec-agree, outbound, path, X-cisco-serviceuri
User-Agent: Z 5.6.6 v2.10.20.5
Allow-Events: presence, kpml, talk, as-feature-event
Content-Length: 0"""

# สร้าง UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    # ส่งข้อมูลไปยัง SIP Server
    sock.sendto(sip_register.encode(), (SIP_SERVER, SIP_PORT))
    print("SIP REGISTER request sent successfully.")

    # รับคำตอบจากเซิร์ฟเวอร์ (ถ้ามี)
    response, _ = sock.recvfrom(1024)  # กำหนด buffer size 1024 bytes
    print("Response from server:")
    print(response.decode())
except Exception as e:
    print(f"Error: {e}")
finally:
    sock.close()
