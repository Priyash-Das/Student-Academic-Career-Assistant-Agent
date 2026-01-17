class WebsiteSpec:
    def __init__(self, site_type: str, description: str):
        self.site_type = site_type
        self.description = description
class WebsiteSpecInference:
    KEYWORDS = {
        "portfolio": ["portfolio", "developer", "designer", "personal site"],
        "business": ["company", "business", "corporate", "startup"],
        "landing": ["landing page", "marketing", "signup", "promotion"],
        "product": ["product", "showcase", "saas", "app"],
        "blog": ["blog", "articles", "posts", "writing"],
        "personal": ["personal", "about me", "profile"],
    }
    @classmethod
    def infer(cls, prompt: str) -> WebsiteSpec:
        prompt_lower = prompt.lower()

        for site_type, keywords in cls.KEYWORDS.items():
            for kw in keywords:
                if kw in prompt_lower:
                    return WebsiteSpec(site_type, prompt)
        return WebsiteSpec("generic", prompt)