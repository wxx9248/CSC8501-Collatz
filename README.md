# CSC8501-Collatz

Part of CSC8501 Coursework – 2021

Provided by [@NachtgeistW](https://github.com/NachtgeistW)

Author: Dr. Graham Morgan, Newcastle University

## Specification

Assume an algorithm that encrypts (actually "hashes", or more precisely, "maps") a plain-text string of characters
with [Collatz Conjecture](https://en.wikipedia.org/wiki/Collatz_conjecture) with the following procedure:

For each character in the plain-text string:

1. The character is turned into its ASCII decimal representation, and an offset (seed) is added;
2. Count the number of turns required for the algorithm with input as the decimal above to reach `1` for the first time;
3. This number is the encrypted version of the character, and it is concatenated with previous output without space;
4. This number becomes the new offset value for the next character.

The input is limited by the following conditions:

* Characters are limited to the printable ASCII characters;
* Strings can be in any length;
* Each character of the string is considered from left to right when encrypting.

## Problem

Given a string of ciphertext, specifically:
```27322810313331033910211452912207344136146925461033281533271031012815108114101```

We want to crack out the corresponding plain text.

The following conditions are known:

* An offset value of `0` is initially set (Initialization Vector) for the first character of the plain text;
* The plain text is a well-known sentence in English.

## General Approach

The most challenging part is how to divide the long string of ciphertext into small pieces that each one could properly
represent an encrypted printable ASCII character. I used simple backtracking to determine possible correct combinations.

### Notions

|              Name              |   Type   | Description                                                                                                                                                                                                             |
|:------------------------------:|:--------:|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|     Collatz Step Function      | Function | The function `f(n)` that is defined in the Collatz Conjecture. See Wikipedia.                                                                                                                                           |
|         Collatz Number         | Integer  | The number of turns required for a positive integer input to reach `1` for the first time with the Collatz Step Function `f(n)` being applied iteratively. The algorithm is realized in Collatz Number Generator (CNG). |
| Collatz Number Generator (CNG) | Function | The function that is used to generate a Collatz Number from an integer.                                                                                                                                                 |

### Reverse Collatz Dictionary

I built a dictionary that contains all the possible mappings from a Collatz Number to a set of possible corresponding
ASCII codes. The dictionary will give out some clue that how to partition the known ciphertext.

The most important part of building this dictionary is to determine the possible range of Collatz Numbers that the
algorithm may produce. I tried to determine the range but failed. So I have to guess one and do trial and error.
Fortunately, my first guess `[0x01, 0xff)` worked. It is sufficient for the string of ciphertext.

### Search by Backtracking

The searching algorithm is a recursion.

* Values from the previous recursion:
    * `start` and `end`, which determine a slice that comes from the ciphertext string.
        * `start` is inclusive; `end` is exclusive.
        * At the beginning of each recursion, `end` is always `start + 1`, which indicates that the slice has
          length `1` (which has only one character).
    * `offset`, which is the cipher character from the previous recursion.
    * `accumulator`, which contains all possibilities for each character.

The following steps describe the algorithm:

1. The slice from the previous step is converted to an integer afterwards.
1. Search the reverse collatz dictionary for the integer from the previous step.
    * If exists, continue to the next step.
    * If not exists, increment `end` cursor with 1 and go back to Step 1.
1. Retrieve the corresponding result (a set) from the reverse collatz dictionary.
1. For each element in the set from the previous step:
    * Subtract the element with `offset` and test if it is a valid ASCII letter or a space.
        * If succeeds, add the corresponding character to a set.
        * If fails, try the next element.
1. Test the length of the set obtained from the previous step.
    * If it is `0`, increment `end` cursor with 1 and go back to Step 1.
1. Copy the current accumulator and pass it to the next recursion.

Since we know that the first offset value is `0`, we may start searching for the first character.

### Data Cleansing

The search algorithm would generate a list that contains multiple non-empty sets. Each set contains all possibilities
for each character.

Since the plain text is an English sentence, we could determine each word by the delimiter `' '` (space).

Then we can use an English dictionary (in this case, PyEnchant library) to purge out combinations that are not English
words.

The output would contain few words and is easy to identify the answer from.

## Output and Answer

A sample output of the algorithm is listed below:

```
Word 1:
A
B
C

Word 2:
friend

Word 3:
to
vi
ti

Word 4:
ail
all

Word 5:
it
es
is

Word 6:
a

Word 7:
friend

Word 8:
to
so

Word 9:
pone
zone
pond
lope
pope
nope
pole
none
lone

```

We could easily find the sentence:
> A friend to all is a friend to none.
>
> -- <cite>Aristotle</cite>
