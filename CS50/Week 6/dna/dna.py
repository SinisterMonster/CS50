import csv
import sys


def main():

    # Check for command-line usage
    if len(sys.argv) != 3:
        print("Error in argument. Format: <STR database file.csv> <DNA sequence to identify.txt>")
        return

    # Read database file into a variable
    databaseRows = []
    with open(sys.argv[1], newline='') as dbfile:
        database = csv.DictReader(dbfile)
        for row in database:
            databaseRows.append(row)

        # Read fieldnames and remove "name"
        fieldnames = database.fieldnames
        fieldnames.remove('name')

    # Read DNA sequence file into a variable
    with open(sys.argv[2]) as sqfile:
        sequence = sqfile.read()

    # Find longest match of each STR in DNA sequence
    sequence_match = {}

    # Create dict of longest STR found in sequence
    for i in range(len(fieldnames)):
        sequence_match[fieldnames[i]] = longest_match(sequence, fieldnames[i])

    # Check database for matching profiles

    for person in databaseRows:
        match_finder = 0
        for STR in sequence_match:
            # Check and update match_finder
            if (int(person[STR]) == int(sequence_match[STR])):
                match_finder += 1

            # If match equals the # of STRs then we found person
            if match_finder == len(sequence_match):
                print(person['name'])
                return
    print("No match")


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
