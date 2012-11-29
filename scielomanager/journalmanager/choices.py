# coding: utf-8
import calendar

SCIELO_ISSN = [
    ('print', 'print'),
    ('electronic', 'electronic'),
]

SUBJECTS = [
    ('Agricultural Sciences', 'Agricultural Sciences'),
    ('Applied Social Sciences', 'Applied Social Sciences'),
    ('Biological Sciences', 'Biological Sciences'),
    ('Engineering', 'Engineering'),
    ('Exact and Earth Sciences', 'Exact and Earth Sciences'),
    ('Health Sciences', 'Health Sciences'),
    ('Humanities', 'Humanities'),
    ('Linguistics, Letters and Arts', 'Linguistics, Letters and Arts'),
]

PUBLICATION_STATUS = [
    ('C', 'Current'),
    ('D', 'Ceased'),
    ('R', 'Reports Only'),
    ('S', 'Suspended'),
    ('?', 'Unknow'),
]

LANGUAGE = [
    ('pt', 'português'),
    ('en', 'inglês'),
    ('es', 'espanhol'),
]

FREQUENCY = [
    ('M', 'Monthly'),
    ('B', 'Bimonthly (every two months)'),
    ('Q', 'Quaterly'),
    ('T', 'Three times a year'),
    ('F', 'Semiannual (twice a year)'),
    ('A', 'Annual'),
    ('K', 'Irregular (know to be so)'),
]

STANDARD = [
    ('iso690', 'iso 690/87 - international standard'),
    ('nbr6023', 'nbr 6023/89 - associação nacional'),
    ('other', 'other standard'),
    ('vancouv', 'the vancouver group - uniform'),
    ('apa', 'American Psychological Association')
]

CTRL_VOCABULARY = [
    ('decs', 'Health Sciences Descriptors'),
    ('nd', 'No Descriptor'),
]

PUBLICATION_LEVEL = [
    ('DI', 'Divulgation'),
    ('CT', 'Scientific Technical'),
]

PDF_DOWNLOAD = [
    ('art', 'article based - a PDF file for each article'),
    ('iss', 'issue based - a PDF file for each issue'),
    ('na', 'Not Available'),
]
TITLE_CATEGORY = [
    ('paralleltitle', 'Parallel Title'),
    ('other', 'Other'),
]

JOURNAL_PUBLICATION_STATUS = [
    ('current', 'Current'),
    ('deceased', 'Deceased'),
    ('suspended', 'Suspended'),
    ('inprogress', 'In Progress'),
]

# the index 0 has an empty value
MONTHS = [(i, month) for i, month in enumerate(calendar.month_name) if i > 0]

AUTHOR_ROLES = [
    ('nd', 'Not defined'),
    ('coord', 'coordinator'),
    ('ed', 'Publisher'),
    ('org', 'Organizer'),
    ('tr', 'Translator'),
]

LITERATURE_TYPE = [
    ('C','Conference'),
    ('M','Monograph'),
    ('MC','Conference papers and monograph'),
    ('MCP','Project and conference papers as monograph'),
    ('MP','Project papers and monograph'),
    ('MS','Monograph series'),
    ('MSC','Conference papers as monograph series'),
    ('MSP','Project paperas as monograph series'),
    ('N','Document in a non convetional form'),
    ('NC','Conference papers in a non conventional form'),
    ('P','Project'),
    ('S','Serial'),
    ('SC','Project papers as periodical series'),
    ('SCP','Conference and project papers as periodical series'),
    ('SP','Project papers as periodical series'),
    ('T','Thesis and dissertation'),
    ('TS','Thesis series'),

]