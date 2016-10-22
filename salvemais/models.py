from datetime import datetime, timedelta
from flask import current_app

from . import db
from .util import cell_chart, protein_chart


class BloodType(db.Document):
    cell = db.StringField(required=True, choices=('A', 'B', 'AB', 'O'))
    protein = db.StringField(required=True, choices=('+', '-'))

    @classmethod
    def get(cls, blood_type=None, **kwargs):
        if blood_type:
            cell, protein = blood_type[:-1], blood_type[-1:]
            if cell not in cell_chart or protein not in protein_chart:
                return []
            kwargs['cell'] = cell
            kwargs['protein'] = protein

        try:
            blood = BloodType.objects.get(**kwargs)
        except cls.DoesNotExist:
            blood = BloodType(**kwargs).save()
        return blood

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

    def __unicode__(self):
        return '{}{}'.format(self.cell, self.protein)

# pre-load blood types
for cell in cell_chart:
    for protein in protein_chart:
        BloodType.get(cell=cell, protein=protein)


class Address(db.EmbeddedDocument):
    street = db.StringField(max_length=150)
    number = db.StringField(max_length=15)
    complement = db.StringField(max_length=50)
    district = db.StringField(max_length=50)
    city = db.StringField(max_length=50)
    state = db.StringField(max_length=2)
    cep = db.StringField(max_length=8)


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
    blood_type = db.ReferenceField(BloodType)
    cpf = db.StringField()
    gender = db.StringField(choices=current_app.config['GENDERS'])
    birthday = db.DateTimeField()
    height = db.FloatField()
    weigth = db.FloatField()

    def grace_period(self):
        latest_donation = self.latest_donation
        today = datetime.now()
        return today - latest_donation.timestamp

    @property
    def latest_donation(self):
        return self.donations().orderby('timestamp')[0]

    @property
    def blood_volume(self):
        return current_app.config['BLOOD_RATIO'][self.gender] * self.weigth

    @property
    def years_old(self):
        return datetime.now().year - self.birthday.year

    @property
    def can_donate(self):
        age_check = 18 <= self.years_old <= 60

        weight_check = self.weigth >= 50 if self.weigth else True

        year_donations = self.donations(timestamp__gte=datetime.now() - timedelta(months=12)).count()
        if self.gender == 'M':
            month_range = 2  # 60 days
            yearly_amount = 4  # 4 donations/year
        else:
            month_range = 3  # 90 days
            yearly_amount = 3  # 3 donations/year
        month_donations = self.donations(timestamp__gte=datetime.now() - timedelta(months=month_range)).count()
        frequency_check = month_donations < 2 and year_donations < yearly_amount
        
        return age_check and weight_check and frequency_check

    def donations(self, **kwargs):
        return Donation.objects(donor=self, **kwargs)


class Hemocenter(User):
    address = db.EmbeddedDocumentField(Address)


class Donation(db.Document):
    donor = db.ReferenceField(Donor)
    hemocenter = db.ReferenceField(Hemocenter)
    timestamp = db.DateTimeField(default=datetime.now)
