import os
import re

seo_tags = """
  <meta name="description" content="XSTN is a performance-driven technology execution network building scalable digital products, enterprise websites, and powerful web applications.">
  <meta name="keywords" content="technology, scalable web applications, tech network, developers, internship, AI systems, SaaS, UI/UX">
  <meta name="author" content="Xplorevo Pvt Ltd">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
"""

def add_seo_to_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip if already has description meta tag
    if '<meta name="description"' in content:
        print(f"Skipping {os.path.basename(filepath)}, already has SEO tags.")
        return

    # Find the <title> tag and insert SEO tags right after it
    # We can use regex to find <title>.*?</title>
    match = re.search(r'(<title>.*?</title>)', content, re.IGNORECASE | re.DOTALL)
    if match:
        title_str = match.group(1)
        new_content = content.replace(title_str, title_str + seo_tags)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Added SEO tags to {os.path.basename(filepath)}")
    else:
        # If no <title>, try right before </head>
        match_head = re.search(r'(</head>)', content, re.IGNORECASE)
        if match_head:
            head_str = match_head.group(1)
            new_content = content.replace(head_str, seo_tags + head_str)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Added SEO tags right before </head> to {os.path.basename(filepath)}")
        else:
            print(f"Could not find <title> or </head> in {os.path.basename(filepath)}")

def main():
    frontend_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Don't add to admin itself if it doesn't need public SEO
    skip_files = ['admin.html']
    
    for filename in os.listdir(frontend_dir):
        if filename.endswith('.html') and filename not in skip_files:
            filepath = os.path.join(frontend_dir, filename)
            add_seo_to_file(filepath)

if __name__ == '__main__':
    main()
