# pylint: disable=missing-docstring,import-error
import functools

from weechat import hook_command, prnt, WEECHAT_RC_OK, WEECHAT_RC_ERROR


# pylint: disable=too-many-arguments
def hook_command_partial(func, cmdname, desc, args, args_desc, compl):
    hook_command(cmdname, desc, args, args_desc, compl, func.__name__, "")

    @functools.wraps(func)
    def handle(*args, **kwargs):
        try:
            if func(*args, **kwargs):
                return WEECHAT_RC_OK
            return WEECHAT_RC_ERROR
        except Exception as e:  # pylint: disable=broad-except,invalid-name
            prnt("", "%s: %r" % (cmdname, e))
            return WEECHAT_RC_ERROR

    return handle


def command(cmdname, desc, args, args_desc, compl):
    hook_args = {"cmdname": cmdname, "desc": desc, "args": args,
                 "args_desc": args_desc, "compl": compl}
    return functools.partial(hook_command_partial, **hook_args)
