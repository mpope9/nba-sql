"""
------------------------------------------------------------------------------
Copyright 2023 Matthew Pope

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
------------------------------------------------------------------------------


This is a wrapper, to allow building the cmdline executable without
having to include the full GUI libs.
"""

from nba_sql import main
from args import create_parser

from gooey import Gooey
from gooey import GooeyParser

from utils import generate_valid_seasons

import codecs
import sys


# This fixes an issue with Gooey and PyInstaller.
if sys.stdout.encoding != 'UTF-8':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
if sys.stderr.encoding != 'UTF-8':
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


# This 'fixes' an issue with printing in the Gooey console, kinda sorta not really.
class Unbuffered(object):

    def __init__(self, stream):
        self.stream = stream

    def write(self, data):
        self.stream.write(data)
        self.stream.flush()

    def writelines(self, datas):
        self.stream.writelines(datas)
        self.stream.flush()

    def __getattr__(self, attr):
        return getattr(self.stream, attr)


sys.stdout = Unbuffered(sys.stdout)


# Bad practice? Yes. Any other alternative? Not at this point.
# Only enable Gooey if there are no arguments passed to the script.
if len(sys.argv) >= 2:
    if '--ignore-gooey' not in sys.argv:
        sys.argv.append('--ignore-gooey')


@Gooey(
    program_name='nba-sql',
    program_description='An application to build a database of NBA data.',
    header_show_title=True)
def gui_main():
    parser = GooeyParser(description="nba-sql")
    create_parser(parser)

    # Add the 'mode args' that the regular python arg parse doesn't support.
    mode_parser = parser.add_mutually_exclusive_group(
        required=True,
        gooey_options={
            'initial_selection': 0
        })
    mode_parser.add_argument(
        '--default_mode',
        help='''
            Mode to create the database and load historic data.
            Use this mode when creating a new database or when
            trying to load a specific season or a range of seasons.
        ''',
        action='store_true')
    mode_parser.add_argument(
        '--current_season_mode',
        help='''
            Mode to refresh the current season. Use this mode on an
            existing database to update it with the latest data.
        ''',
        action='store_true')

    parser.add_argument(
        '--password',
        help="Database Password (Not Needed For SQLite)",
        widget='PasswordField',
        default=None)

    valid_seasons = generate_valid_seasons()
    last_loadable_season = valid_seasons[-1]

    parser.add_argument(
        '--seasons',
        dest='seasons',
        default=[last_loadable_season],
        choices=valid_seasons,
        widget='Listbox',
        nargs="*",
        help='''
            The seasons flag loads the database with the specified season.
            The format of the season should be in the form "YYYY-YY".
            The default behavior is loading the current season.
        ''')

    parser.add_argument(
        '--skip-tables',
        action='store',
        nargs="*",
        default='',
        choices=[
            'player_season',
            'player_game_log',
            'play_by_play',
            'pgtt',
            'shot_chart_detail',
            'game',
            'event_message_type',
            'team',
            'player',
            ''
        ],
        widget='Listbox',
        help='Use this option to skip loading certain tables.')

    args = parser.parse_args()

    main(args, True)


if __name__ == "__main__":
    gui_main()
