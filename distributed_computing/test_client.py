from xmlrpc.client import ServerProxy


def test_rpc():
    BirdServer = ServerProxy("http://localhost:8000")

    # Test sequence
    angle = 0.5
    print("Testing RPC calls...")
    BirdServer.set_angle("HeadYaw", angle)
    print(BirdServer.get_angle("HeadYaw"))

    result = BirdServer.get_angle("HeadYaw")
    print(f"{angle=} == {result=}")
    assert result == angle, f"should be {angle=}, got {result=}"

    # Test all functions
    print("\nTesting set/get angle...")
    BirdServer.set_angle("HeadYaw", 0.5)
    assert BirdServer.get_angle("HeadYaw") == 0.5

    print("\nTesting get_posture...")
    posture = BirdServer.get_posture()
    print(f"Posture: {posture=}")

    print("\nTesting execute_keyframes...")
    keyframes = [[0, {"HeadYaw": 0.5}], [1, {"HeadYaw": -0.5}]]
    assert BirdServer.execute_keyframes(keyframes)

    print("\nTesting set/get transform...")
    transform = [1.0, 2.0, 3.0]
    BirdServer.set_transform("Head", transform)
    result = BirdServer.get_transform("Head")
    assert result == transform

    print("Test passed!")


if __name__ == "__main__":
    test_rpc()
