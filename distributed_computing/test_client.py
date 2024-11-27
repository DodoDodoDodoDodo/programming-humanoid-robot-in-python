from xmlrpc.client import ServerProxy


def test_rpc():
    BirbServer = ServerProxy("http://localhost:8000")

    # Test sequence
    angle = 0.5
    print("Testing RPC calls...")
    BirbServer.set_angle("HeadYaw", angle)
    print(BirbServer.get_angle("HeadYaw"))

    result = BirbServer.get_angle("HeadYaw")
    print(f"{angle=} == {result=}")
    assert result == angle, f"should be {angle=}, got {result=}"

    # Test all functions
    print("\nTesting set/get angle...")
    BirbServer.set_angle("HeadYaw", 0.5)
    assert BirbServer.get_angle("HeadYaw") == 0.5

    print("\nTesting get_posture...")
    posture = BirbServer.get_posture()
    print(f"Posture: {posture=}")

    print("Test passed!")


if __name__ == "__main__":
    test_rpc()
