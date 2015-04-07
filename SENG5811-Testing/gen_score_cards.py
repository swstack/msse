#!/usr/bin/env python
import random
import os
import shlex
import subprocess
import time
import shutil

THIS_DIR = os.path.dirname(__file__)
INPUT_FILE_DIR = os.path.join(THIS_DIR, 'input_files')
OUTPUT_FILE_DIR = os.path.join(THIS_DIR, 'output_files')
GOLFER_REPORT = os.path.join(os.getcwd(), 'golfer.rep')
COURSE_REPORT = os.path.join(os.getcwd(), 'course.rep')
TOURNAMENT_REPORT = os.path.join(os.getcwd(), 'trank.rep')
GOLFSCORE_BIN = os.path.join(THIS_DIR, 'golf_win32')


PROG_INPUT = {
    'courses': {
        'A': {
            'name': 'Course A',
            'holes': 18,
        },
        'B': {
            'name': 'Course B',
            'holes': 18,
        }
    },

    'rounds': [
        {
            'golfer_name': 'Bob',
            'course_played': 'A',
        },
        {
            'golfer_name': 'Jim',
            'course_played': 'A',
        },
        {
            'golfer_name': 'Bob',
            'course_played': 'B',
        },
        {
            'golfer_name': 'Jim',
            'course_played': 'B',
        }
    ]
}

TEMPLATE_COURSE = " {course_name}          {course_id}{pars}\n"
TEMPLATE_ROUND = " {course_id}       {golfer_name}                  {scores}\n"


def _gen_par_value():
    return random.randint(3, 5)


def _gen_score_value():
    return random.randint(1, 9)


def _clean_reports():
    if os.path.exists(GOLFER_REPORT):
        print "Cleaning golfer report..."
        os.remove(GOLFER_REPORT)

    if os.path.exists(COURSE_REPORT):
        print "Cleaning course report..."
        os.remove(COURSE_REPORT)

    if os.path.exists(TOURNAMENT_REPORT):
        print "Cleaning tournament report..."
        os.remove(TOURNAMENT_REPORT)


def _gen_input_files(number):
    if not os.path.exists(INPUT_FILE_DIR):
        os.makedirs(INPUT_FILE_DIR)

    for no in xrange(number):
        input_filename = os.path.join(INPUT_FILE_DIR, "in_golf_scores_{}.txt".format(no))
        with open(input_filename, 'w') as f:

            # write courses
            for cid, cinfo in PROG_INPUT['courses'].items():
                num_holes = cinfo['holes']
                pars = ("{}" * num_holes).format(*[_gen_par_value() for _ in xrange(num_holes)])
                f.write(TEMPLATE_COURSE.format(course_name=cinfo['name'],
                                               course_id=cid,
                                               pars=pars))

            # write delimiter
            f.write('_\n')

            # write rounds
            for r in PROG_INPUT['rounds']:
                num_holes = PROG_INPUT['courses'][r['course_played']]['holes']
                scores = ("{}" * num_holes).format(*[_gen_score_value() for _ in xrange(num_holes)])
                f.write(TEMPLATE_ROUND.format(course_id=r['course_played'],
                                              golfer_name=r['golfer_name'],
                                              scores=scores))

            # write delimeter
            f.write('_\n')


def _gen_output_files():
    root, dirs, files = os.walk(INPUT_FILE_DIR).next()
    for i, input_file in enumerate(files):
        input_file_path = os.path.join(root, input_file)
        command = "{} {} {}".format(GOLFSCORE_BIN, '-g', os.path.abspath(input_file_path))
        print "Running golf score against {}...".format(input_file)
        subprocess.check_output(shlex.split(command))
        output_file_path = os.path.join(OUTPUT_FILE_DIR, 'golf_report_{}.txt'.format(i))
        os.rename(GOLFER_REPORT, output_file_path)
        print "Generated {}...".format(output_file_path)
        _clean_reports()


def _verify_requirements():
    pass  # TODO: implement me


def main():
    _clean_reports()
    _gen_input_files(10)
    _gen_output_files()
    _verify_requirements()


if __name__ == "__main__":
    main()
