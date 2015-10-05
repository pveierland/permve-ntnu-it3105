#!/usr/bin/python

from bs4 import BeautifulSoup
import sys

soup = BeautifulSoup(sys.stdin.read(), 'html.parser')

rows = []

for row in soup.find('table', {'id': 'cross_left'}).find_all('tr'):
    rows.append([ int(cell.get_text()) for cell in row.find_all('td') if cell.get_text().strip() ])

rows = list(reversed(rows))

columns = []

for row in soup.find('table', {'id': 'cross_top'}).find_all('tr'):
    columns.append([ (int(cell.get_text()) if cell.get_text().strip() else 0) for cell in row.find_all('td') ])

columns = zip(*columns)
columns = [[element for element in column if element] for column in columns]

print('{0} {1}'.format(len(columns), len(rows)))

for row in rows:
    print(' '.join(map(str, row)))

for column in columns:
    print(' '.join(map(str, column)))
