import click
from .dataset import check_labels
from .resize_image_and_polygon import check_size
from ..visualize.visualizer import visualize_coco


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    pass


@click.command(help='Check labels and resize image and mask')
@click.option('--labels', is_flag=True)
@click.option('--size', is_flag=True)
def check(labels, size):
    if labels:
        check_labels()

    if size:
        check_size()

@click.command(help='Visualizer')
@click.argument('image_dir', required=True, type=str)
@click.argument('info_path', required=True, type=str)
@click.option('--num_images', default=6, type=int, help='Number of images')
def visualize(image_dir, info_path, num_images):
    visualize_coco(image_dir, info_path, num_images)


def main():
    cli.add_command(check)
    cli.add_command(visualize)
    cli()


if __name__ == '__main__':
    main()

# @click.option('--name', prompt='Your name')
# @click.command()
# @click.option('--check_labels', is_flag=True)
# @click.option('-v', '--version', is_flag=True)
# def main(name, version, check_labels):
#     if version:
#         click.echo('0.0.1')
#         sys.exit()