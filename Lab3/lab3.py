# CIS-117 Lab3
# Read the CSV and save countries in different files by region.
# Keep only the country name and region.
# Name: Zhaochun Fu
# Partner / Group: None
# I worked on this lab without a class partner.

import csv
from pathlib import Path
import sys


def read_countries(input_file):
    # Read the countries and group them by region.
    regions = {}
    with open(input_file, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file, strict=True)
        if not reader.fieldnames:
            raise ValueError("The input CSV is empty or has no header.")

        # Find the name and region columns.
        headers = {name.strip().lower(): name for name in reader.fieldnames}
        country_column = next(
            (headers[name] for name in ("name", "country", "country name", "country_name")
             if name in headers), None
        )
        region_column = headers.get("region")
        if country_column is None or region_column is None:
            raise ValueError("The CSV must have a country name column and a region column.")

        for row in reader:
            if None in row or any(value is None for value in row.values()):
                raise ValueError(f"Incorrect number of columns near line {reader.line_num}.")
            country = row[country_column].strip()
            region = row[region_column].strip()
            if not country:
                raise ValueError(f"Missing country near line {reader.line_num}.")
            # Check if the region can be a file name.
            if any(char in region for char in '/\\:*?"<>|') or any(
                ord(char) < 32 for char in region
            ) or region.endswith("."):
                raise ValueError(f"Region cannot be used as a filename: {region!r}")
            regions.setdefault(region, []).append((country, region))

    if not regions:
        raise ValueError("The CSV contains no country records.")
    if len({(region or "Unspecified").casefold() for region in regions}) != len(regions):
        raise ValueError("Region filenames conflict; check the input.")
    return regions


def write_regions(regions, output_directory):
    # Make one file for each region.
    output_directory.mkdir(parents=True, exist_ok=True)
    for region, countries in sorted(regions.items()):
        # Antarctica has no region, so use Unspecified for its file name.
        output_file = output_directory / f"{region or 'Unspecified'}.csv"
        with open(output_file, "w", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Country", "Region"])
            writer.writerows(countries)
        print(f"Created {output_file.name}: {len(countries)} countries")


def main(input_file, output_directory):
    # Read and write the files, and handle errors.
    try:
        regions = read_countries(input_file)
        # Do not write over the input file.
        if any((output_directory / f"{region or 'Unspecified'}.csv").resolve() == input_file.resolve()
               for region in regions):
            raise ValueError("An output file would overwrite the input CSV.")
        write_regions(regions, output_directory)
    except FileNotFoundError as error:
        print(f"File not found: {error.filename}", file=sys.stderr)
    except PermissionError as error:
        print(f"Permission denied: {error.filename}", file=sys.stderr)
    except OSError as error:  # This also handles IOError.
        print(f"File input/output error: {error}", file=sys.stderr)
    except (csv.Error, UnicodeError, ValueError) as error:
        print(f"Invalid CSV data: {error}", file=sys.stderr)
    else:
        total = sum(len(countries) for countries in regions.values())
        print(f"Done: {total} countries in {len(regions)} region files.")
        return 0
    return 1


if __name__ == "__main__":
    folder = Path(__file__).resolve().parent
    source = Path(sys.argv[1]) if len(sys.argv) > 1 else folder / "country_full.csv"
    destination = Path(sys.argv[2]) if len(sys.argv) > 2 else folder / "region_files"
    sys.exit(main(source, destination))
