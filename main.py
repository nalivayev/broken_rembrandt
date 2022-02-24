from checker import Checker, CheckerParser, CheckerLogger


def main():
    v_parser = CheckerParser()
    v_args = v_parser.parse_args()
    v_logger = CheckerLogger()
    v_marauder = MultiMarauder()
    try:
        v_marauder.do(v_logger, v_args.id, v_args.skip, v_args.count, v_args.groupcount, v_args.flowcount)
    except Exception:
        v_logger.info(f"Unknown error")


if __name__ == "__main__":
    main()
