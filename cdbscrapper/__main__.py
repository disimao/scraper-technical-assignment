import pathlib
import subprocess
import sys

if sys.stdin.isatty():
    raise Exception(
        (
            "Your command line is incorrect or input might be empty. "
            "Run with text file with newline-separated list of website URLs "
            "as: cat websites.txt | python -m cdbscrapper"
        )
    )

path = pathlib.Path(__file__)
cwd = path.parent.resolve()
urls = sys.stdin.read()

proc = subprocess.Popen(
    ["scrapy", "crawl", "cdbspider", "-a", f"start_urls={urls}"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    cwd=cwd,
)
output, err = proc.communicate()
sys.stdout.write(output.decode())
