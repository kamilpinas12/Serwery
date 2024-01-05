#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import Optional
from abc import ABC, abstractmethod
import re




#Zrobię klasę Product (Maria)
class Product:
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą argumenty wyrażające nazwę produktu (typu str) i jego cenę (typu float) -- w takiej kolejności -- i ustawiającą atrybuty `name` (typu str) oraz `price` (typu float)

    # wiem że nie ja to miałem pisać ale dodaje żeby mi błędu nie pokazywało jak się będę do name i price odwoływał
    def __init__(self, name, price):
        self.name = name
        self.price = price


    def __eq__(self, other):
        return None  # FIXME: zwróć odpowiednią wartość

    def __hash__(self):
        return hash((self.name, self.price))


class Server(ABC):
    def __init__(self):
        self._n_max_returned_entries = 3

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
        self.products = products

    def get_entries(self, n_letters: int) -> list[Product]:
        pattern = r'^[a-zA-Z]{' + str(n_letters) + r'}\d{2,3}$'
        lst = [product for product in self.products if re.fullmatch(pattern, product.name)]

        if len(lst) == 0:
            return []

        if len(lst) >= self._n_max_returned_entries:
            raise TooManyProductsFoundError(self, len(lst), self._n_max_returned_entries)

        return sorted(lst, key=lambda product: product.price)


class MapServer(Server):
    def __init__(self, products: list[Product]):
        super().__init__()
        self.products = {}
        for product in products:
            products[product.name] = product

    def get_entries(self, n_letters: int) -> list[Product]:
        pattern = r'^[a-zA-Z]{' + str(n_letters) + r'}\d{2,3}$'
        lst = [product for name, product in self.products if re.fullmatch(pattern, name)]

        if len(lst) == 0:
            return []

        if len(lst) >= self._n_max_returned_entries:
            raise TooManyProductsFoundError(self, len(lst), self._n_max_returned_entries)

        return sorted(lst, key=lambda product: product.price)


class Client:
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą obiekt reprezentujący serwer

    def get_total_price(self, n_letters: Optional[int]) -> Optional[float]:
        raise NotImplementedError()
