import argparse

def navigate():
    parser = argparse.ArgumentParser(description="NaviCode command line tool")
    parser.add_argument("--init", action="store_true", default=False, help="Initialize navicode in your repository")
    parser.add_argument("--query", action="store_true", default=False, help="Query in initialized navicode repository")
    args = parser.parse_args()

    if args.init:
        print("Initializing navicode . . .")
        from navicode.drivers.cli.cli import navicode_init
        navicode_init()
    
    if args.query:
        print("Loading navicode lookup . . .")
        from navicode.drivers.cli.cli import navicode_query
        navicode_query()
