from requests import get
# from iso3166 import countries_by_alpha2


class NordApi(object):
    """nordapi - Fetch VPN Endpoints
    Interact with the undocumented, but publicly exposed API from NordVPN
    """

    def __init__(self, limit=10, cap=30):
        """[initialization]

        Args:
            cap (int, optional): Maximum server load. 0-100. Defaults to 30.
            limit (int, optional): Number of results. Defaults to 10.
        """
        assert type(cap) == int and type(limit) == int

        self.url = "https://api.nordvpn.com"
        self.cap = cap
        self.limit = limit
        self.country = None
        self.cid = None

    def get_request(self, endpoint, payload=None):
        assert type(endpoint) == str
        if payload is None:
            payload = {}
        else:
            assert type(payload) is dict

        try:
            response = get(self.url + endpoint, params=payload)
            response.raise_for_status()
        except response.exceptions.RequestException as e:
            raise Exception(e)

        print(str(response.status_code) + ' : ' + response.url)
        return response

    def bisect_search(self, L, keyinput, keyoutput, match):
        if len(L) == 0:
            raise Exception('empty list. no value found.')
        elif len(L) < 2:
            raise Exception(str(match) + ' not found.')
        else:
            middle = len(L) // 2
            if match.lower() == L[middle][keyinput].lower():
                return L[middle][keyoutput]
            elif match.lower() > L[middle][keyinput].lower():
                return self.bisect_search(
                    L[middle:], keyinput, keyoutput, match
                )
            else:
                return self.bisect_search(
                    L[:middle], keyinput, keyoutput, match
                )

    def get_country_id(self, country):
        assert type(country) == str
        self.country = country
        endpoint = "/v1/servers/countries"
        key_input = "name"
        key_output = "id"

        # response is sorted A-Z on 'name' and id's are ascending
        response = self.get_request(endpoint)

        self.cid = (self.bisect_search(
            response.json(), key_input, key_output, country))

        return self.cid

    def get_recommended(self):
        assert type(
            self.cid) == int, "Country ID must be defined and an integer"
        # ex: /v1/servers/recommendations?filters[country_id]=227&limit=3
        endpoint = "/v1/servers/recommendations"
        payload = {'limit': self.limit, 'filters[country_id]': self.cid}

        return self.get_request(endpoint, payload).json()

    def set_limit(self, newlimit):
        assert type(newlimit) == int, "Limit must be an integer"
        self.limit = newlimit

    def set_capacity(self, newcapacity):
        assert type(newcapacity) == int, "Capacity must be an integer"
        self.cap = newcapacity
