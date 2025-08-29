import unittest
import subprocess
import sys
import io
from unittest.mock import patch
from contextlib import redirect_stdout
from demo_argparse import parse_args, process_data, main

class TestArgparseDemo(unittest.TestCase):

    def test_parse_args_required(self):
        args = parse_args(["-i", "input.txt", "-o", "output.txt"])
        self.assertEqual(args.input, "input.txt")
        self.assertEqual(args.output, "output.txt")
        self.assertEqual(args.factor, 1)
        self.assertFalse(args.verbose)

    def test_parse_args_with_all(self):
        args = parse_args(["-i", "in.csv", "-o", "out.csv", "-f", "5", "-v"])
        self.assertEqual(args.input, "in.csv")
        self.assertEqual(args.output, "out.csv")
        self.assertEqual(args.factor, 5)
        self.assertTrue(args.verbose)

    def test_process_data(self):
        result = process_data("a.txt", "b.txt", verbose=True, factor=3)
        self.assertIn("Processed a.txt -> b.txt with factor=3", result)
        self.assertIn("VERBOSE MODE", result)

    def test_main_function(self):
        result = main(["-i", "data.in", "-o", "data.out", "-f", "2"])
        self.assertEqual(result, "Processed data.in -> data.out with factor=2")

    def test_main_with_sys_argv(self):
        """Simulate CLI by mocking sys.argv"""
        test_argv = ["demo_argparse.py", "-i", "mock.in", "-o", "mock.out", "-f", "7", "-v"]
        with patch.object(sys, "argv", test_argv):
            result = main()
        self.assertEqual(result, "Processed mock.in -> mock.out with factor=7 [VERBOSE MODE]")

    def test_main_print_output(self):
        """Capture printed output from script-like behavior"""
        test_argv = ["demo_argparse.py", "-i", "print.in", "-o", "print.out", "-f", "3"]
        with patch.object(sys, "argv", test_argv):
            buf = io.StringIO()
            with redirect_stdout(buf):
                print(main())   # simulate `if __name__ == "__main__": print(main())`
            output = buf.getvalue().strip()
        self.assertEqual(output, "Processed print.in -> print.out with factor=3")

    def test_cli_subprocess(self):
        """Run the script as a real CLI call"""
        cmd = [sys.executable, "demo_argparse.py", "-i", "cli.in", "-o", "cli.out", "-f", "10", "-v"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        output = result.stdout + result.stderr   # combine both
        self.assertEqual(result.returncode, 0)
        self.assertIn("Processed cli.in -> cli.out with factor=10", output)
        self.assertIn("VERBOSE MODE", output)

    def test_cli_missing_required(self):
        """Check that missing required args triggers CustomArgumentParser.error"""
        cmd = [sys.executable, "demo_argparse.py", "-i", "cli.in"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        output = result.stdout + result.stderr   # combine both
        self.assertEqual(result.returncode, 2)
        self.assertIn("Error:", output)
        self.assertIn("usage:", output)


if __name__ == "__main__":
    unittest.main()


# Example usage:
# python -m unittest test_my_script.py  # or
# python test_my_script.py  # if __name__ == "__main__": block is present
# python argparse_demo.py --input data.txt --output result.txt --factor 5 --verbose # to see the script in action