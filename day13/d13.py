#! /usr/bin/env python3


def closest_over(target, period):
    """
    return the smallest number greater than target
    that is divisible by period

    """
    for i in range(target, target + period):
        if i % period == 0:
            return i


def p1():
    with open("input.txt", "r") as f:
        earliest_timestamp = int(f.readline().strip())
        busses = [int(b) for b in f.readline().split(",") if b != "x"]
        earliests = sorted(
            [(b, closest_over(earliest_timestamp, b)) for b in busses],
            key=lambda v: v[1],
        )
    return earliests[0][0] * (earliests[0][1] - earliest_timestamp)


def format_bus_str(bus_str):
    return sorted(
        [(i, int(b)) for i, b in enumerate(bus_str.strip().split(",")) if b != "x"],
        key=lambda v: v[1],
        reverse=True,
    )


def get_earliest_timestamp_brute(busses):
    lb_offset, lb = busses[0]
    t = lb
    while True:
        valid = True
        for t_offset, bus_num in busses[1:]:
            if (t + t_offset - lb_offset) % bus_num != 0:
                valid = False
                break

        if valid:
            return t - lb_offset

        t += lb


def brute_p2(fname):
    with open(fname, "r") as f:
        f.readline()  # first line useless
        return get_earliest_timestamp_brute(format_bus_str(f.readline()))


def test_p2():
    assert get_earliest_timestamp_brute(format_bus_str("17,x,13,19")) == 3417
    assert get_earliest_timestamp_brute(format_bus_str("67,7,59,61")) == 754018
    assert get_earliest_timestamp_brute(format_bus_str("67,x,7,59,61")) == 779210
    assert get_earliest_timestamp_brute(format_bus_str("67,7,x,59,61")) == 1261476
    assert get_earliest_timestamp_brute(format_bus_str("1789,37,47,1889")) == 1202161486
    print("Tests passed")


print(p1())
print("test p2")
test_p2()
print("p2")
print(brute_p2(fname="input.txt"))
