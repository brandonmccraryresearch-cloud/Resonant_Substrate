"""Command-line interface for IRH framework"""

import argparse

from .core import IRH_Framework


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Resonant Substrate: IRH Computational Framework"
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0"
    )
    parser.add_argument(
        "--resolution",
        type=int,
        default=50,
        help="Grid resolution for computations (default: 50)"
    )

    args = parser.parse_args()

    print("Initializing IRH Framework...")
    framework = IRH_Framework(grid_resolution=args.resolution)

    print(f"Framework initialized with grid resolution: {framework.grid_resolution}")
    print(f"Physical constants loaded: α_EM = {framework.constants.alpha_EM:.6f}")
    print("Use 'import irh' in Python to access the framework programmatically")


if __name__ == "__main__":
    main()
