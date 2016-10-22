import re

from .app import db
from .util import cell_chart, protein_chart


class BloodType(db.Document):
    cell = db.StringField(required=True, choices=('A', 'B', 'AB', 'O'))
    protein = db.StringField(required=True, choices=('+', '-'))

    @classmethod
    def find(cls, blood_type):
        cell, protein = re.split(r'[ABO]{2}[+\-]', blood_type)
        return BloodType.objects.get(cell=cell, protein=protein)

    def can_donate(self, to_blood=None):
        pass

    def can_receive(self, from_blood=None):
        if from_blood:
            if isinstance(from_blood, str):
                from_blood = self.find(from_blood)
            match_cell = cell_chart[self.cell][from_blood.cell]
            match_protein = protein_chart[self.protein][from_blood.protein]

            return match_cell and match_protein

        matches = []
        for blood in BloodType.objects:
            match_cell = cell_chart[self.cell][blood.cell]
            match_protein = protein_chart[self.protein][blood.protein]

            if match_cell and match_protein:
                matches.append(blood)
        return matches


class Address(db.EmbeddedDocument):
    street = db.StringField(max_length=150)
    number = db.StringField(max_length=150)
    complement = db.StringField(max_length=150)
    district = db.StringField(max_length=150)
    city = db.StringField(max_length=150)
    state = db.StringField(max_length=150)
    cep = db.StringField(max_length=150)


class Facebook(db.EmbeddedDocument):
    user_id = db.StringField(max_length=150)
    api_token = db.StringField(max_length=150)


class Google(db.EmbeddedDocument):
    user_id = db.StringField(max_length=150)
    api_token = db.StringField(max_length=150)


class User(db.Document):
    email = db.StringField(required=True)
    name = db.StringField(max_length=150)
    nickname = db.StringField(max_length=50)

    facebook = db.EmbeddedDocumentField(Facebook)
    google = db.EmbeddedDocumentField(Google)

    meta = {
        'abstract': True,
        'allow_inheritance': True
    }


class Donor(User):
    blood_type = db.RefereceField(to=BloodType)
    cpf = db.StringField()


class Hemocenter(User):
    address = db.EmbeddedDocumentField(Address)
