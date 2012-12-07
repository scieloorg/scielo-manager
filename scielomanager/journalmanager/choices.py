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
    ('Human Sciences', 'Human Sciences'),
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
