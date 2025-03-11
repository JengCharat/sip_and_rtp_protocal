import socket
import time

import pyaudio

SIP_SERVER = "0.0.0.0"  # IP ของ SIP Server
SIP_PORT = 5060
CLIENT_IP = "0.0.0.0"  # IP ของ Client
CLIENT_PORT = 5062  # SIP Client ใช้พอร์ตนี้
RTP_PORT = 4000  # พอร์ตที่ใช้ส่งเสียง RTP

# รับ username จากผู้ใช้
username = input("👤 Enter your username: ")

# ตั้งค่า PyAudio
p = pyaudio.PyAudio()
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 8000
CHUNK = 200
WIDTH = 2

input_stream = p.open(
    format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK
)
output_stream = p.open(
    format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK
)

# สร้าง UDP socket สำหรับ SIP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((CLIENT_IP, CLIENT_PORT))

sip_invite_body = f"""v=0
o=- 0 0 IN IP4 {CLIENT_IP}
s=VoIP Call
c=IN IP4 {CLIENT_IP}
t=0 0
m=audio {RTP_PORT} RTP/AVP 0
a=rtpmap:0 PCMU/8000
"""

content_length = len(sip_invite_body)

sip_invite = f"""INVITE sip:receiver@{SIP_SERVER} SIP/2.0
Via: SIP/2.0/UDP {CLIENT_IP}:{CLIENT_PORT};branch=z9hG4bK776asdhds
Max-Forwards: 70
To: <sip:receiver@{SIP_SERVER}>
From: <sip:{username}@{CLIENT_IP}>;tag=1928301774
Call-ID: 12345678@{CLIENT_IP}
CSeq: 1 INVITE
Contact: <sip:{username}@{CLIENT_IP}>
Content-Type: application/sdp
Content-Length: {content_length}

{sip_invite_body}
"""

try:
    # ส่ง SIP INVITE ไปหา SIP Server
    sock.sendto(sip_invite.encode(), (SIP_SERVER, SIP_PORT))
    print(f"📨 SIP INVITE sent as {username}")

    # รับ Response จาก Server
    response, _ = sock.recvfrom(1024)
    print("📩 Response from server:")
    print(response.decode())

    # เปิด RTP socket สำหรับส่งเสียง
    rtp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    print("🎙️ Sending RTP audio packets...")

    while True:
        audio_data = input_stream.read(CHUNK)
        rtp_packet = b"\x80\x78\x00\x01" + audio_data  # RTP header + ข้อมูลเสียง
        rtp_sock.sendto(rtp_packet, (SIP_SERVER, RTP_PORT))
        time.sleep(0.01)

        # รับ RTP Audio packets
        rtp_data, _ = rtp_sock.recvfrom(1024)
        output_stream.write(rtp_data[4:])  # ข้าม RTP header เพื่อให้เล่นเสียง

except Exception as e:
    print(f"❌ Error: {e}")
finally:
    try:
        if input_stream.is_active():
            input_stream.stop_stream()
        if output_stream.is_active():
            output_stream.stop_stream()
    except OSError:
        print("Stream is not open.")
    input_stream.close()
    output_stream.close()
    p.terminate()
    sock.close()
    rtp_sock.close()
