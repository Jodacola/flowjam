import argparse


def get_arguments():
    parser = argparse.ArgumentParser(description="Flow Jam command line arguments")
    parser.add_argument(
        "-t",
        "--threshold",
        type=int,
        help="Number of events to trigger to reach the maximum level, within the falloff period; default is 300 events",
        default=300,
    )
    parser.add_argument(
        "-f",
        "--falloff",
        type=int,
        help="The number of minutes in the falloff period; default is 2 minutes",
        default=2,
    )
    parser.add_argument(
        "-j",
        "--jamspath",
        type=str,
        help="The path which is searched to find jam manifests; default is jam_library",
        default="jam_library",
    )

    args = parser.parse_args()
    return args


def validate_arguments(args):
    if args.threshold < 50:
        print(
            "⚠️  Warning: Threshold is very low. You may want to increase it, otherwise you'll reach the highest level of a flow jam very quickly.\n"
        )
    if args.threshold <= 0:
        print("Please enter a positive number for the threshold.")
        return False

    if args.falloff < 1:
        print(
            "⚠️ Warning: Falloff is very low. You may want to increase it, otherwise you may never get the full breadth of your flow jam.\n"
        )
    if args.falloff <= 0:
        print("Please enter a positive number for the falloff.")
        return False
    
    return True
