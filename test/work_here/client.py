import socket

SIP_SERVER = "192.168.11.252"  # IP ของ SIP Server
SIP_PORT = 5060
CLIENT_IP = "192.168.11.252"  # IP ของเครื่อง Client
CLIENT_PORT = 5061  # SIP Client ใช้พอร์ตนี้
RTP_PORT = 4000  # พอร์ตที่ใช้ส่งเสียง RTP

# สร้าง UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((CLIENT_IP, CLIENT_PORT))

# สร้าง SIP INVITE + SDP (กำหนด RTP port)
sip_invite = f"""INVITE sip:jeng2@{SIP_SERVER} SIP/2.0
Via: SIP/2.0/UDP {CLIENT_IP}:{CLIENT_PORT};branch=z9hG4bK776asdhds
Max-Forwards: 70
To: <sip:jeng2@{SIP_SERVER}>
From: <sip:jeng@{CLIENT_IP}>;tag=1928301774
Call-ID: 12345678@{CLIENT_IP}
CSeq: 1 INVITE
Contact: <sip:jeng@{CLIENT_IP}>
Content-Type: application/sdp
Content-Length: 100

v=0
o=- 0 0 IN IP4 {CLIENT_IP}
s=VoIP Call
c=IN IP4 {CLIENT_IP}
t=0 0
m=audio {RTP_PORT} RTP/AVP 0
a=rtpmap:0 PCMU/8000
"""

try:
    # ส่ง INVITE ไปหา SIP Server
    sock.sendto(sip_invite.encode(), (SIP_SERVER, SIP_PORT))
    print("📨 SIP INVITE request sent.")

    # รับ Response จาก Server
    response, _ = sock.recvfrom(1024)
    print("📩 Response from server:")
    print(response.decode())

    # เปิด RTP Socket ส่งเสียง
    rtp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    print("🎙️ Sending RTP audio packets...")
    for i in range(10):  # ส่งเสียงตัวอย่าง 10 ครั้ง
        rtp_packet = b"\x80\x78\x00\x01" + b"\x00" * 160  # ส่งข้อมูลเสียง (PCMU 8kHz)
        rtp_sock.sendto(rtp_packet, (SIP_SERVER, RTP_PORT))

except Exception as e:
    print(f"❌ Error: {e}")
finally:
    sock.close()
    rtp_sock.close()
