#!/usr/bin/python

import os, sys, re
from datetime import datetime, timedelta

TIME_REGEX = r"^[\d]{2}:[\d]{2}:[\d]{2}"

# open the file if it exists and return it as text
def open_file(filename):
    with open(filename, "r") as txt:
        return txt.read()

# return a list of captions/time dictionaries
def format_lines(text):
    lines = []
    for line in text.splitlines():
        match = re.search(TIME_REGEX, line)
        if match is not None:
            lines.append({
                "time": line[match.start(): match.end()],
                "caption": line[match.end():].lstrip()
            })
    return lines

# helper function to convert our timestamps!
def convert_to_datetime(time_string):
    return datetime.strptime(time_string, "%H:%M:%S")

# this is the SRT format!
"""
1
00:00:01,00 --> 00:00:10,00
Hello, this is an SRT caption! Yeah!

"""

def format_srt(lines):

    # add one blank one to the end because we're calculating times by look back
    final_datetime = convert_to_datetime(lines[-1]["time"])
    # for the last 1 maybe just add 15 seconds on the end...
    final_timestamp = str((final_datetime + timedelta(seconds=15)).time())
    lines.append({
        "time": final_timestamp,
        "caption": ""
    })
    
    # intial values before we get started
    srt = ""
    line_number = 1
    init_datetime = convert_to_datetime(lines[0]["time"])
    prev_datetime = convert_to_datetime(lines[0]["time"])
    prev_timestamp = "00:00:01,00"
    
    # start at 1 look earlier to find the duration
    for line_index in range(1, len(lines)):
        
        curr_datetime = convert_to_datetime(lines[line_index]["time"])

        # check that the duration is positive
        if (curr_datetime - prev_datetime) > timedelta(seconds=0):
            
            # add the new linenumber with extra whitespace
            srt += "\n\n{}\n".format(line_number)

            # get the current time in hours:minutes:seconds,milliseconds format
            # assume 00 milliseconds
            curr_timestamp = str(curr_datetime - init_datetime) + ",00"
            # the timestamps when we want the text to be displayed
            srt += "{} --> {}\n".format(prev_timestamp, curr_timestamp)
            # the text we want displayed
            srt += lines[line_index-1]["caption"]

            # increment the line_number
            line_number += 1
            # also move the times forward
            prev_datetime = curr_datetime
            prev_timestamp = curr_timestamp

        else:

            # if the duration was negative add the text to the previous line
            srt += lines[line_index-1]["caption"]

    # strip off leading whitespace
    return srt.lstrip()


if __name__ == "__main__":
    
    if len(sys.argv) < 2:
        raise Exception("You must provide a filename\nexample: txt2srt closed_caption.txt\n")
    
    # the user will provide a command line argument of the file to convert
    text_transcript = open_file(sys.argv[1])
    
    # this reads in the file and gives it back as text
    text_lines = format_lines(text_transcript)
    
    # I think if a video is recorded that overlaps midnight something weird will happen...
    # create a srt file and save the subtitles to it
    with open('closed_caption.srt', 'w+') as captions:
        captions.write(format_srt(text_lines))