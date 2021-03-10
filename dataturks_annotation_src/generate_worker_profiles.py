import json
import random
import argparse


def randompassword():
    # maximum length of password needed
    # this can be changed to suit your password length
    MAX_LEN = 12

    # declare arrays of the character that we need in out password
    # Represented as chars to enable easy string concatenation
    DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    LOCASE_CHARACTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
                         'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q',
                         'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
                         'z']

    UPCASE_CHARACTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
                         'I', 'J', 'K', 'M', 'N', 'O', 'p', 'Q',
                         'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
                         'Z']

    SYMBOLS = ['@', '#', '$', '%', '=', ':', '?', '.', '/', '|', '~', '>',
               '*', '(', ')', '<']

    # combines all the character arrays above to form one array
    COMBINED_LIST = DIGITS + UPCASE_CHARACTERS + LOCASE_CHARACTERS + SYMBOLS

    # randomly select at least one character from each character set above
    rand_digit = random.choice(DIGITS)
    rand_upper = random.choice(UPCASE_CHARACTERS)
    rand_lower = random.choice(LOCASE_CHARACTERS)
    rand_symbol = random.choice(SYMBOLS)

    # combine the character randomly selected above
    # at this stage, the password contains only 4 characters but
    # we want a 12-character password
    temp_pass = rand_digit + rand_upper + rand_lower + rand_symbol


    # now that we are sure we have at least one character from each
    # set of characters, we fill the rest of
    # the password length by selecting randomly from the combined
    # list of character above.
    for x in range(MAX_LEN - 4):
        temp_pass = temp_pass + random.choice(COMBINED_LIST)

    # convert temporary password into array and shuffle to
    # prevent it from having a consistent pattern
    # where the beginning of the password is predictable
    temp_pass_list = list(temp_pass)
    random.shuffle(temp_pass_list)

    return "".join(temp_pass_list)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="generate the profiles of workers")
    parser.add_argument('--input', required=True, help="the path to the emails of the workers")
    parser.add_argument('--output', required=True, help="the path to the output worker profiles")
    parser.add_argument('--seed', type=int, default=0, help="number of passwords to generate")
    args = parser.parse_args()

    random.seed(args.seed)

    with open(args.input, 'r') as f:
        worker_profiles = {}
        for idx, email in enumerate(f):
            email = email.strip()
            assert email.endswith("@instacart.com"), email
            name = email[:-14]
            firstname = "".join(name.split('.')[:-1]).capitalize()
            secondname = name.split('.')[-1].capitalize()
            worker_profiles[email] = {
                "worker_id": idx,
                "email": email,
                "firstname": firstname,
                "secondname": secondname,
                'password': randompassword()
            }

    with open(args.output, 'w') as f:
        json.dump(worker_profiles, f, indent=2)
