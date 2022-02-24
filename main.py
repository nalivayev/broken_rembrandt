from checker import PathChecker, CheckerParser, CheckerLogger


def main():
    v_parser = CheckerParser()
    v_args = v_parser.parse_args()
    v_logger = CheckerLogger()
    v_checker = PathChecker()
    try:
        v_checker.do(v_logger, v_args.path, v_args.recursively)
    except Exception:
        v_logger.info(f"Unknown error")


if __name__ == "__main__":
    main()
