import re
import piping_handler

def get_lp_and_confidence(path_to_picture):
    full_command = "alpr -n 8 -c eu -p nl " + path_to_picture
    try:
        output, err = piping_handler.run_script(full_command)
    except BrokenPipeError as err:
        print("Error running ALPR")
        return "0", 0

    output = output.decode(encoding='utf-8')
    if "results" in output:
        lines = output.split("\n")
        for line in lines:
            if "pattern_match: 1" in line:
                print("output")
                lp = re.search("- (.*)\t conf", line)
                conf = re.search('confidence: (.*)\t patt', line)
                lp_string = lp.group(1)
                conf_float = float(conf.group(1))
                return lp_string, conf_float
    return "0", 0
