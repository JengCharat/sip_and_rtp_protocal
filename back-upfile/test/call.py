import socket

# ตั้งค่า SIP Server และพอร์ต
SIP_SERVER = "192.168.10.97"
SIP_PORT = 5060

# สร้าง SDP message
sdp_message = """v=0
o=Z 0 2826203 IN IP4 192.168.10.97
s=Z
c=IN IP4 192.168.10.97
t=0 0
m=audio 42052 RTP/AVP 106 9 98 101 0 8 3
a=rtpmap:106 opus/48000/2
a=fmtp:106 sprop-maxcapturerate=16000; minptime=20; useinbandfec=1
a=rtpmap:98 telephone-event/48000
a=fmtp:98 0-16
a=rtpmap:101 telephone-event/8000
a=fmtp:101 0-16
a=sendrecv
a=rtcp-mux"""

# คำนวณ Content-Length ใหม่
content_length = len(sdp_message.encode())

# สร้าง SIP INVITE request โดยใช้ Content-Length ที่คำนวณได้
sip_invite = f"""INVITE sip:jeng@192.168.10.97:5060;transport=TCP SIP/2.0
Via: SIP/2.0/TCP 192.168.10.97:36363;branch=z9hG4bK-524287-1---6b9f2ab20c54976b;rport
Max-Forwards: 70
Contact: <sip:jeng2@192.168.10.97:52671;transport=TCP>
To: <sip:jeng@192.168.10.97:5060>
From: <sip:jeng2@192.168.10.97:5060;transport=TCP>;tag=e3f8960d
Call-ID: SmMrxi03iSBUCE1ziov4kQT
CSeq: 3 INVITE
Allow: INVITE, ACK, CANCEL, BYE, NOTIFY, REFER, MESSAGE, OPTIONS, INFO, SUBSCRIBE
Content-Type: application/sdp
Supported: replaces, norefersub, extended-refer, timer, sec-agree, outbound, path, X-cisco-serviceuri
User-Agent: Z 5.6.6 v2.10.20.5
Allow-Events: presence, kpml, talk, as-feature-event
Content-Length: {content_length}

{sdp_message}"""

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
