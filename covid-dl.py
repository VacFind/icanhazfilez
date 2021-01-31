import argparse, logging, requests, sys
# import sqlalchemy as db
from util.db import session, Source, RawData

# parser.add_argument("-v", "--verbose", action='store_true', help='output more information')
# parser.add_argument("-n", "--dry-run", action='store_true', help='run the program without actually making any web requests')


logger = logging.getLogger(__name__)

# https://chase-seibert.github.io/blog/2014/03/21/python-multilevel-argparse.html
class CovidDL(object):

	def __init__(self):
		parser = argparse.ArgumentParser(
			description='Tool for downloading COVID-related Data Dumps',
			usage='''covid-dl <command> [<args>]

The available commands are:
   new        Add a new data source to the database
   fetch      Check and scrape all existing data sources
''')
		parser.add_argument('command', help='Subcommand to run')
		# parse_args defaults to [1:] for args, but you need to
		# exclude the rest of the args too, or validation will fail
		args = parser.parse_args(sys.argv[1:2])
		if not hasattr(self, args.command):
			print("Unrecognized command")
			parser.print_help()
			exit(1)
		# use dispatch pattern to invoke method with same name
		getattr(self, args.command)()

	def new(self):
		parser = argparse.ArgumentParser(
			description='Add a new data source to the database')
		# NOT prefixing the argument with -- means it's not optional
		parser.add_argument('url', help="a consistent url to add to the list of sources")
		parser.add_argument('--selector', help="the selector on the page to look for if the page contains a link that changes frequently", default=None, type=str)
		parser.add_argument('--description', help="a description for this data source to help identiify what data it provides .etc", default=None, type=str)
		# now that we're inside a subcommand, ignore the first
		# TWO argvs, ie the command and the subcommand
		args = parser.parse_args(sys.argv[2:])

		new_source = Source(source_url=args.url, page_selector=args.selector, is_active=True, description=args.description)
		session.add(new_source)
		session.commit()

		print("Record Added Successfully.")

	def fetch(self):
		parser = argparse.ArgumentParser(
			description='Check and scrape all existing data sources')
		# prefixing the argument with -- means it's optional
		parser.add_argument('--dry-run', '-n', action='store_true')
		parser.add_argument('--verbose', '-v', action='store_true')
		args = parser.parse_args(sys.argv[2:])

def should_download_source(source, current_datetime):
	# Dates increase as time advances, thus, a descending ordering puts the most recent dates first.
	last_record = session.query(RawData).filter(RawData.source_id == source.id).order_by(RawData.date_created.desc()).first()

	#if source is disabled, dont download it
	if source.update_frequency == 0:
		return False

	# if this source hasnt been downloaded yet, download it
	if last_record == None:
		return True

	#if we are still within the update_frequency window, skip this update
	update_window = datetime.timedelta(minutes=source.update_frequency)
	if source.last_checked + update_window > current_datetime:
		return False

	#check if source has changed since last download
	# headers available:
	# last-modified: Fri, 29 Jan 2021 17:08:40 GMT
	# content-length: 17101
		
def get_source_file_info(source):
	# HEAD request the file and look at content-disposition


def get_source_file(source):
	raise NotImplementedError()

if __name__ == '__main__':
    CovidDL()