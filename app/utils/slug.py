

def reverse_slugify(slug: str) -> str:
    return slug.replace("-", " ").title()
