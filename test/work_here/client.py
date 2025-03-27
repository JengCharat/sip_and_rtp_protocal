import socket
import time

import pyaudio

SIP_SERVER = "192.168.11.252"  # IP ของ SIP Server
SIP_PORT = 5060
CLIENT_IP = "192.168.11.252"  # IP ของ Client
CLIENT_PORT = 5062  # SIP Client ใช้พอร์ตนี้
RTP_PORT = 4000  # พอร์ตที่ใช้ส่งเสียง RTP

# ตั้งค่า PyAudio สำหรับจับเสียงจากไมโครโฟน
p = pyaudio.PyAudio()

# ตั้งค่าคุณภาพเสียง
FORMAT = pyaudio.paInt16  # ใช้ 16-bit PCM
CHANNELS = 1  # Mono
RATE = 8000  # Sampling rate 8kHz (ใช้สำหรับ PCMU)
CHUNK = 1024  # จำนวนข้อมูลที่จับได้ในแต่ละครั้ง (แต่ละช่องเวลา 10ms)
WIDTH = 2  # ขนาดข้อมูลแต่ละ sample 2 byte

# เปิด Stream สำหรับจับเสียงจากไมโครโฟน (input stream)
input_stream = p.open(
    format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK
)

# เปิด Stream สำหรับ output เพื่อเล่นเสียงที่ได้รับจาก RTP
output_stream = p.open(
    format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK
)

# สร้าง UDP socket สำหรับ SIP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((CLIENT_IP, CLIENT_PORT))

# ข้อความ SIP INVITE + SDP (กำหนด RTP port)
sip_invite_body = f"""v=0 
o=- 0 0 IN IP4 {CLIENT_IP}
s=VoIP Call
c=IN IP4 {CLIENT_IP}
t=0 0
m=audio {RTP_PORT} RTP/AVP 0
a=rtpmap:0 PCMU/8000
"""

# คำนวณ Content-Length ของ SIP message
content_length = len(sip_invite_body)

# SIP INVITE message
sip_invite = f"""INVITE sip:jeng2@{SIP_SERVER} SIP/2.0
Via: SIP/2.0/UDP {CLIENT_IP}:{CLIENT_PORT};branch=z9hG4bK776asdhds
Max-Forwards: 70
To: <sip:jeng2@{SIP_SERVER}>
From: <sip:jeng@{CLIENT_IP}>;tag=1928301774
Call-ID: 12345678@{CLIENT_IP}
CSeq: 1 INVITE
Contact: <sip:jeng@{CLIENT_IP}>
Content-Type: application/sdp
Content-Length: {content_length}

{sip_invite_body}
"""

try:
    # ส่ง SIP INVITE ไปหา SIP Server
    sock.sendto(sip_invite.encode(), (SIP_SERVER, SIP_PORT))
    print("📨 SIP INVITE request sent.")

    # รับ Response จาก Server
    response, _ = sock.recvfrom(1024)
    print("📩 Response from server:")
    print(response.decode())

    # เปิด RTP socket สำหรับส่งเสียง
    rtp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    print("🎙️ Sending RTP audio packets...")

    # รับ RTP Audio packets จากเซิร์ฟเวอร์
    while True:
        # อ่านข้อมูลเสียงจากไมโครโฟน
        audio_data = input_stream.read(CHUNK)

        # สร้าง RTP packet (เริ่มต้น RTP header)
        rtp_packet = b"\x80\x78\x00\x01" + audio_data  # RTP header + ข้อมูลเสียง

        # ส่ง RTP packet ไปที่ SIP Server
        rtp_sock.sendto(rtp_packet, (SIP_SERVER, RTP_PORT))
        time.sleep(0.01)  # เพิ่มเวลาหน่วงทุก 10ms

        # รับ RTP Audio packets จากเซิร์ฟเวอร์ (ซึ่งจะ echo กลับ)
        rtp_data, _ = rtp_sock.recvfrom(1024)

        # แสดงข้อมูลของ RTP packet ที่ได้รับ
        print("🔊 Received RTP packet from server:")
        print(rtp_data)  # แสดงข้อมูล raw ของ RTP packet

        # เล่นเสียงที่ได้รับจาก RTP packet
        output_stream.write(rtp_data[4:])  # ข้าม RTP header เพื่อให้เล่นเสียง

except Exception as e:
    print(f"❌ Error: {e}")
finally:
    # ปิด Stream และ socket
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
