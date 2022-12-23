import click
from netmin.lib.cli.app import pass_environment


@click.command("run", short_help="Run the application in development mode.")
@click.option('-e', '--env-file', default='.env',
              help='The path to an .env file to load command settings from.')
@click.option('--env-file-encoding', default='UTF-8',
              help='The encoding of the env file specified by the "--env-file" option.')
@click.option('-s', '--secrets-dir', default=None,
              help='The path to a directory containing environment variable secret files.')
@pass_environment
def cli(ctx, env_file: str, env_file_encoding: str, secrets_dir: str | None):
    """Run the application in development mode."""
    import os
    from config import AppSettings

    if not env_file.startswith('/'):
        env_file = os.path.join(ctx.project_path, env_file)

    params: dict = {
        '_env_file': env_file,
        '_env_file_encoding': env_file_encoding,
    }

    os.putenv('MN_ENV_FILE', env_file)
    os.putenv('MN_ENV_FILE_ENCODING', env_file_encoding)

    if secrets_dir is not None:
        valid: bool = True
        secrets_path: str = secrets_dir if secrets_dir.startswith('/') else os.path.join(ctx.project_path, secrets_dir)

        if not os.path.exists(secrets_path):
            valid = False
            ctx.log(f'The given path for the "--secrets-dir" option does not exist: {secrets_path}')
        elif not os.path.isdir(secrets_path):
            valid = False
            ctx.log(f'The given path for the "--secrets-dir" option is not a directory: {secrets_path}')

        if valid:
            params['_secrets_dir'] = secrets_dir
            os.putenv('MN_ENV_SECRETS_DIR', secrets_dir)

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'netmin.settings')

    settings: AppSettings = AppSettings(**params)

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    execute_from_command_line(
        ['src/manage.py', 'runserver', f'{settings.dev_server_address}:{settings.dev_server_port}']
    )
