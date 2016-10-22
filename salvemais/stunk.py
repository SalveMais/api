from .models import BloodType
from .util import cell_chart, protein_chart

for cell in cell_chart:
    for protein in protein_chart:
        blood_type_str = "{}{}".format(cell, protein)
        blood_type = BloodType.find(blood_type=blood_type_str)
        if not blood_type:
            BloodType(cell=cell, protein=protein).save()
