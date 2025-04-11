#!/usr/bin/env python
"""Define a function that will parse the arguments. This will eventually be
a huge function, so we will isolate it into this script for ease of development
and maintenance."""

import argparse
import CHURPipelines
from CHURPipelines.ArgHandling import group_template_args
from CHURPipelines.ArgHandling import bulk_rnaseq_args
from CHURPipelines import DieGracefully


# Longer help messages as constants
PIPE_HELP = 'CHURP pipelines for high-throughput sequencing data analysis.'
BRNASEQ_HELP = ('Bulk RNAseq analysis, including QC, mapping, and expression. '
                'Alignment is performed with HISAT2. Read counts are '
                'generated with featureCounts from the Subread package. '
                'Expression anaylsis is done with edgeR in R.')
ALIAS_HELP = ('List species shorthands for automatically setting alignment '
             'targets and annotation databases.')
GROUP_HELP = ('Make sample metadata templates for statistical tests. '
              'Usage requires "group_template bulk_rnaseq" to create '
              'a template for bulk RNA-seq differential expression testing.')


def usage():
    """Print a usage message for the pipeline. This is invoked when there are
    no arguments supplied to the script."""
    msg = """Usage: churp.py <subcommand> <options>

where <subcommand> is the name of the pipeline that is to be run. The specified
<options> will be applied to the operations in the pipeline. Each pipeline has
its own set of options that must be specified. To see a full listing of each
available option for a given pipeline, pass the '--help' option.

Currently, the following subcommands are supported:
    - bulk_rnaseq
    - genome_aliases
    - group_template bulk_rnaseq

For issues, contact ribhelp@msi.umn.edu.
Version: {version}
{date}"""
    print(
        msg.format(
            version=CHURPipelines.__version__,
            date=CHURPipelines.__date__))
    return


def check_for_bad(a):
    """Check for bad characters in the args and throw an error if it detects
    any of them. These are characters that let users terminate the current
    command and start another, e.g., a file called 'sample_01; rm -rf ~'"""
    v = vars(a)
    bad_chars = [';', '#', '|', '$(', '<', '>', '`']
    for option in v:
        if not v[option]:
            continue
        else:
            for bc in bad_chars:
                if bc in str(v[option]):
                    DieGracefully.die_gracefully(
                        DieGracefully.NEFARIOUS_CHAR, str(v[option]))
    return


def pipeline_args():
    """Parse arguments for the pipeline as a whole. This will dispatch the
    arguments to other functions that parse pipeline-specific arguments. This
    is a bit crazy for now, but it should be pretty flexible for adding new
    pipelines and easier to maintain in the long run."""
    parser = argparse.ArgumentParser(
        description=PIPE_HELP,
        add_help=True)
    # Add a sub-parser for the subcommands. These will be the pipelines.
    pipe_parser = parser.add_subparsers(
        dest='pipeline',
        title='Available Subcommands',
        help='')
    # This is the bulk_rnaseq parser
    bulk_rnaseq_parser = pipe_parser.add_parser(
        'bulk_rnaseq',
        help=BRNASEQ_HELP,
        add_help=False)    
    # Species list parser
    # using add_help = True here to add a help message for genome_aliases
    alias_parser = pipe_parser.add_parser(
        'genome_aliases',
        help=ALIAS_HELP,
        add_help=True,
        epilog='genome_aliases has no required or optional arguments.\n\n')
    # Group template parser
    group_parser = pipe_parser.add_parser(
        'group_template',
        help=GROUP_HELP,
        add_help=False)

    group_template_args.add_args(group_parser)
    bulk_rnaseq_args.add_args(bulk_rnaseq_parser)
    # genome_aliases does not have any required or optional args,
    # so this is commented out and -h or --help won't work for it because there is nothing to help with
    # genome_aliases_args.add_args(alias_parser)
    pargs = parser.parse_args()
    check_for_bad(pargs)
    return vars(pargs)
