import socket

# ตั้งค่า SIP Server และพอร์ต
SIP_SERVER = "192.168.10.97"
SIP_PORT = 5060

# สร้างข้อความ SIP INVITE
sip_invite = """INVITE sip:jeng@192.168.11.252:55392;rinstance=616b97526f7eaa52;transport=UDP SIP/2.0
Record-Route: <sip:192.168.10.97;lr>
Via: SIP/2.0/UDP 192.168.10.97;branch=z9hG4bK8552.1e53a36eace33dd8155f25c13838ed41.0
Via: SIP/2.0/UDP 192.168.11.252:55392;received=192.168.11.252;branch=z9hG4bK-524287-1---32b535bdb3a4fd7c;rport=55392
Max-Forwards: 69
Contact: <sip:jeng@192.168.11.252:55392;transport=UDP>
To: <sip:jeng@192.168.10.97>
From: <sip:jeng@192.168.10.97;transport=UDP>;tag=70d7b60b
Call-ID: 7HHYjUFDAQ-E8iV3w9u8Uw..
CSeq: 1 INVITE
Allow: INVITE, ACK, CANCEL, BYE, NOTIFY, REFER, MESSAGE, OPTIONS, INFO, SUBSCRIBE
Content-Type: application/sdp
Supported: replaces, norefersub, extended-refer, timer, sec-agree, outbound, path, X-cisco-serviceuri
User-Agent: Z 5.6.6 v2.10.20.5
Allow-Events: presence, kpml, talk, as-feature-event
Content-Length: 346

v=0
o=Z 0 1432295756 IN IP4 192.168.11.252
s=Z
c=IN IP4 192.168.11.252
t=0 0
m=audio 58709 RTP/AVP 106 9 98 101 0 8 3
a=rtpmap:106 opus/48000/2
a=fmtp:106 sprop-maxcapturerate=16000; minptime=20; useinbandfec=1
a=rtpmap:98 telephone-event/48000
a=fmtp:98 0-16
a=rtpmap:101 telephone-event/8000
a=fmtp:101 0-16
a=sendrecv"""
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
