Flag Bearer
===========
A small utility to help with planting IScorE flags.

Installation
------------
The recommending way to install flag bearer is through pip:

    pip install flag-bearer

You may optionally install from source by cloning the repository and running

    python setup.py install

Usage
-----
The main purpose of flag bearer is to make planting blue and red flags easier.
To plant flag, start by running the following command:

    flag-bearer plant

You will then be asked for your API token, you can either paste in your API
token or press enter to use your credentials instead.

    Flag Bearer v0.1
    Enter your IScorE API Token (leave blank to use your credentials)
    > 

If you are on red team, you will be prompted for which team you are trying to
plant a flag for.

Both Red and Blue teamers will be presented with a list of flags available to
place.

    Pick the flag to place
    0. WWW /etc/
    1. Shell /etc/
    2. DB /etc/
    > 1

Enter the number next to the flag you want to plant.

At this point, if you are a Blue Teamer, or you have passed the `--save` flag,
you will be asked what directory you wish to place the flag. **NOTE**: The
current user must have permission to write to the specified directory. For Red
Teamers, the default functionality is to print out the contents of the flag to
make it easier to copy and paste.

### Download All Flags
You can also download all flags for your team (Red Team: any team) using the
following command:

    flag-bearer download

This will create a zip file in your current directory containing the flags, the
same as if you had downloaded them directly from IScorE.

### Remote
You can remotely plant flags using the `remote` subcommand. You will need to
install the remote extras: `pip install flag-bearer[remote]`. You can then plant
a flag with the following command:

    flag-beareer remote plant -H www.team11.isucdc.com -u root -P cdc -l /root/

After running this command you will be prompted just like a local plant. The
command will attempt to verify that the flag has been planted by reading the flag
and comparing the actual flag data.