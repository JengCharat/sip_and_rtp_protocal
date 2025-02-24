import time
import wave

from pyVoIP.VoIP import CallState, InvalidStateError, VoIPPhone


def answer(call):
    try:
        f = wave.open("announcment.wav", "rb")
        frames = f.getnframes()
        data = f.readframes(frames)
        f.close()

        call.answer()
        call.write_audio(
            data
        )  # This writes the audio data to the transmit buffer, this must be bytes.

        stop = time.time() + (
            frames / 8000
        )  # frames/8000 is the length of the audio in seconds. 8000 is the hertz of PCMU.

        while time.time() <= stop and call.state == CallState.ANSWERED:
            time.sleep(0.1)
        call.hangup()
    except InvalidStateError:
        pass
    except:
        call.hangup()


if __name__ == "__main__":
    phone = VoIPPhone(
        "192.168.10.97", 5060, "jeng", "", myIP="192.168.11.252", callCallback=answer
    )
    phone.start()
    input("Press enter to disable the phone")
    phone.stop()
