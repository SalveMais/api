# encoding:utf-8
import re
import requests

from flask_script import Manager

from salvemais import create_app


app = create_app(env='dev')

manager = Manager(app)


@manager.command
def load_hemocenters():
    from salvemais.models import Hemocenter, Address
    from salvemais.util.maps import GoogleMaps
    from salvemais.util.postmon_api import Postmon
    from bs4 import BeautifulSoup

    if Hemocenter.objects():
        return

    url = "http://www2.inca.gov.br/wps/wcm/connect/orientacoes/site/home/hemocentros"
    page = requests.get(url).read()
    soup = BeautifulSoup(page, "html.parser")

    for row in soup.find("div", {"id": "conteudo"}).findAll('p'):
        for item in row.findAll('strong'):
            c = item.next
            if c.name == 'u':
                continue  # ex: Região Nordeste
            elif c.name == 'br':
                c = c.next

            name_row = str(c)

            c = c.next.next
            address_row = str(c)
            cep = re.findall(r'[0-9]{5}-[0-9]{3}', address_row)[0]

            c = c.next.next
            phone_row = str(c)

            address_kwargs = {'cep': cep}
            address_kwargs.update(Postmon.cep(code=cep))
            address_kwargs.update(GoogleMaps.get_latlong(address_row))

            address = Address(**address_kwargs)
            Hemocenter(name=name_row, phone=phone_row, address=address).save()


@manager.command
def load_bloodtypes():
    from salvemais.models import Hemocenter, BloodType
    from salvemais.util.data import cell_chart, protein_chart

    if Hemocenter.objects():
        return

    for cell in cell_chart:
        for protein in protein_chart:
            BloodType.get(cell=cell, protein=protein)


if __name__ == '__main__':
    manager.run()
