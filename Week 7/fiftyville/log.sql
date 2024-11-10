-- Keep a log of any SQL queries you execute as you solve the mystery.

-- .schema to see db structure

-- View crime report
SELECT description
FROM crime_scene_reports
WHERE year = 2023
AND month = 07
AND day = 28
AND street = 'Humphrey Street';


/*Output:
Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery. Interviews were conducted today
with three witnesses who were present at the time – each of their interview transcripts mentions the bakery. |
| Littering took place at 16:36. No known witnesses.
*/

-- Look at interview names and logs and look at them one by one:
SELECT name
FROM interviews
WHERE year = 2023
AND month = 07
AND day = 28;

SELECT transcript, id
FROM interviews
WHERE year = 2023
AND month = 07
AND day = 28
AND name = 'Jose'; -- Do the same for others

/*
Output: Ruth
Sometime within ten minutes of the theft,
I saw the thief get into a car in the bakery parking lot and drive away.
If you have security footage from the bakery parking lot, you might want
to look for cars that left the parking lot in that time frame.

Output: Eugene-2 (id:162) - there are 2 entries for Eugene
I don't know the thief's name, but it was someone I recognized.
Earlier this morning, before I arrived at Emma's bakery,
I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money.

Output: Raymond
As the thief was leaving the bakery, they called someone who talked to them for less than a minute.
In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow.
The thief then asked the person on the other end of the phone to purchase the flight ticket.

Output: Transcript from Lily, Jose, Barbara, Eugene-1 (id: 159)
Not useful transcript. I like how they quote Sherlock Holmes though
*/

-- First tackling Eugene-2's ATM transaction lead:

SELECT * FROM atm_transactions
WHERE year = 2023
AND month = 7
AND day = 28
AND atm_location = 'Leggett Street'
AND transaction_type = 'withdraw';

/*
Output:
+-----+----------------+------+-------+-----+----------------+------------------+--------+
| id  | account_number | year | month | day |  atm_location  | transaction_type | amount |
+-----+----------------+------+-------+-----+----------------+------------------+--------+
| 246 | 28500762       | 2023 | 7     | 28  | Leggett Street | withdraw         | 48     |
| 264 | 28296815       | 2023 | 7     | 28  | Leggett Street | withdraw         | 20     |
| 266 | 76054385       | 2023 | 7     | 28  | Leggett Street | withdraw         | 60     |
| 267 | 49610011       | 2023 | 7     | 28  | Leggett Street | withdraw         | 50     |
| 269 | 16153065       | 2023 | 7     | 28  | Leggett Street | withdraw         | 80     |
| 288 | 25506511       | 2023 | 7     | 28  | Leggett Street | withdraw         | 20     |
| 313 | 81061156       | 2023 | 7     | 28  | Leggett Street | withdraw         | 30     |
| 336 | 26013199       | 2023 | 7     | 28  | Leggett Street | withdraw         | 35     |
+-----+----------------+------+-------+-----+----------------+------------------+--------+
*/

-- Let me see what going on with their bank accounts
SELECT person_id, a.account_number, b.creation_year, a.amount, p.name, p.phone_number, p.passport_number, p.license_plate
FROM bank_accounts AS b
JOIN atm_transactions AS a
    ON a.account_number = b.account_number
JOIN people AS p
    ON p.id = b.person_id
WHERE
    year = 2023
    AND month = 7
    AND day = 28
    AND atm_location = 'Leggett Street'
    AND transaction_type = 'withdraw';
/*
Output:
+-----------+----------------+---------------+--------+---------+----------------+-----------------+---------------+
| person_id | account_number | creation_year | amount |  name   |  phone_number  | passport_number | license_plate |
+-----------+----------------+---------------+--------+---------+----------------+-----------------+---------------+
| 686048    | 49610011       | 2010          | 50     | Bruce   | (367) 555-5533 | 5773159633      | 94KL13X       |
| 514354    | 26013199       | 2012          | 35     | Diana   | (770) 555-1861 | 3592750733      | 322W7JE       |
| 458378    | 16153065       | 2012          | 80     | Brooke  | (122) 555-4581 | 4408372428      | QX4YZN3       |
| 395717    | 28296815       | 2014          | 20     | Kenny   | (826) 555-1652 | 9878712108      | 30G67EN       |
| 396669    | 25506511       | 2014          | 20     | Iman    | (829) 555-5269 | 7049073643      | L93JTIZ       |
| 467400    | 28500762       | 2014          | 48     | Luca    | (389) 555-5198 | 8496433585      | 4328GD8       |
| 449774    | 76054385       | 2015          | 60     | Taylor  | (286) 555-6063 | 1988161715      | 1106N58       |
| 438727    | 81061156       | 2018          | 30     | Benista | (338) 555-6650 | 9586786673      | 8X428L0       |
+-----------+----------------+---------------+--------+---------+----------------+-----------------+---------------+
*/

