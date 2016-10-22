#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
.. module:: utils.postmon_api
   :platform: Windows

.. moduleauthor:: Joao Daher <joao.daher@gmail.com>
"""
import re
import requests


class InvalidCepFormatException(Exception):
    """
    Represents an error of CEP formatting
    """
    def __init__(self, code):
        message = "The CEP {} provided must be in the format 00.000-000 (both dot and slash are optional)"
        super().__init__(message)


class Postmon:
    """
    Implements request to the Postmon API
    Still lacks of a request-limit technique to avoid being blacklisted when flooding API
    """
    API_URL = "http://api.postmon.com.br/"
    API_VERSION = "v1"

    CEP_REGEX = r'^[0-9]{2}.?[0-9]{3}\-?[0-9]{3}$'

    @classmethod
    def cep(cls, code):
        """
        Fetches online an address when given a zipcode.
        JSON parsing errors (due to API wrong format response) are suppressed
        :param code: Zipcode number
        :return: API response dict or None
        :raises:
        HTTPErrors: when unable to contact API

        """
        cleaned_code = cls.clean_code(code=code)
        url = "{}/{}/cep/{}".format(cls.API_URL, cls.API_VERSION, cleaned_code)
        response = requests.get(url=url)  # HTTP errors will be raised

        try:
            data = response.json()

            fields = {
                'state': 'estado',
                'cep': 'cep',
                'district': 'bairro',
                'city': 'cidade',
                'complement': 'complemento',
                'street': 'logradouro'
            }

            response = {}
            for new_field, old_field in fields.items():
                response[new_field] = data[old_field]

            return response
        except Exception as e:
            return {}

    @classmethod
    def clean_code(cls, code):
        """
        Validates and clean a CEP code
        :param code: CEP code
        :return: The sanitized CEP code, without dot and hyphen
        :raises:
        postmon_api.InvalidCEPFormatException, if wrong zipcode format
        """
        if not re.match(cls.CEP_REGEX, code):
            raise InvalidCepFormatException(code=code)
        return code.replace('.', '').replace('-', '')

