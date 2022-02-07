#!/usr/bin/env python3

import itertools
import sys
from typing import Callable, Dict, List, Optional, Set

import enchant


def collatzStep(i: int) -> int:
    count = 0
    while i != 1:
        count += 1
        if i % 2 == 0:
            i /= 2
        else:
            i = 3 * i + 1
    return count


def buildReverseCollatzDict(rangeMin: int, rangeMax: int) -> Dict[int, Set[int]]:
    reverseCollatzDict = {}
    for (i, c) in [(i, collatzStep(i)) for i in range(rangeMin, rangeMax)]:
        if c not in reverseCollatzDict:
            reverseCollatzDict[c] = set()
        reverseCollatzDict[c].add(i)
    return reverseCollatzDict


def search(cipher: str, reverseCollatzDict: Dict[int, Set[int]], characterFilter: Callable[[str], bool],
           start: int, end: int, offset: int, accumulator: List[Set[str]]) -> Optional[List[Set[str]]]:
    if start == len(cipher):
        return accumulator
    else:
        while end <= len(cipher):
            current = int(cipher[start:end])
            if current in reverseCollatzDict:
                possibleASCII = set()
                for item in reverseCollatzDict[current]:
                    try:
                        if characterFilter(chr(item - offset)):
                            possibleASCII.add(chr(item - offset))
                    except ValueError:
                        pass
                if len(possibleASCII) == 0:
                    end += 1
                    continue
                newAccumulator = accumulator.copy()
                newAccumulator.append(possibleASCII)
                result = search(cipher, reverseCollatzDict, characterFilter, end, end + 1, current, newAccumulator)
                if result is not None:
                    return result
                else:
                    end += 1
            else:
                end += 1
        return None


def cleanse(searchResult: List[Set[str]]) -> List[Set[str]]:
    english = enchant.Dict("en_GB")

    # Use space as a terminator, rather than a delimiter.
    # The last group would be ignored if there is no space group at the tail.
    searchResult.append({' '})

    result = []
    currentGroup = []
    for s in searchResult:
        if len(s) == 1:
            c = s.pop()
            if c != ' ':
                # Not a terminator, continue
                s.add(c)
                currentGroup.append(s)
            else:
                # Encounter a terminator. Calculate all the possibilities as an English word.
                wordPossibilities = set()

                for element in itertools.product(*currentGroup):
                    string = "".join(element)
                    if string.islower() or string.istitle():
                        if english.check(string):
                            wordPossibilities.add(string)
                result.append(wordPossibilities)
                currentGroup = []
        else:
            # Not a terminator, continue
            currentGroup.append(s)

    return result


def writeResult(filename: str, result: List[Set[str]]) -> None:
    with open(filename, "w") as f:
        for index, wordPossibilities in enumerate(result):
            f.write(f"Word {index + 1}:\n")
            for possibleWord in wordPossibilities:
                f.write(f"{possibleWord}\n")
            f.write('\n')


def main(argv: List[str]) -> None:
    cipher = "27322810313331033910211452912207344136146925461033281533271031012815108114101"

    reverseCollatzDict = buildReverseCollatzDict(0x01, 0xff)
    searchResult = search(
        cipher, reverseCollatzDict, lambda c: (c.isascii() and c.isalpha()) or (c in " "),
        0, 1, 0, [])
    if searchResult is None:
        print("No possible result found")
    else:
        result = cleanse(searchResult)
        writeResult("output.txt", result)


if __name__ == "__main__":
    main(sys.argv)
