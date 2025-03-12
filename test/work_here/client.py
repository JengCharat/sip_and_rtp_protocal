import socket
import time

import pyaudio

SIP_SERVER = "10.52.249.25"  # IP ของ SIP Server
SIP_PORT = 5060
CLIENT_IP = "10.52.249.25"  # IP ของ Client
CLIENT_PORT = 5062  # SIP Client ใช้พอร์ตนี้
RTP_PORT = 4000  # พอร์ตที่ใช้ส่งเสียง RTP

# ตั้งค่า PyAudio สำหรับจับเสียงจากไมโครโฟน
p = pyaudio.PyAudio()

# ตั้งค่าคุณภาพเสียง
FORMAT = pyaudio.paInt16  # ใช้ 16-bit PCM
CHANNELS = 1  # Mono
RATE = 8000  # Sampling rate 8kHz (ใช้สำหรับ PCMU)
CHUNK = 200  # จำนวนข้อมูลที่จับได้ในแต่ละครั้ง (แต่ละช่องเวลา 10ms)
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
# socket.SOCK_DGRAM: กำหนดประเภทของ socket เป็น UDP ซึ่งจะไม่เหมือนกับ TCP (Transmission Control Protocol)
# ที่ต้องมีการเชื่อมต่อและรับประกันความน่าเชื่อถือ (reliable) ในการส่งข้อมูล
sock.bind((CLIENT_IP, CLIENT_PORT))
# ผูกเพื่อให้สามารถรับและส่งข้อมูลกันได้

# ข้อความ SIP INVITE + SDP (กำหนด RTP port)
# v = 0 = sdp_version

# o=- 0 0 IN IP4 {CLIENT_IP} ส่วนนี้บอกถึงข้อมูลของ origin หรือผู้เริ่มต้นการเชื่อมต่อ
# o=- ชื่อของผู้เริ่มต้นเป็น - ซึ่งหมายความว่าไม่มีชื่อผู้ใช้งานที่ถูกระบุ
# 0 0: หมายเลขการแก้ไข (version) ของการเชื่อมต่อ
# IN IP4 {CLIENT_IP}: ใช้โปรโตคอล IPv4 และที่อยู่ IP ของเครื่องที่จะรับสัญญาณ

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

# INVITE: หมายถึงคำขอที่ต้องการเชื่อมต่อหรือเริ่มต้นการโทร
# ip:jeng2@{SIP_SERVER}: ระบุปลายทางของการโทร โดย jeng2@{SIP_SERVER} คือ URI (Uniform Resource Identifier) ของผู้รับปลายทางที่ต้องการติดต่อ
# SIP/2.0: เวอร์ชันของโปรโตคอล SIP ที่ใช้งาน ซึ่งในที่นี้คือ SIP เวอร์ชัน 2.0


# Via: SIP/2.0/UDP {CLIENT_IP}:{CLIENT_PORT};branch=z9hG4bK776asdhds:
# ระบุ Via header เพื่อบ่งบอกเส้นทางที่ข้อความนี้เดินทางไป
# SIP/2.0/UDP: หมายถึงโปรโตคอล SIP ใช้ UDP สำหรับการส่งข้อมูล
# branch=z9hG4bK776asdhds: ตัวระบุเฉพาะสำหรับ SIP transaction ที่ช่วยในการจัดการหลายคำขอพร้อมกัน
# Max-Forwards: 70กำหนดจำนวนครั้งสูงสุดที่ SIP message นี้สามารถถูกส่งผ่านเซิร์ฟเวอร์หรือพร็อกซี่ก่อนที่จะถูกลบ (ใช้เพื่อป้องกันวงจรการวนลูป)


# To: <sip:jeng2@{SIP_SERVER}>:
# ระบุผู้รับ (Recipient) ของคำขอ SIP
# sip:jeng2@{SIP_SERVER}: URI ของผู้รับการโทร

# From: <sip:jeng@{CLIENT_IP}>;tag=1928301774:
# ระบุผู้ส่ง (Sender) ของคำขอ SIP
# sip:jeng@{CLIENT_IP}: URI ของผู้ส่ง
# tag=1928301774: Tag ที่ใช้เพื่อแยกแยะการติดต่อหลายครั้ง


# Call-ID: 12345678@{CLIENT_IP}:ตัวระบุที่ไม่ซ้ำสำหรับแต่ละการโทร (แต่ละเซสชันการโทร) ซึ่งใช้ในการติดตามคำขอ SIP ที่เกี่ยวข้องกัน

# Contact: <sip:jeng@{CLIENT_IP}>:ระบุ URI ที่ใช้ติดต่อผู้ส่งคำขอ SIP
# sip:jeng@{CLIENT_IP}: หมายเลขที่ติดต่อของผู้ส่ง

# Content-Type: application/sdp:กำหนดประเภทของเนื้อหาภายในคำขอ SIP ว่าเป็น SDP (Session Description Protocol) ซึ่งใช้ในการระบุรายละเอียดของเซสชัน (เช่น codec, IP, port, เป็นต้น)

# Content-Length: {content_length}:ะบุความยาวของเนื้อหาภายในคำขอ SIP

# {sip_invite_body}:
# sip_invite_body เป็นตัวแปรที่ประกอบไปด้วยรายละเอียดเพิ่มเติมของการเชื่อมต่อที่ใช้ SDP ซึ่งจะระบุเกี่ยวกับการตั้งค่าของเซสชันเสียง เช่น codec ที่จะใช้ (เช่น PCMU), ที่อยู่ IP และพอร์ต RTP

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
    # socket.SOCK_DGRAM -> ใช้ UDP ซึ่งเป็นพื้นฐานของ RTP

    print("🎙️ Sending RTP audio packets...")

    while True:
        # อ่านข้อมูลเสียงจากไมโครโฟน
        audio_data = input_stream.read(CHUNK)

        # สร้าง RTP packet (เริ่มต้น RTP header)
        rtp_packet = b"\x80\x78\x00\x01" + audio_data  # RTP header + ข้อมูลเสียง

        # ส่ง RTP packet ไปที่ SIP Server
        rtp_sock.sendto(rtp_packet, (SIP_SERVER, RTP_PORT))
        time.sleep(0.01)  # เพิ่มเวลาหน่วงทุก 10ms

        # รับ RTP Audio packets
        rtp_data, _ = rtp_sock.recvfrom(1024)
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
