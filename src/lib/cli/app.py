import os
import sys
import click

CONTEXT_SETTINGS = dict(auto_envvar_prefix="MN")


class Environment:
    def __init__(self):
        self.verbose = False
        self.project_path = os.getcwd()

    def log(self, msg, *args):
        """Logs a message to stderr."""
        if args:
            msg %= args
        click.echo(msg, file=sys.stderr)

    def vlog(self, msg, *args):
        """Logs a message to stderr only if verbose is enabled."""
        if self.verbose:
            self.log(msg, *args)


pass_environment = click.make_pass_decorator(Environment, ensure=True)
cmd_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "commands"))


class AsCli(click.MultiCommand):
    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(cmd_folder):
            filename = filename.lower()
            if filename.endswith('.py') and filename.startswith('cmd_'):
                rv.append(filename[4:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name: str):
        import importlib
        name = name.lower()
        try:
            mod = importlib.import_module(f'lib.cli.commands.cmd_{name}')
        except ImportError:
            return
        return mod.cli


@click.command(cls=AsCli, context_settings=CONTEXT_SETTINGS)
@click.version_option()
@click.option(
    '-p',
    '--project-path',
    type=click.Path(exists=True, file_okay=False, resolve_path=True),
    help="Changes the project's root path.",
)
@click.option("-v", "--verbose", is_flag=True, help="Increases verbosity of the application.")
@pass_environment
def cli(ctx, verbose, project_path):
    """A CLI to manage the Docker image's build process."""
    ctx.verbose = verbose
    if project_path is not None:
        ctx.project_path = project_path
