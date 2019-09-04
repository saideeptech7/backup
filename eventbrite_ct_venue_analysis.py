import csv

data = dict()

file = csv.DictReader(open('eventbrite_ct.csv', 'r', encoding='mac_roman'))

for row in file:
    if (row['Venue'].strip(), row['Location'].strip()) not in data:
        data[(row['Venue'].strip(), row['Location'].strip())] = {
            'organizers': dict(),
            'count': 0
        }

    data[(row['Venue'].strip(), row['Location'].strip())]['count'] += 1

    if (row['Organizer Name'].strip(), row['Organizer ID'].strip()) not in \
            data[(row['Venue'].strip(), row['Location'].strip())]['organizers']:
        data[(row['Venue'].strip(), row['Location'].strip())]['organizers'][(row['Organizer Name'].strip(),
                                                                             row['Organizer ID'].strip())] = {
            'url': row['Organizer Page'],
            'count': 0
        }

    data[(row['Venue'].strip(), row['Location'].strip())]['organizers'][
        (row['Organizer Name'].strip(), row['Organizer ID'].strip())]['count'] += 1


output = []

for each in data:
    if not each[0] or not each[1]:
        continue
    sorted_org = list(
        reversed(
            sorted(
                list(data[each]['organizers'].items()),
                key=lambda x: x[1]['count']
            )
        )
    )

    output.append({
        'Venue': each[0],
        'Location': each[1],
        'Total Events': data[each]['count'],
        'Top Organizer': sorted_org[0][0][0],
        'Top Organizer URL': sorted_org[0][1]['url'],
        'Top Organizer Events': sorted_org[0][1]['count']
    })

sorted_output = list(reversed(sorted(output, key=lambda x: x['Top Organizer Events'])))

with open('eventbrite_ct_venue_analysis.csv', 'w') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=['Venue', 'Location', 'Total Events', 'Top Organizer', 'Top Organizer URL',
                                                 'Top Organizer Events'], lineterminator='\n', delimiter=',')
    writer.writeheader()
    writer.writerows(sorted_output)
