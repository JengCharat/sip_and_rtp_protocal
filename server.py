from pyVoIP.VoIP import InvalidStateError, VoIPPhone


def answer(
    call,
):  # This will be your callback function for when you receive a phone call.
    try:
        call.answer()
        call.hangup()
    except InvalidStateError:
        pass


if __name__ == "__main__":
    phone = VoIPPhone(
        "192.168.10.97",
        5060,
        "jeng",
        "",
        callCallback=answer,
        myIP="192.168.11.252",
        sipPort=5060,
        rtpPortLow=10000,
        rtpPortHigh=10000,
    )
    phone.start()
    input("Press enter to disable the phone")
    phone.stop()
