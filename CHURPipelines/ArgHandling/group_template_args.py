#!/usr/bin/env python
"""Add arguments for the group template building subcommand."""

import argparse

from CHURPipelines.FileOps import default_dirs
from CHURPipelines.FileOps import default_files


def add_args(ap):
    """Takes an ArgumentParser object, and adds arguments to it. These args
    will be for the group template building subcommand. The function returns
    NoneType; we only call it for the side-effect of adding arguments to the
    parser object."""
    # Try to define a nested subparser. This will get wild
    ap_sub = ap.add_subparsers(
        dest='pipe_group',
        title='Pipelines',
        help='Available pipelines')

    # This is a parser for the bulk RNAseq options.
    brnaseq_def_xlsx = default_dirs.default_output('bulk_rnaseq') / \
        default_files.default_group_xlsx('bulk_rnaseq')
    brnaseq_group = ap_sub.add_parser(
        'bulk_rnaseq',
        help='Generate template groups file for bulk RNAseq analysis.',
        add_help=False)
    brnaseq_group_req = brnaseq_group.add_argument_group(
        title='Required arguments')
    brnaseq_group_req.add_argument(
        '--fq-folder',
        '-f',
        metavar='<fastq folder>',
        dest='fq_folder',
        help='Directory that contains the FASTQ files.',
        required=True)
    brnaseq_group_opt = brnaseq_group.add_argument_group(
        title='Optional arguments')
    brnaseq_group_opt.add_argument(
        '--help',
        '-h',
        help='Show this help message and exit.',
        action='help')
    brnaseq_group_opt.add_argument(
        '--verbosity',
        '-v',
        metavar='<loglevel>',
        dest='verbosity',
        help=('How much logging output to show. '
              'Choose one of "debug," "info," or "warn."'),
        choices=['debug', 'info', 'warn'],
        default='warn')
    brnaseq_group_opt.add_argument(
        '--output',
        '-o',
        metavar='<output file>',
        dest='outfile',
        help='Name of output file. If a file type extension is included (e.g. csv or xlsx) that extension will be respected. An xlsx file is required for producing differential expression testing results with the CHURP bulk_rnaseq command, because the xlsx has a second sheet for DE testing comparisons. A csv file can be used with CHURP bulk_rnaseq to allow for group labels, but the csv cannot be used to get basic DE testing results. The default for this argument if no file name is provided will be the following xlsx file: ' + str(brnaseq_def_xlsx),
        default=brnaseq_def_xlsx)
    brnaseq_group_opt.add_argument(
        '--command-log',
        dest='cmd_log',
        help=('Save the command that was run into this file. This file will be'
              ' appended to, rather than overwritten, so you can save multiple'
              ' CHURP runs into this file.'),
        default=None)
    return