-- Raymond mentioned a phone call lasting less than aminute.
-- Let me check call logs and cross reference the phone numbers from above result
-- I am assuming the 'less than 1 min' part is accurate. Normally I wont trust that

SELECT  p1.caller, p2.name AS caller_name, p2.passport_number AS caller_passport, p1.duration,
        p2.license_plate  AS caller_license,
        p1.receiver, p3.name AS receiver_name, p3.passport_number AS receiver_passport,
        p3.license_plate  AS receiver_license
FROM phone_calls as p1
JOIN people AS p2
ON p1.caller = p2.phone_number
JOIN people AS p3
ON p1.receiver = p3.phone_number
WHERE
    duration <60
    AND caller IN (
        SELECT p.phone_number
        FROM bank_accounts AS b
        JOIN atm_transactions AS a
            ON a.account_number = b.account_number
        JOIN people AS p
            ON p.id = b.person_id
        WHERE
            year = 2023
            AND month = 7
            AND day = 28
            AND atm_location = 'Leggett Street'
            AND transaction_type = 'withdraw');
/*
Output:
+----------------+-------------+-----------------+----------+----------------+----------------+---------------+-------------------+------------------+
|     caller     | caller_name | caller_passport | duration | caller_license |    receiver    | receiver_name | receiver_passport | receiver_license |
+----------------+-------------+-----------------+----------+----------------+----------------+---------------+-------------------+------------------+
| (367) 555-5533 | Bruce       | 5773159633      | 45       | 94KL13X        | (375) 555-8161 | Robin         | NULL              | 4V16VO0          |
| (286) 555-6063 | Taylor      | 1988161715      | 43       | 1106N58        | (676) 555-6554 | James         | 2438825627        | Q13SVG6          |
| (770) 555-1861 | Diana       | 3592750733      | 49       | 322W7JE        | (725) 555-3243 | Philip        | 3391710505        | GW362R6          |
| (826) 555-1652 | Kenny       | 9878712108      | 55       | 30G67EN        | (066) 555-9701 | Doris         | 7214083635        | M51FA04          |
| (338) 555-6650 | Benista     | 9586786673      | 54       | 8X428L0        | (704) 555-2131 | Anna          | NULL              | NULL             |
| (367) 555-5533 | Bruce       | 5773159633      | 31       | 94KL13X        | (455) 555-5315 | Charlotte     | 7226911797        | Z5FH038          |
+----------------+-------------+-----------------+----------+----------------+----------------+---------------+-------------------+------------------+
*/

-- From the above list let me see who flew the day after on the earliest flight. To start let me find airport IDs
SELECT a1. id, a1.full_name AS origin_airport, a2.id, a2.full_name AS destination_airport, f.hour, f.minute, a2.city AS destination_city, f.id AS flight_id
FROM flights AS f
JOIN airports AS a1
ON a1.id = f.origin_airport_id
JOIN airports AS a2
ON a2.id = f.destination_airport_id
WHERE
    year = 2023
    AND month = 7
    AND day = 29
    AND a1.full_name LIKE '%Fiftyville%'
ORDER BY hour, minute
LIMIT 1;

/*
Output:
+----+-----------------------------+----+---------------------+------+--------+------------------+-----------+
| id |       origin_airport        | id | destination_airport | hour | minute | destination_city | flight_id |
+----+-----------------------------+----+---------------------+------+--------+------------------+-----------+
| 8  | Fiftyville Regional Airport | 4  | LaGuardia Airport   | 8    | 20     | New York City    | 36        |
+----+-----------------------------+----+---------------------+------+--------+------------------+-----------+
*/

-- Now checking who flew that day on that flight
SELECT p1.name
FROM people AS p1
JOIN passengers AS p2
    ON p1.passport_number = p2.passport_number
JOIN flights as f
    ON f.id = p2.flight_id
JOIN airports AS a
    ON a.id = f.origin_airport_id
WHERE
    year = 2023
    AND month = 7
    AND day = 29
    AND f.id =36;
/*
Output:
+--------+
|  name  |
+--------+
| Doris  |
| Sofia  |
| Bruce  |
| Edward |
| Kelsey |
| Taylor |
| Kenny  |
| Luca   |
+--------+
*/

-- Checking out the bakery that everyone keeps mentioning
SELECT *
FROM bakery_security_logs
WHERE
    year = 2023
    AND month = 7
    AND day = 28
    AND hour = 10
    AND minute <25
    AND minute >15;
