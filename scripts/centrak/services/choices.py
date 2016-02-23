ACCT_STATUS = (
    ('unknown',         'Yet to be Determined'),
    ('new',             'New'),
    ('active',          'Active'),
    ('inactive',        'Inactive'),
    ('not-conn',        'Not Connected'),
    ('disconn-bill',    'Disconnected (Has Bill)'),
    ('disconn-no-bill', 'Disconnected (No Bill)'),
    ('n-a',             'Not Applicable'),
)

TARIFF = (
    ('R1',   'R1'),
    ('R2.A', 'R2.A'),
    ('R2.B', 'R2.B'),
    ('R3',   'R3'),
    ('R4',   'R4'),
    ('C1.A', 'C1.A'),
    ('C1.B', 'C1.B'),
    ('C2',   'C2'),
    ('C3',   'C3'),
    ('D1',   'D1'),
    ('D2',   'D2'),
    ('D3',   'D3'),
    ('A1',   'A1'),
    ('A2',   'A2'),
    ('A3',   'A3'),
    ('L1',   'L1'),
)
TARIFF_NEW = TARIFF

METER_TYPE = (
    ('none',    'None'),
    ('analog',  'Analog'),
    ('ppm',     'Prepaid Meter (PPM)'),
)

METER_BRAND = (
    ('conlog',   'Conlog'),
    ('momas',    'Momas'),
    ('elsewedy', 'Elsewedy'),
    ('zte',      'ZTE'),
)

METER_STATUS = (
    ('unknown',     'Yet to be Determined'),
    ('n-a',         'Not Applicable'),
    ('none',        'None'),
    ('ok',          'OK'),
    ('bypass',      'By-Pass'),
    ('burnt',       'Burnt'),
    ('faulty',      'Faulty'),
    ('abandoned',   'Abandoned'),
    ('removed',     'Removed'),
    ('stolen',      'Stolen'),
    ('other',       'Other')
)

METER_LOCATION = (
    ('n-a',     'Not Applicable'),
    ('inside-premises',  'Inside the Property'),
    ('outside-premises', 'Outside the Property'),
    ('inside-building',  'Inside the Building'),
    ('outside-building', 'Outside the Building'),
)

PLOT_TYPE = (
    ('residence',   'Residence'),
    ('flats-estate',  'Flats/Estate'),
    ('commercial',    'Commercial'),
    ('factory-ind',   'Factory/Industry'),
    ('farm',          'Farm Land'),
    ('hospital',      'Hospital/Clinic'),
    ('mosque',        'Mosque'),
    ('church',        'Church'),
    ('school',        'School'),
    ('v-plot',        'Vacant Plot'),
    ('v-residence',   'Vacant Residence'),
    ('v-commercial',  'Vacant Commercial'),
    ('u-building',    'Uncompleted Building'),
)

SUPPLY_SOURCE = (
    ('none',         'None'),
    ('disconnected', 'Disconnected'),
    ('pole',         'Pole'),
    ('neighbour',    'Neighbour')
)


