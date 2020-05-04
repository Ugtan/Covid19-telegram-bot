import os

import requests

_URL = "https://corona.lmao.ninja/v2"


class Covid19:
    def __str__(self):
        return self.cases

    def __repr__(self):
        return repr(self.__data)

    def __init__(self, data):
        self.__data = data

    @property
    def cases(self):
        return self.__data['cases']

    @property
    def active(self):
        return self.__data['active']

    @property
    def recovered(self):
        return self.__data['recovered']

    @property
    def deaths(self):
        return self.__data['deaths']

    @property
    def today_cases(self):
        return self.__data['todayCases']

    @property
    def today_recovered(self):
        return self.__data['todayRecovered']

    @property
    def today_deaths(self):
        return self.__data['todayDeaths']

    @property
    def country(self):
        _country = self.__data.get('country', None)
        if _country is None:
            return "Global"
        return _country


def getData(endpoint, params={}):
    """ Send get request and returns json response"""
    response = requests.get(os.path.join(_URL, endpoint), {**params})
    response.raise_for_status()
    return response.json() if response else False


def getByCountry(country, data):
    """ To get Covid19 cases by country"""
    country = country.strip().lower()
    return Covid19(next((d for d in data if d["country"].strip().lower() == country), None))


def getAllCountries():
    """To get all the countries affected by Covid-19"""
    params = {'yesterday': True, 'sort': True}
    data = getData("countries", params=params)
    return [d['country'].lower() for d in data]
