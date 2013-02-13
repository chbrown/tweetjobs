#!/usr/bin/env python
import os
import re
import gzip
import bz2
import argparse
from twilight import stdout_tabs, stdoutn, stderrn
from twilight.ttv import TTV2


description = '''Convert json.gz files to ttv2.
    ttv2izer looks at /usr/local/data/twitter/*.json.gz files and sequentially ttv2'izes them.
    To check if it's behaving:
    cat yourfile.bz2 | awk 'BEGIN{FS="\\t"}{print NF}' # should only output 26's'''


def open_any(path):
    '''Open any Tweets raw json file, depending on its extension.'''
    if path.endswith('gz'):
        return gzip.GzipFile(path)
    elif path.endswith('bz2'):
        return bz2.BZ2File(path)
    else:
        return open(path)


def convert_json_to_ttv2(json_path, ttv2_path):
    # the given json_path can be either gzip'ed or bzip2'ed or not
    # the resulting file at ttv2_path will always be bzip2'ed
    with bz2.BZ2File(ttv2_path, 'w') as ttv2_fp:
        with open_any(json_path) as json_fp:
            for line in json_fp:
                line = line.decode('utf-8')
                try:
                    tweet = TTV2.from_json(line)
                    ttv2_fp.write(tweet.to_tsv().encode('utf-8'))
                    ttv2_fp.write('\n')
                except Exception, exc:
                    stderrn("Error translating json: %s (%s)" % (line.strip(), exc))


def main():
    parser = argparse.ArgumentParser(description=description,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--directory', default='/usr/local/data/twitter')
    parser.add_argument('--delete', action='store_true')
    parser.add_argument('--overwrite', action='store_true')
    opts = parser.parse_args()

    os.chdir(opts.directory)
    for filename in os.listdir('.'):
        # only do gz extensions for now, to ensure we don't try to pick up any live files.
        if re.search('.json(.gz)?$', filename):
            ttv2_filename = '%s.ttv2.bz2' % filename.split('.')[0]

            stdout_tabs(filename, '>', ttv2_filename)

            if not os.path.exists(ttv2_filename) or opts.overwrite:
                stdout_tabs('ttv2izing')
                convert_json_to_ttv2(filename, ttv2_filename)
            else:
                stdout_tabs('ttv2ized')

            fraction = os.stat(ttv2_filename).st_size / float(os.stat(filename).st_size)
            stdout_tabs('%0.2f%% as big' % (fraction * 100))

            if fraction > 0.5:
                stdout_tabs('too-big')
            elif fraction < 0.18:
                stdout_tabs('too-small')
            else:
                if opts.delete:
                    stdout_tabs('rm')
                    os.remove(filename)
                else:
                    stdout_tabs('deletable')
        else:
            stdout_tabs(filename, 'not json')

        stdoutn()


if __name__ == '__main__':
    main()
