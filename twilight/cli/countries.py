import sys
import argparse
from twilight.lib import shapes, geo
from twilight.lib import tweets

import logging
logger = logging.getLogger(__name__)


def main(parser):
    '''
    Add country match to TTV2 data on STDIN.
    Output format: [...TTV2...]<TAB>country_iso3_code
    '''
    parser.add_argument('input', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('output', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('--map', help='ESRI Shapefile filepath',
        default='/data/chbrown/TM_WORLD_BORDERS-0.3/TM_WORLD_BORDERS-0.3.shp')
    opts = parser.parse_args()

    countries = map(geo.NamedArea.from_tm_world_borders, shapes.read_shapefile(opts.map))

    def countries_containing(lon, lat):
        # should reorder countries into the most popular first so that we find them quicker
        for country in countries:
            if country.contains(lon, lat):
                yield country

    def first_country_containing(lon, lat):
        for country in countries_containing(lon, lat):
            return country

    if opts.input.isatty():
        raise IOError('You must pipe in uncompressed TTV2-formatted tweets')

    for i, line in enumerate(opts.input):
        line = line.decode('utf8').strip()
        tweet = tweets.TTV2(*line.split(u'\t'))

        if tweet.coordinates != '':
            lon, lat = map(float, tweet.coordinates.split(','))
            country_match = first_country_containing(lon, lat)
            if country_match:
                extended_line = unicode(tweet) + u'\t' + unicode(country_match.ISO3)
                print >> opts.output, extended_line.encode('utf8')
                # melt out each hashtag into its own line
                # for hashtag in re.findall(r'#\S+', tweet.text):
                #     timestamp = tweet.created_at  # [:8]
                #     print '\t'.join((timestamp, country_match.ISO3, hashtag))
        else:
            logger.debug('No coordinates: %s', tweet.id)
