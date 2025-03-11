import socket
import threading
import re

SIP_PORT = 5060
RTP_PORT = 4000

sip_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sip_sock.bind(("0.0.0.0", SIP_PORT))

rtp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
rtp_sock.bind(("0.0.0.0", RTP_PORT))

print(f"📡 SIP Server is running on port {SIP_PORT}")
print(f"🎙️ RTP Server is listening on port {RTP_PORT}")


def handle_rtp():
    while True:
        try:
            rtp_data, rtp_addr = rtp_sock.recvfrom(2048)
            print(f"🔊 Received RTP audio from {rtp_addr}")
            rtp_sock.sendto(rtp_data, rtp_addr)
        except Exception as e:
            print(f"❌ Error: {e}")


def handle_sip():
    while True:
        try:
            data, addr = sip_sock.recvfrom(1024)
            request = data.decode()
            print(f"📥 Received SIP request from {addr}:\n{request}")

            # ใช้ regex เพื่อดึง username จาก SIP INVITE
            match = re.search(r"From: <sip:(.*?)@", request)
            if match:
                caller_username = match.group(1)
                print(f"📞 Incoming call from: {caller_username}")

            if request.startswith("INVITE"):
                sip_sock.sendto(b"SIP/2.0 100 Trying\r\n\r\n", addr)
                sip_sock.sendto(b"SIP/2.0 180 Ringing\r\n\r\n", addr)

                sip_response = f"""SIP/2.0 200 OK
Via: SIP/2.0/UDP {addr[0]}:5060
From: <sip:{caller_username}@{addr[0]}>
To: <sip:receiver@{addr[0]}>;tag=12345
Call-ID: 12345678@{addr[0]}
CSeq: 1 INVITE
Contact: <sip:receiver@{addr[0]}>
Content-Type: application/sdp
Content-Length: 100

v=0
o=- 0 0 IN IP4 {addr[0]}
s=VoIP Call
c=IN IP4 {addr[0]}
t=0 0
m=audio {RTP_PORT} RTP/AVP 0
a=rtpmap:0 PCMU/8000
"""

                sip_sock.sendto(sip_response.encode(), addr)
                print(f"✅ Sent SIP 200 OK to {caller_username}")
                print("🎧 Waiting for RTP audio...")

        except Exception as e:
            print(f"❌ Error: {e}")


sip_thread = threading.Thread(target=handle_sip)
sip_thread.daemon = True
sip_thread.start()

rtp_thread = threading.Thread(target=handle_rtp)
rtp_thread.daemon = True
rtp_thread.start()

while True:
    pass
