import csv

class DBController():

    # function takes a string(comma seperated!)
    # and puts it in the csv file
    def csv_write(list):
        with open('lp_db.csv', 'a') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=',')
            csv_writer.writerow(list)

    # function that searchers the csv db for a
    # given license plate and returns
    # the results in a dict
    def csv_check_match_lp(licsene_plate):
        i = 1
        dict = {}
        with open('lp_db.csv', 'rt') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=',')
            for row in csv_reader:
                if row[0] == licsene_plate:
                    dict[i] = row
                    i += 1
        return dict

    def search_csv_for_match(license_plate):
        string = ""
        matches = csv_check_match_lp("GZVX47")
        if matches != {}:
            string = ("We have a logged history of this licenseplate:" + n)
            for row in matches:
                string += ("location:" + t + matches[row][ADDRESS_POS] + n)
                string += ("date     " + t + matches[row][TIME_POS] + n)
        return string
