# !/usr/bin/env python
# encoding: utf-8

import hprose


def main():
    client = hprose.HttpClient('http://127.0.0.1:8080/')
    print(client.hello("World"))


if __name__ == '__main__':
    main()