/*
Output:
+-----+------+-------+-----+------+--------+----------+---------------+
| id  | year | month | day | hour | minute | activity | license_plate |
+-----+------+-------+-----+------+--------+----------+---------------+
| 260 | 2023 | 7     | 28  | 10   | 16     | exit     | 5P2BI95       |
| 261 | 2023 | 7     | 28  | 10   | 18     | exit     | 94KL13X       |
| 262 | 2023 | 7     | 28  | 10   | 18     | exit     | 6P58WS2       |
| 263 | 2023 | 7     | 28  | 10   | 19     | exit     | 4328GD8       |
| 264 | 2023 | 7     | 28  | 10   | 20     | exit     | G412CB7       |
| 265 | 2023 | 7     | 28  | 10   | 21     | exit     | L93JTIZ       |
| 266 | 2023 | 7     | 28  | 10   | 23     | exit     | 322W7JE       |
| 267 | 2023 | 7     | 28  | 10   | 23     | exit     | 0NTHK55       |
+-----+------+-------+-----+------+--------+----------+---------------+
*/

--Cross referencing this with people and their license plates:

SELECT name
FROM people
WHERE license_plate IN
(
    SELECT license_plate
    FROM bakery_security_logs
    WHERE
        year = 2023
        AND month = 7
        AND day = 28
        AND hour = 10
        AND minute <25
        AND minute >15
);

/*
Output:
+---------+
|  name   |
+---------+
| Vanessa |
| Barry   |
| Iman    |
| Sofia   |
| Luca    |
| Diana   |
| Kelsey  |
| Bruce   |
+---------+
*/

-- Checking who made the phone call and withdrew money from ATM from the above list

SELECT  DISTINCT(p2.name) AS caller_name
FROM phone_calls as p1
JOIN people AS p2
ON p1.caller = p2.phone_number
WHERE
    duration <60
    AND caller IN
(
        SELECT p.phone_number
        FROM bank_accounts AS b
        JOIN atm_transactions AS a
            ON a.account_number = b.account_number
        JOIN people AS p
            ON p.id = b.person_id
        WHERE
            year = 2023
            AND month = 7
            AND day = 28
            AND atm_location = 'Leggett Street'
            AND transaction_type = 'withdraw'
            AND p.name IN
            (
               SELECT name
                FROM people
                WHERE license_plate IN
                (
                    SELECT license_plate
                    FROM bakery_security_logs
                    WHERE
                        year = 2023
                        AND month = 7
                        AND day = 28
                        AND hour = 10
                        AND minute <25
                        AND minute >15
                )
            )
);

/*
Output:
+-------------+
| caller_name |
+-------------+
| Diana       |
| Bruce       |
+-------------+

These are the names of people who:
Left the bakery within 10 mins of crime
Withdrew money from ATM
Had a phone call lasting less than 1 min

Now what reamins is to see who took a flight the next day
*/
 WITH suspects (suspect_name) AS
 (
    SELECT  DISTINCT (p2.name) AS caller_name
    FROM phone_calls as p1
    JOIN people AS p2
    ON p1.caller = p2.phone_number
    WHERE
        duration <60
        AND caller IN
    (
        SELECT p.phone_number
        FROM bank_accounts AS b
        JOIN atm_transactions AS a
            ON a.account_number = b.account_number
        JOIN people AS p
            ON p.id = b.person_id
        WHERE
            year = 2023
            AND month = 7
            AND day = 28
            AND atm_location = 'Leggett Street'
            AND transaction_type = 'withdraw'
            AND p.name IN
            (
               SELECT name
                FROM people
                WHERE license_plate IN
                (
                    SELECT license_plate
                    FROM bakery_security_logs
                    WHERE
                        year = 2023
                        AND month = 7
                        AND day = 28
                        AND hour = 10
                        AND minute <25
                        AND minute >15
                )
            )
    )
)

SELECT suspect_name
FROM suspects
WHERE suspect_name IN
(
    SELECT DISTINCT(p1.name)
    FROM people AS p1
    JOIN passengers AS p2
        ON p1.passport_number = p2.passport_number
    JOIN flights as f
        ON f.id = p2.flight_id
    JOIN airports AS a
        ON a.id = f.origin_airport_id
    WHERE
        year = 2023
        AND month = 7
        AND day = 29
        AND f.id = 36
);

/*
Output:
+--------------+
| suspect_name |
+--------------+
| Bruce        |
+--------------+

GOT EM!
*/

--Who did Bruce call?

SELECT p3.name AS accomplice
FROM phone_calls AS p1
JOIN people as p2
    ON p1.caller = p2.phone_number
JOIN people as p3
    ON p1.receiver = p3.phone_number
WHERE
    year = 2023
    AND month = 7
    AND day = 28
    AND p2.name = 'Bruce'
    AND duration <60;
/*
Output:
+------------+
| accomplice |
+------------+
| Robin      |
+------------+
*/


