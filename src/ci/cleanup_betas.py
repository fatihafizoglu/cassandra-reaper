import requests
from requests.auth import HTTPBasicAuth
import argparse

USAGE = """
cleanup_betas.py [<command_args>]
"""

def _arguments(parser):
    """Arguments relevant for every CLI command"""
    
    parser.add_argument("--repository", default=None,
                       help="Bintray repository to cleanup (mandatory)")
    parser.add_argument("--latest-release", default=None,
                       help="Release version for which betas should be cleaned up (mandatory)")
    parser.add_argument("--bintray-user", default=None,
                       help="Bintray username (mandatory)")
    parser.add_argument("--bintray-api-key", default=None, help="Bintray API key (mandatory)")
    parser.add_argument("--noop", help="Performs a blank run that will only list"
                                        " the versions that would be deleted (optional)", action="store_true")

def _parse_arguments():
    parser = argparse.ArgumentParser(description="", usage=USAGE)
    _arguments(parser)
    args = parser.parse_args()
    if args.repository == None or args.latest_release == None or args.bintray_user == None or args.bintray_api_key == None:
        print "Missing parameters!"
        print parser.format_help()
        exit()
    return args

if __name__ == '__main__':
    args = _parse_arguments()
    print "calling " + 'https://api.bintray.com/packages/thelastpickle/{0}/cassandra-reaper-beta'.format(args.repository)
    res = requests.get('https://api.bintray.com/packages/thelastpickle/{0}/cassandra-reaper-beta'.format(args.repository), auth=HTTPBasicAuth(args.bintray_user, args.bintray_api_key))
    #print res.text
    print "Candidates for deletion in {0}:".format(args.repository)
    for version in res.json()['versions']:
        if version.startswith(args.latest_release):
            print version
    
    if not args.noop:
        for version in res.json()['versions']:
            if version.startswith(args.latest_release):
                print 'Deleting {0} {1}...'.format(args.repository, version)
                res = requests.delete('https://api.bintray.com/packages/thelastpickle/{0}/cassandra-reaper-beta/versions/{1}'.format(args.repository, version), auth=HTTPBasicAuth(args.bintray_user, args.bintray_api_key))
    
    print "All done"