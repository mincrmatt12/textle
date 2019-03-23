import click 

def bool_adapter(x):
    return True if x == "true" else False

def interpret_extra_options(extra_options):
    glob_opts = {}

    intern_opts = {}

    if len(extra_options) % 2 == 1:
        click.echo("Invalid number of extra options passed to new.", stderr=True)
        click.abort()

    for opt, value in zip(extra_options[::2], extra_options[1::2]):
        if not opt.startswith("--") or ":" not in opt:
            click.echo("All extra options passed to new must be of the form --subsystem:value <some_value>", stderr=True)
            click.abort()

        subsystem, value, type_ = opt.split(":") if opt.count(":") == 2 else (opt.split(":"), None)

        if type_ == None:
            if value in ("true", "false"):
                type_ = bool_adapter
            elif all(x in "0123456789" for x in value):
                type_ = int
            else:
                type_ = str
        else:
            if type_ not in ("bool", "int", "str"):
                click.echo("Invalid argument type {}".format(type_))
            else:
                type_ = {
                    "bool": bool_adapter,
                    "int": int,
                    "str": str
                }

        value = type_(value)
        d = glob_opts if subsystem == "global" else intern_opts.get(subsystem, None)
        if not d:
            intern_opts[subsystem] = {}
            d = intern_opts[subsystem]

        if opt in d and type(d[opt]) is (type_ if type_ is not bool_adapter else bool):
            d[opt] = [d[opt], value]
        elif opt in d and type(d[opt]) is list:
            d[opt].append(value)
        else:
            d[opt] = value

    return glob_opts, intern_opts
