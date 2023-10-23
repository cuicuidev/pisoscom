import argparse
from scraping import scrape

def cli():
    parser = argparse.ArgumentParser(description = 'Custom CLI training util commands.')

    subparsers = parser.add_subparsers(dest = 'command')

    train_command = subparsers.add_parser(
        name = 'train',
        help = 'Trains the current model.'
        )
    
    train_command.add_argument(
        '-e',
        '--epochs',
        type = int,
        help = 'Number of epochs to train the model. 10 if not specified.'
        )
    
    train_command.add_argument(
        '-s',
        '--save-interval',
        type = int,
        help = "How often the model is saved along with it's history. None if not specified."
    )


    reset_command = subparsers.add_parser(
        name = 'reset',
        help = 'Resets the current history.'
    )

    args = parser.parse_args()

    if args.command == 'train':
        train.run(args.epochs, args.save_interval)
    
    if args.command == 'reset':
        reset.run()

if __name__ == '__main__':
    cli()