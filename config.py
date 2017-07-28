_form = '10-K'
_count = '10'  # Amount of links to fetch. Only recent years are interesting.
_url = 'https://www.sec.gov'
_years = ['2017', '2016', '2015', '2014', '2013']
toc = ['item 1 business',
       'item 1a risk factors',
       'item 1b unresolved staff comments',
       'item 2 properties',
       'item 3 legal proceedings',
       'item 4 mine safety disclosures',
       'item 5 market for registrants common equity related stockholder matters and issuer purchases of equity securities',
       'item 6 selected financial data',
       'item 7 managements discussion and analysis of financial condition and results of operations',
       'item 7a quantitative and qualitative disclosures about market risk',
       'item 8 financial statements and supplementary data',
       'item 9 changes in and disagreements with accountants on accounting and financial disclosure',
       'item 9a controls and procedures',
       'item 9b other information',
       'item 10 directors executive officers and corporate governance',
       'item 11 executive compensation',
       'item 12 security ownership of certain beneficial owners and management and related stockholder matters',
       'item 13 certain relationships and related transactions and director independence',
       'item 14 principal accounting fees and services',
       'item 15 exhibits financial statement schedules'
       ]
toc_nospace = [
       'item 1business',
       'item 1arisk factors',
       'item 1bunresolved staff comments',
       'item 2properties',
       'item 3legal proceedings',
       'item 4mine safety disclosures',
       'item 5market for registrants common equity related stockholder matters and issuer purchases of equity securities',
       'item 6selected financial data',
       'item 7managements discussion and analysis of financial condition and results of operations',
       'item 7aquantitative and qualitative disclosures about market risk',
       'item 8financial statements and supplementary data',
       'item 9changes in and disagreements with accountants on accounting and financial disclosure',
       'item 9acontrols and procedures',
       'item 9bother information',
       'item 10directors executive officers and corporate governance',
       'item 11executive compensation',
       'item 12security ownership of certain beneficial owners and management and related stockholder matters',
       'item 13certain relationships and related transactions and director independence',
       'item 14principal accounting fees and services',
       'item 15exhibits financial statement schedules'
       ]
