#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
from collections import Counter

from servers import ListServer, Product, Client, MapServer, TooManyProductsFoundError

server_types = (ListServer, MapServer)


class TestProducts(unittest.TestCase):
    def test_product_init(self):
        p = Product("ab12", 1)
        self.assertEqual(p.name, "ab12")
        self.assertEqual(p.price, 1)

        # incorrect entry
        entry = ["aBc", "32hf", "A522h2", "gGg5d", " g7A", "66As", "53"]
        for i in entry:
            with self.assertRaises(ValueError, msg=f"{i} entry didn't raised error"):
                p = Product(i, 1)

    def test_eq(self):
        p1 = Product("ab12", 12)
        p2 = Product("aB12", 12)
        p3 = Product("ab12", 11)
        p4 = Product("ab12", 12)

        self.assertNotEquals(p1, p2)
        self.assertEqual(p1, p4)
        self.assertNotEquals(p1, p3)


class ServerTest(unittest.TestCase):

    def test_get_entries_returns_proper_entries(self):
        products = [Product('P12', 1), Product('PP234', 2), Product('PP235', 1)]
        for server_type in server_types:
            server = server_type(products)
            entries = server.get_entries(2)
            self.assertEqual(Counter([products[2], products[1]]), Counter(entries))

    def test_to_many_products_found(self):
        products = [Product('P12', 1), Product('a12', 1), Product('b12', 1), Product('c12', 1)]

        for server_type in server_types:
            server = server_type(products)
            with self.assertRaises(TooManyProductsFoundError):
                server.get_entries(1)

    def test_order_of_returned_products(self):
        products = [Product('P12', 3), Product('a12', 4), Product('b12', 2)]
        correct_order = [2, 3, 4]
        for server_type in server_types:
            server = server_type(products)
            entries = server.get_entries(1)
            prices_lst = [product.price for product in entries]
            self.assertListEqual(prices_lst, correct_order, msg=f"{prices_lst} in server {server_type}")


class ClientTest(unittest.TestCase):
    def test_total_price_for_normal_execution(self):
        products = [Product('PP234', 2), Product('PP235', 3)]
        for server_type in server_types:
            server = server_type(products)
            client = Client(server)
            self.assertEqual(5, client.get_total_price(2))
        products = [Product('PP234', 2), Product('PP235', 3), Product('PPP235', 3),
                    Product('P234', 5), Product('P123', 2.2)]
        for server_type in server_types:
            server = server_type(products)
            client = Client(server)
            self.assertEqual(5, client.get_total_price(2))
            self.assertEqual(7.2, client.get_total_price(1))
            self.assertEqual(3, client.get_total_price(3))


if __name__ == '__main__':
    unittest.main()

