from xmlrpc.client import ServerProxy


def test_rpc():
    BirbServer = ServerProxy("http://localhost:8000")

    # Test sequence
    angle = 0.5
    print("Testing RPC calls...")
    BirbServer.set_angle("HeadYaw", angle)
    result = BirbServer.get_angle("HeadYaw")

    assert result == angle, f"should be {angle=}, got {result=}"
    print("Test passed!")
