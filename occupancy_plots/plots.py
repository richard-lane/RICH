import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from matplotlib.ticker import AutoMinorLocator, MultipleLocator
import re


def parse(strings):
    """
    Parse ints and floats for mirror number + occupancy from a match group string

    """
    # Separated by a double spac
    s = strings.split("  ")
    return int(s[0][:-1]), int(s[1][:-1]), float(s[2])


def group(n, line, regex):
    """
    Get the nth match group found from line in regex, and convert from strings to (primary number, secondary number, occupancy)

    """
    # Separated by double spaces
    match = regex.match(line)
    if not match:
        raise re.error(f"No match found in line:\n\tcontents:{line}")

    # Two cases: either we've matched a long line with many match groups
    # Or a short line with only one match, the rest are None
    groups = match.groups()

    if not groups[1]:
        # Short line matched
        if n:
            raise re.error(
                f"No group {n} available on line:\n\tgroups:{groups}\nThis may be ok if you asked for a subset of mirror combinations (e.g. the MST)"
            )
        return parse(groups[n])

    # If we get here, long line match. So ignore the second match group as thats just the entire line
    groups = [groups[i] for i in range(len(groups)) if i != 1]

    return parse(groups[n])


def entire_bigraph(line, regex):
    """
    Returns (primary mirror number, secondary mirror number, occupancy)

    """
    # The information for the entire bigraph is in the 0th match group (i.e. it's the first relevant column in the text file)
    return group(0, line, regex)


def minimum_spanning_solution(line, regex):
    """
    Returns (primary mirror number, secondary mirror number, occupancy)

    """
    # MST is in the 2nd match group (0 indexed)
    return group(2, line, regex)


def old_spanning_tree(line, regex):
    """
    Returns (primary mirror number, secondary mirror number, occupancy)

    """
    # old spanning tree is in the 4th match group (0 indexed)
    return group(4, line, regex)


def plot(array, title, path):
    plt.clf()
    f, ax = plt.subplots(1, 1)
    axcolor = f.add_axes()
    im = ax.matshow(array, norm=LogNorm(vmin=10, vmax=1000000))

    colorbar = f.colorbar(im, cax=axcolor)
    colorbar.ax.set_ylabel("# Photon Hits")

    # Grid and stuff
    ax.xaxis.set_major_locator(MultipleLocator(5))
    ax.yaxis.set_major_locator(MultipleLocator(5))

    ax.xaxis.set_minor_locator(AutoMinorLocator(5))
    ax.yaxis.set_minor_locator(AutoMinorLocator(5))

    plt.grid(linewidth=0.3, color="k", which="major", alpha=1)
    plt.grid(linewidth=0.2, color="k", which="minor", alpha=0.5)

    ax.set_xlabel("Secondary mirror number")
    ax.set_ylabel("Primary mirror number")

    f.suptitle(title)
    print(f"Creating {title}")
    plt.savefig(path)
    plt.clf()


def main():
    # Read in the file
    with open("mirror_combinations_rich2_side0.txt", "r") as f:
        contents = f.readlines()

    # Regex for parsing things
    # 22 arbitrary characters at the start of the line, then the relevant things are enclosed in (parentheses)
    # Each thing in parentheses  is formatted as XXp XXs XXXXX.0 for primary mirror, secondary mirror and occupancy
    # Or... matches one (thing in parentheses, and nothing else)
    # I wouldn't try to make sense of this if i were you, just check it works sensibly and move on with your life
    pattern = r"^.{22}\((\d\dp\s+\d\ds\s+\d+\.0)\)(\s+\((\d\dp\s+\d\ds\s+\d+\.0)\)\s+\((\d\dp\s+\d\ds\s+\d+\.0)\)\s+\((\d\dp\s+\d\ds\s+\d+\.0)\)\s+\((\d\dp\s+\d\ds\s+\d+\.0)\)\s+\((\d\dp\s+\d\ds\s+\d+\.0)\)|)$"
    regex = re.compile(pattern)

    # Number of primary and secondary mirrors
    n_primary_mirrors = 28
    n_secondary_mirrors = 20

    all_occupancies = np.zeros((n_primary_mirrors, n_secondary_mirrors))
    mst_occupancies = np.zeros((n_primary_mirrors, n_secondary_mirrors))
    old_occupancies = np.zeros((n_primary_mirrors, n_secondary_mirrors))

    # Iterate over the data in the file, collecting the information we want and exiting early if we run out of stuff to read
    print("Iterating over lines")

    # Bool flag telling us whether to attempt to read from the MST or old columns (they have fewer lines)
    read_short = True

    for line in contents[2:]:
        try:
            p, s, c = entire_bigraph(line, regex)
            all_occupancies[p, s] = c

            if read_short:
                p, s, c = old_spanning_tree(line, regex)
                old_occupancies[p, s] = c

                p, s, c = minimum_spanning_solution(line, regex)
                mst_occupancies[p, s] = c

        except re.error as e:
            read_short = False

    print("done")

    plot(old_occupancies, "Old Spanning Tree", "old.png")
    plot(mst_occupancies, "MST Occupancies (new)", "mst.png")
    plot(all_occupancies, "All Combinations", "all.png")

    # Also plot histograms of occupancies
    kw = {"bins": np.logspace(-1, 6, 25), "alpha": 0.4}
    plt.hist(all_occupancies.flatten(), **kw, label="all", color="r")
    plt.hist(mst_occupancies.flatten(), **kw, label="mst", color="k")
    kw["histtype"] = "step"
    plt.hist(old_occupancies.flatten(), **kw, label="old", color="b")
    plt.legend()
    plt.xscale("log")
    plt.title("Number of mirror pairs with a given occupancy")
    plt.text(
        0.05,
        9.5,
        "Can see that the MST\nhas selected the highest\noccupancy combinations, and has\ngenerally chosen higher occupancy\ncombinations than the old ST",
    )
    plt.xlabel("Occupancy")
    plt.ylabel("Number of Mirror pairs")
    plt.savefig("hists.png")


if __name__ == "__main__":
    main()
