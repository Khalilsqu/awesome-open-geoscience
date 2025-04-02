import sys
import json

def main():
    # Check we have at least 2 arguments beyond the script name
    if len(sys.argv) < 3:
        print("Usage: python scripts/json_to_readme.py awesome_open_geoscience.json scripts/order.txt")
        sys.exit(1)
    
    json_file = sys.argv[1]
    order_file = sys.argv[2]
    
    # Load JSON data
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Load order.txt and build ordered structure
    order = []
    with open(order_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            if line.strip():
                indent = len(line) - len(line.lstrip())
                if indent == 0:
                    order.append({'category': line.strip(), 'subcategories': []})
                else:
                    order[-1]['subcategories'].append(line.strip())
    
    # Start creating README.md content
    readme = [
"""# Awesome Open Geoscience
> Geoscience is [awesome](awesome.md).

[![Awesome](https://raw.githubusercontent.com/softwareunderground/awesome-open-geoscience/master/media/icon/badge.svg)](https://github.com/sindresorhus/awesome) [![.github/workflows/link_checker.yml](https://github.com/softwareunderground/awesome-open-geoscience/actions/workflows/link_checker.yml/badge.svg)](https://github.com/softwareunderground/awesome-open-geoscience/actions/workflows/link_checker.yml) [![Contributions](https://img.shields.io/github/issues-pr-closed-raw/softwareunderground/awesome-open-geoscience.svg?label=contributions)](https://github.com/softwareunderground/awesome-open-geoscience/pulls) [![Commits](https://img.shields.io/github/last-commit/softwareunderground/awesome-open-geoscience.svg?label=last%20contribution)](https://github.com/softwareunderground/awesome-open-geoscience/commits/main) [![Chat on slack](https://img.shields.io/badge/slack-join-ff69b4.svg)](https://swung.slack.com/join/shared_invite/enQtNTczNjM4ODMxODMwLTQ3Yjk3MjFmOTJkYzUyZDU3OGI3ZmJhMzIyNzQxYjcyZDM5MWU4OTVmNTBiOTM4Zjg1ZDViOGM3NmQ4OTgzOTk) [![License](https://img.shields.io/github/license/softwareunderground/awesome-open-geoscience.svg)](https://github.com/softwareunderground/awesome-open-geoscience/blob/master/LICENSE)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.8354180.svg)](https://zenodo.org/records/8354180)

Open geoscience is even more awesome, so we made a list. This list is curated from repositories that make our lives as geoscientists, hackers and data wranglers easier or just more awesome. In accordance with the awesome manifesto, we add awesome repositories. We are open to [contributions](contributing.md) of course, this is a community effort after all.
If you are interested in being a maintainer of this repository, leave the [maintainer role](/maintainerRole.md) file.

## Contents
"""
    ]
    
    # Generate Table of Contents
    for item in order:
        cat_link = item['category'].replace(' ', '-').replace('&', '').lower()
        readme.append(f'- [{item["category"]}](#{cat_link})')
        for sub in item['subcategories']:
            sub_link = sub.replace(' ', '-').replace('&', '').lower()
            readme.append(f'  - [{sub}](#{sub_link})')
    
    readme.append('- [How to Contribute](#how-to-contribute)')
    readme.append('\n---\n')
    
    # Generate content sections with correct Top placement
    for item in order:
        category = item['category']
        readme.append(f'## {category}\n')
        
        if category == "Software":
            readme.append("Awesome software projects sub-categorized by focus.\n")

        if item['subcategories']:
            for subcategory in item['subcategories']:
                readme.append(f'### {subcategory}\n')
                entries = [e for e in data if e['category'] == category and e['subcategory'] == subcategory]
                for entry in sorted(entries, key=lambda x: x['name'].lower()):
                    readme.append(f"- [{entry['name']}]({entry['url']}) – {entry['description']}")
                readme.append('')
        else:
            entries = [e for e in data if e['category'] == category and e['subcategory'] is None]
            for entry in sorted(entries, key=lambda x: x['name'].lower()):
                readme.append(f"- [{entry['name']}]({entry['url']}) – {entry['description']}")
            readme.append('')
    
        # Add Top link once after the entire category
        readme.append('| ▲ [Top](#awesome-open-geoscience) |\n| --- |\n')
    
    # Additional sections
    readme.append(
"""
## How to Contribute

Contributions welcome! Read the [contribution guidelines](contributing.md) first.

| ▲ [Top](#awesome-open-geoscience) |\n| --- |\n
## License

[![CC0](http://mirrors.creativecommons.org/presskit/buttons/88x31/svg/cc-zero.svg)](https://creativecommons.org/publicdomain/zero/1.0)

To the extent possible under law, all contributors have waived all copyright and
related or neighboring rights to this work.
"""
    )
    
    # Write to README.md
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write('\n'.join(readme))
    
    print("README.md has been regenerated successfully!")

if __name__ == "__main__":
    main()
