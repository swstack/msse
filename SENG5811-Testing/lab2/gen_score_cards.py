#!/usr/bin/env python
import random
import os
import shlex
import subprocess
import re

THIS_DIR = os.path.dirname(__file__)
INPUT_FILE_DIR = os.path.join(THIS_DIR, 'input_files')
OUTPUT_FILE_DIR = os.path.join(THIS_DIR, 'output_files')
GOLFER_REPORT = os.path.join(os.getcwd(), 'golfer.rep')
COURSE_REPORT = os.path.join(os.getcwd(), 'course.rep')
TOURNAMENT_REPORT = os.path.join(os.getcwd(), 'trank.rep')
GOLFSCORE_BIN = os.path.join(THIS_DIR, 'golf_win32')

TEMPLATE_COURSE = " {course_name}          {course_id}{pars}\n"
TEMPLATE_ROUND = " {course_id}       {golfer_name}                  {scores}\n"

REGEX_GOLFER = "(\w+)\s+Rank:\s+(\w+)"
REGEX_ROUND = "\s+Course ID: (\w+)\s+Raw score: (\w+)\s+Ranking score: (\w+)\s+"

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

SCORING_TABLE = {
    1:  0,          # overpar
    0:  1,          # par
    -1: 2,          # 1 under par
    -2: 4,          # 2 under par
    -3: 6,          # 3 under par
}


expected_scores = {}
input_output_file_map = {}


def _gen_par_value():
    return random.randint(3, 5)  # Inclusive


def _gen_score_value():
    return random.randint(1, 9)  # Inclusive


def _clean_reports():
    if os.path.exists(GOLFER_REPORT):
        print("Cleaning golfer report...")
        os.remove(GOLFER_REPORT)

    if os.path.exists(COURSE_REPORT):
        print("Cleaning course report...")
        os.remove(COURSE_REPORT)

    if os.path.exists(TOURNAMENT_REPORT):
        print("Cleaning tournament report...")
        os.remove(TOURNAMENT_REPORT)


def _gen_input_files(number):
    if not os.path.exists(INPUT_FILE_DIR):
        os.makedirs(INPUT_FILE_DIR)

    in_memory_course_data = {}

    for no in range(number):
        input_file = "in_golf_scores_{}.txt".format(no)
        input_file_path = os.path.join(INPUT_FILE_DIR, input_file)
        with open(input_file_path, 'w') as f:

            # write courses
            for cid, cinfo in PROG_INPUT['courses'].items():
                num_holes = cinfo['holes']
                pars = ("{}" * num_holes).format(*[_gen_par_value() for _ in range(num_holes)])
                f.write(TEMPLATE_COURSE.format(course_name=cinfo['name'],
                                               course_id=cid,
                                               pars=pars))
                in_memory_course_data[cid] = pars

            # write delimiter
            f.write('_\n')

            # write rounds
            for r in PROG_INPUT['rounds']:
                num_holes = PROG_INPUT['courses'][r['course_played']]['holes']
                scores = ("{}" * num_holes).format(*[_gen_score_value() for _ in range(num_holes)])
                f.write(TEMPLATE_ROUND.format(course_id=r['course_played'],
                                              golfer_name=r['golfer_name'],
                                              scores=scores))

                expected_raw_score = 0
                expected_rank_score = 0
                for i, score in enumerate(scores):
                    score = int(score)
                    par = int(list(in_memory_course_data[r['course_played']])[i])
                    expected_raw_score += score
                    diff = score - par
                    rank_score = SCORING_TABLE.get(diff, None)
                    if rank_score is not None:
                        expected_rank_score += rank_score
                    else:
                        if diff > 1:
                            expected_rank_score += 0
                        elif diff < -3:
                            expected_rank_score += 6
                        else:
                            raise Exception("Score == %s, Par == %s" % (score, par))

                expected_scores.setdefault(input_file, {}).setdefault(r['golfer_name'], {}).setdefault(r['course_played'])
                expected_scores[input_file][r['golfer_name']][r['course_played']] = {
                    'expected_raw_score': expected_raw_score,
                    'expected_rank_score': expected_rank_score,
                }

            # write delimeter
            f.write('_\n')


def _gen_output_files():
    if not os.path.exists(OUTPUT_FILE_DIR):
        os.makedirs(OUTPUT_FILE_DIR)

    root, dirs, files = next(os.walk(INPUT_FILE_DIR))
    for i, input_file in enumerate(files):
        input_file_path = os.path.join(root, input_file)
        command = "{} {} {}".format(GOLFSCORE_BIN, '-g', os.path.abspath(input_file_path))
        subprocess.check_output(shlex.split(command))
        output_file = 'golf_report_{}.txt'.format(i)
        output_file_path = os.path.join(OUTPUT_FILE_DIR, output_file)
        os.rename(GOLFER_REPORT, output_file_path)
        input_output_file_map[output_file] = input_file
        _clean_reports()


def _verify_requirements():
    root, dirs, files = next(os.walk(OUTPUT_FILE_DIR))
    for golfer_report in files:
        print('-------------------------------------------------------')
        golfer_report_file = os.path.split(golfer_report)[-1]
        input_file = input_output_file_map[golfer_report_file]
        print("Verifying {} against {}".format(golfer_report_file, input_file))
        golfer_report = os.path.join(root, golfer_report)
        with open(golfer_report, 'r') as f:
            raw_report_lines = f.readlines()
        raw_report_lines = raw_report_lines[1:]  # Trim off "Golfer Report" first line

        for line in raw_report_lines:
            match_golfer = re.match(REGEX_GOLFER, line)
            if match_golfer:
                golfer_name = match_golfer.group(1)
                golfer_rank = match_golfer.group(2)

            match_round = re.match(REGEX_ROUND, line)
            if match_round:
                course_id = match_round.group(1)
                raw_score = match_round.group(2)
                rank_score = match_round.group(3)
                print("{golfer} played course {course} with score {rank_score}...".format(
                    golfer=golfer_name,
                    course=course_id,
                    rank_score=rank_score
                ))

                matching_round = expected_scores[input_file][golfer_name][course_id]
                if int(raw_score) != matching_round['expected_raw_score']:
                    print('  --Raw score of {} does not match {}'.format(
                        raw_score, matching_round['expected_raw_score']
                    ))
                if int(rank_score) != matching_round['expected_rank_score']:
                    print('  --Rank score of {} does not match {}'.format(
                        rank_score, matching_round['expected_rank_score']
                    ))


def main():
    _clean_reports()
    _gen_input_files(10)
    _gen_output_files()
    _verify_requirements()


if __name__ == "__main__":
    main()
