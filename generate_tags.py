import os
import yaml
import glob
from datetime import datetime


def parse_markdown_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()
    parts = content.split('---')
    if len(parts) > 2:
        metadata = yaml.safe_load(parts[1])
        return metadata
    return None


def update_metadata(filepath, metadata):
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()
    parts = content.split('---')
    if len(parts) > 2:
        body = '---'.join(parts[2:])
    else:
        body = parts[0]
    updated_metadata = yaml.dump(metadata)
    new_content = f"---\n{updated_metadata}---\n{body}"
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(new_content)


def generate_tag_pages(posts, tags_dir):
    tag_posts = {}
    for post in posts:
        metadata = parse_markdown_file(post)
        if metadata:
            filename = os.path.basename(post)
            metadata['filename'] = filename
            for tag in metadata.get('tags', []):
                if tag not in tag_posts:
                    tag_posts[tag] = []
                tag_posts[tag].append(metadata)

    for tag, posts in tag_posts.items():
        with open(os.path.join(tags_dir, f"{tag}.md"), 'w', encoding='utf-8') as file:
            file.write(f"# {tag}\n\n")
            for post in posts:
                file.write(f"- [{post['title']}](../posts/{post['filename']})\n")


def update_post_timestamps(posts):
    for post in posts:
        metadata = parse_markdown_file(post)
        if metadata:
            current_time = datetime.now().strftime('%Y-%m-%d')
            if 'date' not in metadata:
                metadata['date'] = current_time
            metadata['updated'] = current_time
            metadata['filename'] = os.path.basename(post)
            update_metadata(post, metadata)


def main():
    posts_dir = './posts'
    tags_dir = './tags'

    if not os.path.exists(tags_dir):
        os.makedirs(tags_dir)

    posts = glob.glob(os.path.join(posts_dir, '*.md'))
    # update_post_timestamps(posts)
    generate_tag_pages(posts, tags_dir)


if __name__ == "__main__":
    main()
