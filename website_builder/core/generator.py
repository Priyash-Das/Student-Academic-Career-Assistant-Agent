class WebsiteGenerator:
    def __init__(self, api_client):
        self.api_client = api_client
    def build_prompt(self, website_spec):
        return f"""
You are a senior front-end engineer and design systems architect known for producing award-quality, modern, animated websites.

Your task is to generate a COMPLETE, PRODUCTION-READY WEBSITE as a SINGLE, SELF-CONTAINED HTML FILE.

The result must look like it was designed by a top-tier product and design team (2024–2025 standards).

──────────────── OUTPUT RULES (STRICT) ────────────────
- Output ONLY valid HTML
- MUST start with <!DOCTYPE html>
- MUST include <html>, <head>, <body>, and closing tags
- ALL CSS must be inside <style>
- ALL JS must be inside <script>
- NO external libraries, fonts, images, SVGs, icons, CDNs
- NO markdown, explanations, comments, or truncation
- Any violation = INVALID OUTPUT

──────────────── LAYOUT REQUIREMENTS ────────────────
- <body> controls layout using Flexbox or Grid
- Center main UI vertically AND horizontally
- min-height: 100vh is REQUIRED
- Margin-based centering is FORBIDDEN
- Main UI must be inside a visually distinct container/card

──────────────── DESIGN QUALITY (CRITICAL) ────────────────
- Premium, modern, high-polish aesthetic
- Tasteful color palette (primary, accent, neutral)
- Strong contrast and accessibility
- Rounded corners, soft shadows, depth, hierarchy
- Clean system font stack
- Clear typography hierarchy (hero, headers, body, meta)
- No dull, default, or generic components

──────────────── INTERACTIONS & MOTION ────────────────
- All interactive elements MUST have hover, focus, and active states
- Smooth transitions and subtle animations (fade, slide, scale)
- Motion must feel intentional and refined (no gimmicks)

──────────────── RESPONSIVE DESIGN ────────────────
- Mobile-first CSS
- Fully usable on phone, tablet, and desktop
- No horizontal scrolling
- Touch-friendly spacing
- Media queries REQUIRED

──────────────── PAGE INTELLIGENCE ────────────────
- Forms: animated labels/placeholders, focus/error/success states
- Landing/Dashboard/Portfolio pages:
  - Strong hero
  - Clear visual sections
  - Consistent spacing and visual flow

──────────────── QUALITY BAR ────────────────
- No bland layouts
- No misalignment
- No weak or empty sections
- No excessive whitespace
- No lorem ipsum unless absolutely necessary

──────────────── INPUT ────────────────
WEBSITE TYPE:
{website_spec.site_type}

USER REQUEST:
{website_spec.description}

──────────────── FINAL CHECK (INTERNAL) ────────────────
Before output:
- Looks like a real premium product
- Visually rich, modern, animated
- Perfectly centered layout
- Valid, complete HTML
- Ends with </html>

Generate the final HTML now.
""".strip()
    def generate(self, website_spec):
        prompt = self.build_prompt(website_spec)
        result = self.api_client.generate(model=None, prompt=prompt)
        if "<body" in result:
            result = result.replace(
                "<body>",
                "<body style=\"margin:0;min-height:100vh;display:flex;align-items:center;justify-content:center;\">",
                1
            )
        return result