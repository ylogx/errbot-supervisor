from errbot import BotPlugin, botcmd, arg_botcmd, webhook


ALLOWED_COMMANDS = [
    'status',
    'tail',
    'version',
    'avail',
    'maintail',
]


class Supervisor(BotPlugin):
    """
    Bot Plugin to control supervisord
    """

    # Passing split_args_with=None will cause arguments to be split on any kind
    # of whitespace, just like Python's split() does
    @botcmd(split_args_with=None)
    def supervisor(self, message, args):
        """A command which simply returns 'Example'"""
        output = 'Unable to process!'
        if len(args) < 1:
            return 'Not enough arguments. Try !supervisor help'

        scmd = args[0]
        if scmd in ALLOWED_COMMANDS:
            additional_params = ' '.join(args[1:]) if len(args) > 1 else ''

            output = run_cmd('sudo supervisorctl {cmd} {params}'.format(cmd=scmd, params=additional_params))
        return output


def run_cmd(cmd):
    import subprocess
    try:
        output = subprocess.check_output(
            cmd.split(),
            stderr=subprocess.STDOUT
        )
        if len(output) > 0:
            return output.decode()
        else:
            return "OK\n"
    except subprocess.CalledProcessError as err:
        if len(err.output):
            return err.output.decode()
        else:
            return "Error"

