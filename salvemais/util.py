
# Receiver to Donor
cell_chart = {
    'A':  {'A': True,  'B': False, 'AB': False, 'O': True},
    'B':  {'A': False, 'B': True,  'AB': False, 'O': True},
    'AB': {'A': True,  'B': True,  'AB': True,  'O': True},
    'O':  {'A': False, 'B': False, 'AB': False, 'O': True},
              }

# Receiver to Donor
protein_chart = {
    '+': {'+': True, '-': True},
    '-': {'+': False, '-': True},
                 }
