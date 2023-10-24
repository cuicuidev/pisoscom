import argparse
from scraping import scrape, commit, reset

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

    commit_command = subparsers.add_parser(
        name = 'commit',
        help = 'Extrae contenido del html y guarda los datos en un csv'
    )

    commit_command.add_argument(
        '-f',
        '--filename',
        type = str,
        help = 'filename'
    )
    
    reset_command = subparsers.add_parser(
        name = 'reset',
        help = 'Resetea el entorno para scrapear'
    )

    args = parser.parse_args()

    if args.command == 'scrape':
        scrape.run(args.endpoint)
    if args.command == 'commit':
        commit.run(args.filename)
    if args.command == 'reset':
        reset.run()

if __name__ == '__main__':
    cli()