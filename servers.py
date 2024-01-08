#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import Optional, TypeVar
from abc import ABC, abstractmethod
import re
import string


# Gotowe (Maria)
class Product:
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą argumenty wyrażające nazwę produktu (typu str) i jego cenę (typu float) -- w takiej kolejności -- i ustawiającą atrybuty `name` (typu str) oraz `price` (typu float)
    def __init__(self, name: string, price: float):
        if re.fullmatch("^[a-zA-Z]+\\d+$", name):
            self.name = name
            self.price = price
        else:
            raise ValueError

    def __eq__(self, other):
        return (self.name == other.name) and (self.price == other.price)  # FIXME: zwróć odpowiednią wartość

    def __hash__(self):
        return hash((self.name, self.price))


class Server(ABC):
    _n_max_returned_entries = 3

    def __init__(self):
        pass

    @abstractmethod
    def get_entries(self, n_letters: int) -> list[Product]:
        raise NotImplementedError


class ServerError(Exception):
    def __init__(self, server, msg=None):
        if msg is None:
            msg = f"An error occured with server {server}"
        super().__init__(msg)
        self.server = server


class TooManyProductsFoundError(ServerError):
    def __init__(self, server, n_returned_elem, n_max):
        super().__init__(server,
                         msg=f"The maximum number of elements that can be returned is {n_max}, but {n_returned_elem} were returned")
        self.n_returned_elem = n_returned_elem
        self.n_max = n_max


class ListServer(Server):
    def __init__(self, products: list[Product]):
        super().__init__()
        self.__products = products

    def get_entries(self, n_letters: int) -> list[Product]:
        pattern = r'^[a-zA-Z]{' + str(n_letters) + r'}\d{2,3}$'
        lst = [product for product in self.__products if re.fullmatch(pattern, product.name)]

        if len(lst) == 0:
            return []

        if len(lst) > self._n_max_returned_entries:
            raise TooManyProductsFoundError(self, len(lst), self._n_max_returned_entries)

        return sorted(lst, key=lambda product: product.price)


class MapServer(Server):
    def __init__(self, products: list[Product]):
        super().__init__()
        self.__products = {product.name: product for product in products}

    def get_entries(self, n_letters: int) -> list[Product]:
        pattern = r'^[a-zA-Z]{' + str(n_letters) + r'}\d{2,3}$'
        lst = [product for name, product in self.__products.items() if re.fullmatch(pattern, name)]

        if len(lst) == 0:
            return []

        if len(lst) > self._n_max_returned_entries:
            raise TooManyProductsFoundError(self, len(lst), self._n_max_returned_entries)

        return sorted(lst, key=lambda product: product.price)


HelperType = TypeVar('HelperType', bound=Server)


class Client:
    def __init__(self, server: HelperType):
        self.__server = server

    def get_total_price(self, n_letters: Optional[int]) -> Optional[float]:
        try:
            p = self.__server.get_entries(n_letters)
        except TooManyProductsFoundError:
            return None

        if len(p):
            return sum([x.price for x in p])
        else:
            return None
