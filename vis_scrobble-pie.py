import dataset
from nvd3 import pieChart

# chart properties
size = 1000
stream_limit = 0.75
artist_limit = 50
chartname = 'scrobble-pie'
metric = 'artist_text'

# file properties
filename = chartname + '.html'

# gets all artists and their respective play counts in order of greatest count to least
db = dataset.connect('sqlite:///last-fm.db')
total = db['scrobbles'].count()
sql = 'SELECT {0}, count({0}) FROM scrobbles GROUP BY {0} ORDER BY count({0}) DESC'.format(metric)
result = db.query(sql)
artists = []
streams = []
for row in result:
	artists.append(row[metric])
	streams.append(int(row['count(%s)' % metric]))

# iterates through all artists and isolates the most significant (i.e. most listened to)
sig_artists = []
sig_streams = []
for artist, plays in zip(artists, streams):
	if sum(sig_streams) < total*stream_limit and len(sig_artists) < artist_limit:
		sig_artists.append(artist)
		sig_streams.append(plays)
sig_artists.append("Other")
sig_streams.append(total - sum(sig_streams))

# sets up the chart
chart = pieChart(name=chartname, color_category='category20c', height=size, width=size)
extra_serie = {"tooltip": {"y_start": "", "y_end": " scrobbles"}}
chart.add_serie(x=sig_artists, y=sig_streams, extra=extra_serie)
chart.buildhtml()

# generates the HTML file
output = open(filename, 'w')
output.write(chart.htmlcontent)
output.close()