#!/usr/bin/env python3
"""
CNAMER - Simple & Beautiful CNAME Checker
A command-line tool to check which domains have CNAME records.
"""

import argparse
import sys
import os
from typing import List, Tuple, Optional

try:
    import dns.resolver
    from dns.exception import DNSException
except ImportError:
    print("\033[91m[!] dnspython is required. Install it with: pip install dnspython\033[0m")
    sys.exit(1)


# ANSI Colors
BLUE = "\033[94m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"
DIM = "\033[2m"


def print_banner():
    """Print a cool blue ASCII banner."""
    banner = f"""
{BLUE}{BOLD}
   ██████╗███╗   ██╗ █████╗ ███╗   ███╗███████╗██████╗ 
  ██╔════╝████╗  ██║██╔══██╗████╗ ████║██╔════╝██╔══██╗
  ██║     ██╔██╗ ██║███████║██╔████╔██║█████╗  ██████╔╝
  ██║     ██║╚██╗██║██╔══██║██║╚██╔╝██║██╔══╝  ██╔══██╗
  ╚██████╗██║ ╚████║██║  ██║██║ ╚═╝ ██║███████╗██║  ██║
   ╚═════╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝
{RESET}
{CYAN}          ★ CNAME Record Checker ★{RESET}
{DIM}              github.com/yourusername/cnamer{RESET}
"""
    print(banner)


def check_cname(domain: str) -> Tuple[bool, Optional[str]]:
    """
    Check if a domain has a CNAME record.
    Returns (has_cname, cname_target or None)
    """
    domain = domain.strip().lower()
    if not domain:
        return False, None

    # Remove protocol if present
    if domain.startswith(("http://", "https://")):
        domain = domain.split("://", 1)[1]
    domain = domain.rstrip("/")

    try:
        answers = dns.resolver.resolve(domain, "CNAME")
        for rdata in answers:
            target = str(rdata.target).rstrip(".")
            return True, target
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.NoNameservers):
        return False, None
    except DNSException:
        return False, None
    except Exception:
        return False, None

    return False, None


def process_domains(domains: List[str]) -> Tuple[List[str], List[str]]:
    """Process a list of domains and return (with_cname, without_cname)."""
    with_cname = []
    without_cname = []

    total = len(domains)
    for i, domain in enumerate(domains, 1):
        domain = domain.strip()
        if not domain or domain.startswith("#"):
            continue

        print(f"{DIM}[{i}/{total}] Checking {domain}...{RESET}", end="\r")

        has_cname, target = check_cname(domain)
        if has_cname and target:
            with_cname.append(f"{domain} (CNAME: {target})")
        else:
            without_cname.append(domain)

    # Clear the progress line
    print(" " * 60, end="\r")
    return with_cname, without_cname


def print_results(with_cname: List[str], without_cname: List[str], output_file: Optional[str] = None):
    """Print results to stdout and optionally to a file."""
    output_lines = []

    header_cname = "======================\n  CNAME:\n======================"
    header_no = "\n======================\n  no CNAME:\n======================"

    output_lines.append(header_cname)
    if with_cname:
        output_lines.extend(with_cname)
    else:
        output_lines.append("(none)")

    output_lines.append(header_no)
    if without_cname:
        output_lines.extend(without_cname)
    else:
        output_lines.append("(none)")

    result_text = "\n".join(output_lines)

    # Colored print to terminal
    print(f"\n{GREEN}{BOLD}======================{RESET}")
    print(f"{GREEN}{BOLD}  CNAME:{RESET}")
    print(f"{GREEN}{BOLD}======================{RESET}")
    if with_cname:
        for item in with_cname:
            print(f"{CYAN}{item}{RESET}")
    else:
        print(f"{DIM}(none){RESET}")

    print(f"\n{YELLOW}{BOLD}======================{RESET}")
    print(f"{YELLOW}{BOLD}  no CNAME:{RESET}")
    print(f"{YELLOW}{BOLD}======================{RESET}")
    if without_cname:
        for item in without_cname:
            print(f"{item}")
    else:
        print(f"{DIM}(none){RESET}")

    print()
    print(f"{GREEN}✓ Found {len(with_cname)} with CNAME | {len(without_cname)} without{RESET}")

    if output_file:
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(result_text + "\n")
            print(f"{BLUE}→ Results saved to: {output_file}{RESET}")
        except Exception as e:
            print(f"{RED}[!] Failed to write output file: {e}{RESET}")


def main():
    parser = argparse.ArgumentParser(
        prog="cnamer",
        description="CNAMER - Check which domains have CNAME records",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
{BOLD}Examples:{RESET}
  python cnamer.py -u example.com
  python cnamer.py -u www.github.com -o result.txt
  python cnamer.py -list domains.txt
  python cnamer.py -list subdomains.txt -o cname_results.txt

{DIM}Note: Requires dnspython (pip install dnspython){RESET}
        """
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-u", "--url",
        metavar="DOMAIN",
        help="Check a single domain"
    )
    group.add_argument(
        "-list", "--list",
        metavar="FILE",
        dest="list_file",
        help="File containing list of domains (one per line)"
    )

    parser.add_argument(
        "-o", "--output",
        metavar="FILE",
        help="Save results to a file"
    )

    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Suppress banner"
    )

    args = parser.parse_args()

    if not args.quiet:
        print_banner()

    domains = []

    if args.url:
        domains = [args.url]
    elif args.list_file:
        if not os.path.isfile(args.list_file):
            print(f"{RED}[!] File not found: {args.list_file}{RESET}")
            sys.exit(1)
        try:
            with open(args.list_file, "r", encoding="utf-8") as f:
                domains = [line.strip() for line in f if line.strip()]
        except Exception as e:
            print(f"{RED}[!] Error reading file: {e}{RESET}")
            sys.exit(1)

        if not domains:
            print(f"{YELLOW}[!] No domains found in the file.{RESET}")
            sys.exit(0)

    print(f"{CYAN}Scanning {len(domains)} domain(s)...{RESET}\n")

    with_cname, without_cname = process_domains(domains)
    print_results(with_cname, without_cname, args.output)


if __name__ == "__main__":
    main()
