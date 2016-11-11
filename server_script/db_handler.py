import csv


# function takes a string(comma separated!)
# and puts it in the csv file
def db_write(csv_str_data, db_path):
    try:
        with open(db_path, 'a') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',')
            csv_writer.writerow(csv_str_data)
        return 1
    except FileNotFoundError as err:
        print("Could not write to db:", err)
        return 0


# function that searchers the csv db for a
# given license plate and returns
# the results in a dictionary
def get_matches(license_plate, db_path):
    i = 1
    dict = {}
    with open(db_path, 'rt') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            print(row)
            if row[0] == license_plate:
                dict[i] = row
                i += 1
    return dict
