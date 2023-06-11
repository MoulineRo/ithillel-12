import json
import pathlib
import unittest

import responses
from exchange.exchange_provider import MonoExchange,NbuExchange, PrivatExchange,VkurseExchange

root = pathlib.Path(__file__).parent

class TestStringMethods(unittest.TestCase):
    # @responses.activate
    # def test_minfin(self):
    #     mocked_response = json.load(open(root / "fixtures/minfin_response.json"))
    #     responses.get(
    #         "https://api.minfin.com.ua/mb/51bafed21077e7a570ec1af587f35c1155bef903/",
    #         json=mocked_response,
    #     )
    #     e = MinfinExchange("minfin", "EUR", "UAH")
    #     e.get_rate()
    #     assert e.vendor == "minfin"
    #     assert e.currency_a == "EUR"
    #     assert e.currency_b == "UAH"
    #     assert e.pair.sell == 39.8077
    #     assert e.pair.buy == 39.4136


    @responses.activate
    def test_mono(self):
        mocked_response = json.load(open(root / "fixtures/mono_response.json"))
        responses.get(
            "https://api.monobank.ua/bank/currency",
            json=mocked_response,
        )
        e = MonoExchange("mono", "USD", "UAH")
        e.get_rate()
        assert e.vendor == "mono"
        assert e.currency_a == "USD"
        assert e.currency_b == "UAH"
        assert e.pair.sell == 37.4406
        assert e.pair.buy == 36.65

    @responses.activate
    def test_nbu(self):
        mocked_response = json.load(open(root / "fixtures/nbu_response.json"))
        responses.get(
            "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json",
            json=mocked_response,
        )
        e = NbuExchange("nbu", "USD", "UAH")
        e.get_rate()
        assert e.vendor == "nbu"
        assert e.currency_a == "USD"
        assert e.currency_b == "UAH"
        assert e.pair.sell == 38.0686
        assert e.pair.buy == 36.5686

    @responses.activate
    def test_privat(self):
        mocked_response = json.load(open(root / "fixtures/privat_response.json"))
        responses.get(
            "https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11",
            json=mocked_response,
        )
        e = PrivatExchange("privat", "USD", "UAH")
        e.get_rate()
        assert e.vendor == "privat"
        assert e.currency_a == "USD"
        assert e.currency_b == "UAH"
        assert e.pair.sell == 37.45318
        assert e.pair.buy == 36.5686

    @responses.activate
    def test_vkurse(self):
        mocked_response = json.load(open(root / "fixtures/vkurse_response.json"))
        responses.get(
            "https://vkurse.dp.ua/course.json",
            json=mocked_response,
        )
        e = VkurseExchange("vkurse", "USD", "UAH")
        e.get_rate()
        assert e.vendor == "vkurse"
        assert e.currency_a == "USD"
        assert e.currency_b == "UAH"
        assert e.pair.sell == 37.5
        assert e.pair.buy == 37.35

if __name__ == "__main__":
    unittest.main()
