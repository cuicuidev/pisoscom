import argparse
from scraping import scrape

def cli():
    parser = argparse.ArgumentParser(description = 'Custom CLI training util commands.')

    subparsers = parser.add_subparsers(dest = 'command')

    train_command = subparsers.add_parser(
        name = 'scrape',
        help = 'Scrapea una web de pisos.com.'
        )
    
    train_command.add_argument(
        '-e',
        '--endpoint',
        type = str,
        help = 'endpoint.'
        )

    args = parser.parse_args()

    if args.command == 'scrape':
        scrape.run(args.endpoint)

if __name__ == '__main__':
    cli()