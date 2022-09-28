#!/usr/bin/env python

# MIT License
# Copyright (c) 2022 Matt Westfall (@disloops)

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

__author__ = 'Matt Westfall'
__version__ = '0.1'
__email__ = 'disloops@gmail.com'

import os
import re
import csv
import sys
import argparse

def parse_log(input_file):

    re_user = re.compile(r'\"USER .*\"\n')
    re_pass = re.compile(r'\", anon password .*\"\n')
    re_pid = re.compile(r'\[pid ([0-9]+)\]')
    re_ip = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')

    progress_list = []
    login_list = []

    with open(input_file, 'r') as file_object:
        print ' [+] Parsing input file...'
        line = file_object.readline()

        while line:
            if re_user.search(line):
                user = re.split(r'\"USER ', line, maxsplit=1)[1][:-2]
                if user in ['ftp','anonymous']:
                    pid = re_pid.search(line).group(1)
                    ip = re_ip.search(line).group(1)
                    login_dict = {
                        'pid': pid,
                        'ip': ip,
                        'user': user
                    }
                    progress_list.append(login_dict)
                else:
                    login_dict = {
                        'user': user,
                        'password': ''
                    }
                    login_list = add_dict(login_dict, login_list)
            elif re_pass.search(line):
                password = re.split(r'\", anon password \"', line, maxsplit=1)[1][:-2]
                pid = re_pid.search(line).group(1)
                ip = re_ip.search(line).group(1)
                for single_dict in progress_list:
                    if (int(pid)-1) <= int(single_dict['pid']) <= (int(pid)+1) and ip == single_dict['ip']:
                        login_dict = {
                            'user': single_dict['user'],
                            'password': password
                        }
                        login_list = add_dict(login_dict, login_list)
                        progress_list.remove(single_dict)
                        break            
            line = file_object.readline()

    return login_list

def add_dict(login_dict, login_list):

    for index, single_list in enumerate(login_list):
        if login_dict == single_list[1]:
            count = single_list[0] + 1
            login_list[index] = [count, login_dict]
            return login_list

    single_list = [1,login_dict]
    login_list.append(single_list)
    return login_list

def print_output(login_list, format):

    if format == 'csv':
        print(' [+] Writing data to results.csv...')
        with open('results.csv', 'w') as f:
            writer = csv.writer(f)
            for single_list in login_list:
                user = single_list[1].get('user')
                password = single_list[1].get('password')
                row = [single_list[0],user,password]
                writer.writerow(row)
        print(' [+] Done')
    else:
        print(' [+] Writing data to results.txt...')
        with open('results.txt', 'w') as f:
            for single_list in login_list:
                user = single_list[1].get('user')
                password = single_list[1].get('password')
                if not password:
                    password = '[NONE]'
                row = str(single_list[0]) + ': ' + user + ' // ' + password + '\n'
                f.write(row)
        print(' [+] Done')

def main():

    logo_msg = ('\n VSFTPD Log Parser v' + __version__ +
                '\n A tool for pulling authentication data from a VSFTPD log.')

    example_msg = ('example: ' +
                   '\n $ python vsftpd_parse.py --input vsftpd.log --output csv\n')

    parser = argparse.ArgumentParser(add_help=False,formatter_class=argparse.RawTextHelpFormatter,epilog=example_msg)
    parser.add_argument('-h', '--help', dest='show_help', action='store_true', help='Show this message and exit\n\n')
    parser.add_argument('-i', '--input', help='The log file name you want to parse\n', type=str)
    parser.add_argument('-o', '--output', help='The format of the results\n', type=str.lower, choices=['csv', 'txt'])
    parser.set_defaults(show_help='False')
    args = parser.parse_args()

    print(logo_msg)

    if args.show_help is True or not args.input or not args.output:
        print('')
        print(parser.format_help())
        sys.exit(0)

    print('')

    login_list = parse_log(args.input)
    login_list = sorted(login_list, key=lambda x:(-x[0], x[1].values()[0], x[1].values()[1]))

    print_output(login_list, args.output)

    print('')

if __name__ == '__main__':
    sys.exit(main())