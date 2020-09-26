from NordApi import NordApi


class OpenVpnUdp(NordApi):

    def get_file(self, country, fname=None):
        assert type(country) == str
        NordApi.get_country_id(self, country)
        NordApi.set_limit(self, 1)

        json = NordApi.get_recommended(self)
        self.servername = json[0]['hostname']
        self.load = json[0]['load']

        self.url = "https://downloads.nordcdn.com"
        endpoint = (
            '/configs/files/ovpn_udp/servers/'
            + self.servername
            + '.udp.ovpn'
        )

        response = NordApi.get_request(self, endpoint)

        filename = self.servername + '.udp.ovpn'
        writebytes = open(filename, 'wb')
        try:
            writebytes.write(response.content)
        finally:
            writebytes.close()

        return filename
