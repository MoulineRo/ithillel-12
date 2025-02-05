import abc
import dataclasses
import enum

import requests


class ExchangeCodes(enum.Enum):
    USD = 840
    EUR = 978
    UAH = 980


@dataclasses.dataclass(frozen=True)
class SellBuy:
    sell: float
    buy: float


class ExchangeBase(abc.ABC):
    """
    Base class for exchange providers, should define get_rate() method
    """

    def __init__(self, vendor, currency_a, currency_b):
        self.vendor = vendor
        self.currency_a = currency_a
        self.currency_b = currency_b
        self.pair: SellBuy = None

    @abc.abstractmethod
    def get_rate(self):
        raise NotImplementedError("Method get_rate() is not implemented")


class MonoExchange(ExchangeBase):
    def get_rate(self):
        a_code = ExchangeCodes[self.currency_a].value
        b_code = ExchangeCodes[self.currency_b].value
        r = requests.get("https://api.monobank.ua/bank/currency")
        r.raise_for_status()
        for rate in r.json():
            currency_code_a = rate["currencyCodeA"]
            currency_code_b = rate["currencyCodeB"]
            if currency_code_a == a_code and currency_code_b == b_code:
                self.pair = SellBuy(rate["rateSell"], rate["rateBuy"])

                return


class PrivatExchange(ExchangeBase):
    def get_rate(self):
        r = requests.get(
            "https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11"
        )
        r.raise_for_status()
        for rate in r.json():
            if rate["ccy"] == self.currency_a and rate["base_ccy"] == self.currency_b:
                self.pair = SellBuy(float(rate["sale"]), float(rate["buy"]))


class VkurseExchange(ExchangeBase):
    def get_rate(self):
        r = requests.get("https://vkurse.dp.ua/course.json")
        r.raise_for_status()
        for rate in r.json():
            if rate == "Dollar":
                if "USD" == self.currency_a and "UAH" == self.currency_b:
                    self.pair = SellBuy(
                        float(r.json()[rate]["sale"]), float(r.json()[rate]["buy"])
                    )
            elif rate == "Euro":
                if "EUR" == self.currency_a and "UAH" == self.currency_b:
                    self.pair = SellBuy(
                        float(r.json()[rate]["sale"]), float(r.json()[rate]["buy"])
                    )


class NbuExchange(ExchangeBase):
    def get_rate(self):
        a_code = ExchangeCodes[self.currency_a].value
        r = requests.get(
            "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json"
        )
        r.raise_for_status()
        for rate in r.json():
            if rate["r030"] == a_code:
                if rate["cc"] == self.currency_a and "UAH" == self.currency_b:
                    # тут трохи накинув на тому що апи НБУ дає тількі продаж
                    self.pair = SellBuy(float(rate["rate"] + 1.5), float(rate["rate"]))
            if rate["r030"] == a_code:
                if rate["cc"] == self.currency_a and "UAH" == self.currency_b:
                    # тут трохи накинув на тому що апи НБУ дає тількі продаж
                    self.pair = SellBuy(float(rate["rate"] + 1.5), float(rate["rate"]))


# class MinfinExchange(ExchangeBase):
#     def get_rate(self):
#         r = requests.get(
#             "https://api.minfin.com.ua/mb/51bafed21077e7a570ec1af587f35c1155bef903/"
#         )
#         r.raise_for_status()
#         for rate in r.json():
#             if rate["currency"] == "eur":
#                 if "EUR" == self.currency_a and "UAH" == self.currency_b:
#                     self.pair = SellBuy(float(rate["ask"]), float(rate["bid"]))
#                     break
#             if rate["currency"] == "usd":
#                 if "USD" == self.currency_a and "UAH" == self.currency_b:
#                     self.pair = SellBuy(float(rate["ask"]), float(rate["bid"]))
#                     break
