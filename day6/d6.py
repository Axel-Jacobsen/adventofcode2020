#! /usr/bin/env python3


with open('test_input.txt', 'r') as f:
    group_answers = f.read().split('\n\n')
    num_qs_anyone = 0
    num_qs_everyone = 0
    for group in group_answers:
        person_answers = group.strip().split('\n')
        everyone_answered = set(person_answers[0]).intersection(*person_answers[1:])
        num_qs_anyone += len(set(list(group.replace('\n', ''))))
        num_qs_everyone += len(everyone_answered)
    print('part 1', num_qs_anyone)
    print('part 2', num_qs_everyone)
