import argparse

class CustomArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        print(f"Error: {message}\n")
        self.print_help()
        exit(2)

def process_data(input_file, output_file, verbose, factor):
    """Dummy function to simulate some processing."""
    result = f"Processed {input_file} -> {output_file} with factor={factor}"
    if verbose:
        result += " [VERBOSE MODE]"
    return result

def parse_args(args=None):
    parser = CustomArgumentParser(
        description="Dummy CLI tool",
        epilog="Example usage:\n  python argparse_demo.py --input data.txt --output result.txt --factor 5 --verbose"
    )
    parser.add_argument("--input", "-i", required=True, help="Input file")
    parser.add_argument("--output", "-o", required=True, help="Output file")
    parser.add_argument("--factor", "-f", type=int, default=1, help="Processing factor")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")
    return parser.parse_args(args)

def main(args=None):
    args = parse_args(args)
    return process_data(args.input, args.output, args.verbose, args.factor)

if __name__ == "__main__":
    print(main())
# Example usage:
# python argparse_demo.py --input data.txt --output result.txt --factor 5 --verbose