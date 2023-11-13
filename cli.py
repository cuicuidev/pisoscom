import argparse
from scraping import scrape, check

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
    
    train_command.add_argument(
        '-p',
        action = 'store_true',
        help = 'Marca el enlace como `/venta/pisos-`'
    )
    
    check_command = subparsers.add_parser(
        name = 'check',
        help = 'Comprueba qué endpoints faltan por scrapear'
    )

    args = parser.parse_args()

    if args.command == 'scrape':
        scrape.run(args.endpoint, args.p)

    if args.command == 'check':
        check.run(args)

if __name__ == '__main__':
    cli()