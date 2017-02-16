import socket


class UDPCannon:
    """
    UDPCannon application

    :author Matt Turi (mturi@mort11.org)
    """

    port = 0  # Default port
    client_address = "0.0.0.0"  # Default client address
    socket = None
    message = ""

    def __init__(self, client_address, client_port):
        self.client_address = client_address
        self.client_port = client_port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_targets(self, center_x, center_y, distance, angle):
        self.message = """
        ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
        ||||||||||||||||||||||||||||[{0}~{1}~{2}~{3}]||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
        ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
        """.format(center_x, center_y, distance, angle)
        # print "Packet size: " + str(sys.getsizeof(message))
        self.socket.sendto(str(self.message), (self.client_address, self.client_port))
