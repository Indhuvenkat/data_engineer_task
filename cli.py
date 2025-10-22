import argparse
from .parser import process_directory, save_report

def main():
    parser = argparse.ArgumentParser(description="Parallel File Parser")
    parser.add_argument("--input-dir", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    report = process_directory(args.input_dir)
    save_report(report, args.output)
    print(f"✅ Report saved at {args.output}")

if __name__ == "__main__":
    main()
