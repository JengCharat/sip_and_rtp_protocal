import socket

# ตั้งค่า SIP Server และพอร์ต
SIP_SERVER = "192.168.10.97"
SIP_PORT = 5060

# สร้างข้อความ SIP INVITE
sip_invite = """INVITE sip:jeng2@192.168.10.97 SIP/2.0
Via: SIP/2.0/TCP 192.168.10.97:50437;branch=z9hG4bK-524287-1---50a1b82113b5836c;rport
Max-Forwards: 70
Contact: <sip:jeng@192.168.10.97:39087;transport=TCP>
To: <sip:jeng2@192.168.10.97:5060>
From: <sip:jeng@192.168.10.97:5060;transport=TCP>;tag=247a3150
Call-ID: 2fRE4umJsIAuO9MtPlvnbh
CSeq: 1 INVITE
Allow: INVITE, ACK, CANCEL, BYE, NOTIFY, REFER, MESSAGE, OPTIONS, INFO, SUBSCRIBE
Content-Type: application/sdp
Supported: replaces, norefersub, extended-refer, timer, sec-agree, outbound, path, X-cisco-serviceuri
User-Agent: Z 5.6.6 v2.10.20.5
Allow-Events: presence, kpml, talk, as-feature-event
Content-Length: 324

v=0
o=Z 0 6264337 IN IP4 192.168.11.252
s=Z
c=IN IP4 192.168.10.97
t=0 0
m=audio 48072 RTP/AVP 106 9 98 101 0 8 3
a=rtpmap:106 opus/48000/2
a=fmtp:106 sprop-maxcapturerate=16000; minptime=20; useinbandfec=1
a=rtpmap:98 telephone-event/48000
a=fmtp:98 0-16
"""  # ปรับ Content-Length เป็น 324 ซึ่งตรงกับขนาดของบอดี้ (ข้อมูล SDP)

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
