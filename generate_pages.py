#!/usr/bin/env python3
"""
Static Programmatic SEO Page Generator for SoarAI USA
=====================================================
Generates static HTML pages for all combinations of:
  4 services x 14 industries x 20 US cities = 1,120 landing pages
  + 4 browse pages (one per service)
  + sitemap.xml

Run:  python3 generate_pages.py
Output goes into the current directory as nested folders.
"""

import os
import json
from datetime import datetime

DOMAIN = "https://soaraiusa.com"
GA_ID = "G-SRZ8MY7SL6"  # Update if different for US site

# ---------------------------------------------------------------------------
# SERVICES
# ---------------------------------------------------------------------------

SERVICES = {
    'free-seo-audit': {
        'name': 'SEO/GEO Audit',
        'short': 'SEO audit',
        'verb': 'audit',
        'form_url': '/SEOAudit/seo-audit-form.html',
        'icon': '\U0001f50d',
        'color': '#2563EB',
        'benefits': [
            'Technical SEO health check across 50+ ranking factors',
            'GEO readiness scoring for AI search engines',
            'Mobile optimization and Core Web Vitals analysis',
            'Schema markup and structured data validation',
            'Actionable recommendations to improve rankings',
        ],
        'description': 'Comprehensive website analysis covering technical SEO, on-page content, performance, mobile optimization, and AI search readiness (GEO).',
        'how_it_helps': 'Our AI-powered crawler analyzes up to 10 pages of your website, scoring it across five key dimensions: Technical SEO, On-Page Content, Performance, Mobile Optimization, and GEO Readiness. You get an instant report with specific fixes ranked by impact.',
    },
    'free-keyword-research': {
        'name': 'Keyword Research & Strategy',
        'short': 'keyword research',
        'verb': 'research',
        'form_url': '/keyword-research-form.html',
        'icon': '\U0001f511',
        'color': '#059669',
        'benefits': [
            '10 AI-identified keyword opportunities',
            'Search intent classification (informational, commercial, transactional)',
            'SEO vs SEM channel recommendation per keyword',
            'Difficulty rating (Low, Medium, High)',
            'Recommended target page mapping',
        ],
        'description': 'AI-powered keyword discovery that identifies the most valuable search terms for your business, classified by intent, channel, and difficulty.',
        'how_it_helps': 'SoarAI crawls your website content and uses AI to identify 10 high-value keyword opportunities tailored to your industry and geography. Each keyword comes with intent classification, channel recommendation, and a page mapping strategy.',
    },
    'free-lpo-scorecard': {
        'name': 'Landing Page Optimization',
        'short': 'landing page audit',
        'verb': 'optimize',
        'form_url': '/lpo-scorecard-form.html',
        'icon': '\U0001f4c8',
        'color': '#7C3AED',
        'benefits': [
            'Conversion potential scoring across 10 dimensions',
            'Headline effectiveness and value proposition analysis',
            'Social proof and trust signal evaluation',
            'CTA design and placement recommendations',
            'Mobile optimization and page speed assessment',
        ],
        'description': "Analyze your landing page's conversion potential across 10 critical dimensions including headline effectiveness, CTA design, trust signals, and mobile readiness.",
        'how_it_helps': 'Our AI evaluates your landing page like a conversion rate optimization expert, scoring it across 10 dimensions from headline clarity to mobile UX. You receive a letter grade (A-F) plus the top 3 issues hurting your conversions, with specific fix recommendations.',
    },
    'free-ad-copy': {
        'name': 'Ad Copy Generator',
        'short': 'ad copy generation',
        'verb': 'generate',
        'form_url': '/AdCopy/ac-agent-form.html',
        'icon': '\u270d\ufe0f',
        'color': '#DC2626',
        'benefits': [
            'AI-generated Google Ads copy (headlines + descriptions)',
            'Multiple ad variations for A/B testing',
            'Industry-specific messaging and tone',
            'Keyword-optimized headlines under character limits',
            'Call-to-action best practices built in',
        ],
        'description': 'Generate high-converting Google Ads copy instantly using AI trained on thousands of successful ad campaigns across industries.',
        'how_it_helps': 'SoarAI analyzes your website and generates multiple Google Ads copy variations tailored to your industry. Each variation includes optimized headlines (under 30 characters) and descriptions (under 90 characters) with strong CTAs.',
    },
}

# ---------------------------------------------------------------------------
# INDUSTRIES (14)
# ---------------------------------------------------------------------------

INDUSTRIES = {
    'ecommerce': {
        'name': 'E-commerce',
        'pain_points': [
            'Low organic visibility for product pages in a crowded online marketplace',
            'High cart abandonment rates due to poor landing page experience',
            'Difficulty competing with Amazon, Shopify stores, and large DTC brands',
            'Ineffective paid ad spend with declining ROAS across Google and Meta',
            'Lack of local SEO presence for city-specific product searches',
        ],
        'keywords': ['online store', 'product listing', 'shopping cart', 'buy online'],
        'context': 'online retail and direct-to-consumer sales',
    },
    'healthcare': {
        'name': 'Healthcare',
        'pain_points': [
            'Low visibility in "doctor near me" and "clinic near me" local searches',
            'HIPAA compliance constraints limiting digital marketing strategies',
            'Poor Google Business Profile optimization leading to lost patient appointments',
            'Competitors outranking for high-intent health-related search terms',
            'Lack of structured data making practice information invisible to AI search',
        ],
        'keywords': ['hospital', 'clinic', 'doctor', 'healthcare provider', 'patient care'],
        'context': 'hospitals, clinics, and healthcare providers',
    },
    'real-estate': {
        'name': 'Real Estate',
        'pain_points': [
            'Property listings not appearing in local search results',
            'Difficulty capturing buyer intent at the research stage',
            'High competition for "homes for sale in [city]" keywords from Zillow and Redfin',
            'Landing pages failing to convert property inquiries into showings',
            'Low engagement on paid ads due to generic ad copy',
        ],
        'keywords': ['property', 'homes for sale', 'real estate agent', 'realtor'],
        'context': 'real estate agencies, brokerages, and property developers',
    },
    'education': {
        'name': 'Education',
        'pain_points': [
            'Difficulty ranking for "best programs in [city]" searches',
            'Low conversion rates on course and enrollment landing pages',
            'Students comparing multiple institutions before applying',
            'Ineffective digital ad campaigns during enrollment season',
            'Poor visibility in AI-powered education recommendation searches',
        ],
        'keywords': ['university', 'college', 'courses', 'training', 'online learning'],
        'context': 'universities, colleges, trade schools, and ed-tech platforms',
    },
    'saas': {
        'name': 'SaaS & Technology',
        'pain_points': [
            'Long sales cycles making paid acquisition expensive',
            'Difficulty ranking for competitive software category keywords',
            'Landing pages failing to communicate complex product value propositions',
            'Low free trial or demo conversion rates from organic traffic',
            'Content marketing not generating enough qualified leads',
        ],
        'keywords': ['software', 'platform', 'SaaS', 'cloud', 'app', 'tool'],
        'context': 'software companies, tech startups, and SaaS platforms',
    },
    'professional-services': {
        'name': 'Professional Services',
        'pain_points': [
            'Low visibility for "best [service] consultant in [city]" searches',
            'Difficulty differentiating from competitors in a trust-based industry',
            'Landing pages not converting visitors into consultation bookings',
            'Reliance on referrals with no scalable digital lead generation',
            'Poor Google Business Profile and local pack presence',
        ],
        'keywords': ['consultant', 'advisor', 'agency', 'firm', 'consulting'],
        'context': 'consulting firms, agencies, accountants, and professional advisors',
    },
    'hospitality': {
        'name': 'Hospitality & Travel',
        'pain_points': [
            'Over-dependence on OTAs (Expedia, Booking.com) for bookings',
            'Poor direct website visibility in "hotel in [city]" searches',
            'Landing pages not compelling enough to drive direct bookings',
            'Seasonal demand making paid ad budgets unpredictable',
            'Difficulty showcasing unique property experiences in search snippets',
        ],
        'keywords': ['hotel', 'resort', 'travel', 'booking', 'tourism', 'stay'],
        'context': 'hotels, resorts, travel agencies, and tourism operators',
    },
    'retail': {
        'name': 'Retail',
        'pain_points': [
            'Low foot traffic from "store near me" and local search queries',
            'Online-offline gap with no integrated digital marketing strategy',
            'Difficulty competing with e-commerce giants for product searches',
            'Ineffective local advertising with poor geo-targeting',
            'Landing pages not driving in-store visit conversions',
        ],
        'keywords': ['store', 'shop', 'retail', 'buy', 'showroom'],
        'context': 'brick-and-mortar retail stores and omni-channel retailers',
    },
    'manufacturing': {
        'name': 'Manufacturing',
        'pain_points': [
            'Invisible online presence despite strong offline reputation',
            'Difficulty reaching B2B buyers searching for suppliers online',
            'Website not optimized for industry-specific technical searches',
            'No content strategy to capture procurement decision-maker searches',
            'Poor structured data making products invisible in B2B search engines',
        ],
        'keywords': ['manufacturer', 'supplier', 'factory', 'OEM', 'industrial'],
        'context': 'manufacturers, industrial suppliers, and B2B producers',
    },
    'automotive': {
        'name': 'Automotive',
        'pain_points': [
            'Low visibility for "car dealer near me" and brand-specific searches',
            'Difficulty competing with AutoTrader, Cars.com, and CarGurus',
            'Landing pages not driving test drive bookings or inquiries',
            'Ineffective paid ads with high cost-per-lead in a competitive market',
            'Poor Google Maps and local pack presence for dealerships',
        ],
        'keywords': ['car dealer', 'auto', 'vehicle', 'dealership', 'test drive'],
        'context': 'car dealerships, auto service centers, and vehicle manufacturers',
    },
    'finance': {
        'name': 'Finance & Insurance',
        'pain_points': [
            'Strict regulatory requirements making digital marketing complex',
            'Low trust signals on landing pages for financial products',
            'High competition for "best loan/insurance" keywords from aggregators like NerdWallet',
            'Difficulty reaching local customers searching for financial advisors',
            'Poor content strategy for high-intent financial planning searches',
        ],
        'keywords': ['loan', 'insurance', 'investment', 'financial advisor', 'banking'],
        'context': 'banks, insurance companies, fintech firms, and financial advisors',
    },
    'legal': {
        'name': 'Legal Services',
        'pain_points': [
            'Low visibility for "lawyer near me" and practice-area searches',
            'Difficulty building trust and credibility through digital presence',
            'Landing pages not converting visitors into consultation requests',
            'Competitors investing heavily in Google Ads for legal keywords ($50-200+ CPC)',
            'No strategy for capturing informational legal queries that lead to clients',
        ],
        'keywords': ['lawyer', 'attorney', 'legal services', 'law firm'],
        'context': 'law firms, solo practitioners, and corporate legal departments',
    },
    'food-beverage': {
        'name': 'Food & Beverage',
        'pain_points': [
            'Heavy dependence on DoorDash, UberEats, and Grubhub for orders',
            'Poor Google Maps presence for "restaurant near me" searches',
            'Landing pages not driving direct online orders or reservations',
            'Difficulty ranking for cuisine-specific and location-based food searches',
            'Ineffective social media to website conversion funnel',
        ],
        'keywords': ['restaurant', 'cafe', 'food delivery', 'catering', 'bakery'],
        'context': 'restaurants, cafes, ghost kitchens, and food delivery businesses',
    },
    'nonprofit': {
        'name': 'Non-Profit',
        'pain_points': [
            'Limited marketing budget making organic visibility critical',
            'Difficulty reaching potential donors and volunteers through search',
            'Landing pages not compelling enough to drive donations',
            'Low awareness of Google Ad Grants ($10K/month free advertising)',
            'Poor structured data making cause-related content invisible to AI search',
        ],
        'keywords': ['nonprofit', 'charity', 'donate', 'volunteer', 'foundation'],
        'context': 'nonprofits, charities, foundations, and social enterprises',
    },
}

# ---------------------------------------------------------------------------
# US CITIES (20)
# ---------------------------------------------------------------------------

CITIES = {
    'new-york': {'name': 'New York', 'state': 'New York', 'tier': 1, 'region': 'Northeast',
                 'context': "The largest city in the US and a global business capital. With millions of businesses competing for attention, digital visibility is make-or-break in the New York metro area."},
    'san-francisco': {'name': 'San Francisco', 'state': 'California', 'tier': 1, 'region': 'West',
                      'context': "The heart of Silicon Valley and America's tech capital. San Francisco businesses operate in one of the most digitally sophisticated and competitive markets in the world."},
    'los-angeles': {'name': 'Los Angeles', 'state': 'California', 'tier': 1, 'region': 'West',
                    'context': "America's second-largest city and the entertainment capital of the world. LA's diverse economy spans media, tech, healthcare, and retail — all fiercely competitive online."},
    'austin': {'name': 'Austin', 'state': 'Texas', 'tier': 1, 'region': 'South',
               'context': "One of America's fastest-growing tech hubs. Austin's booming startup scene and rapid population growth make digital marketing essential for businesses trying to stand out."},
    'chicago': {'name': 'Chicago', 'state': 'Illinois', 'tier': 1, 'region': 'Midwest',
                'context': "America's third-largest city and a major business hub for finance, manufacturing, and professional services. Chicago businesses face intense competition in both local and national search."},
    'miami': {'name': 'Miami', 'state': 'Florida', 'tier': 1, 'region': 'South',
              'context': "A booming international business hub and gateway to Latin America. Miami's real estate, hospitality, and finance sectors are among the most competitive for online visibility."},
    'seattle': {'name': 'Seattle', 'state': 'Washington', 'tier': 1, 'region': 'West',
                'context': "Home to Amazon, Microsoft, and a thriving tech ecosystem. Seattle businesses compete in one of America's most digitally advanced markets."},
    'dallas': {'name': 'Dallas', 'state': 'Texas', 'tier': 1, 'region': 'South',
               'context': "A major business hub in the heart of Texas with a diverse economy spanning finance, healthcare, tech, and retail. The DFW metroplex is one of America's fastest-growing markets."},
    'boston': {'name': 'Boston', 'state': 'Massachusetts', 'tier': 1, 'region': 'Northeast',
              'context': "A leading hub for healthcare, biotech, education, and finance. Boston's highly educated consumer base and competitive business landscape demand strong digital presence."},
    'denver': {'name': 'Denver', 'state': 'Colorado', 'tier': 1, 'region': 'West',
               'context': "One of America's fastest-growing cities with a booming tech and outdoor lifestyle economy. Denver businesses are rapidly investing in digital marketing to capture growth."},
    'atlanta': {'name': 'Atlanta', 'state': 'Georgia', 'tier': 1, 'region': 'South',
                'context': "The economic capital of the Southeast and a major logistics, media, and fintech hub. Atlanta's rapid growth makes digital marketing critical for businesses of all sizes."},
    'phoenix': {'name': 'Phoenix', 'state': 'Arizona', 'tier': 1, 'region': 'West',
                'context': "One of America's fastest-growing metros with a booming real estate, healthcare, and tech sector. Phoenix businesses face increasing competition as the market expands."},
    'houston': {'name': 'Houston', 'state': 'Texas', 'tier': 1, 'region': 'South',
                'context': "America's fourth-largest city and the energy capital of the world. Houston's diverse economy spans oil and gas, healthcare, manufacturing, and a growing tech scene."},
    'san-diego': {'name': 'San Diego', 'state': 'California', 'tier': 2, 'region': 'West',
                  'context': "A major biotech, defense, and tourism hub on the California coast. San Diego's competitive business landscape requires strong digital presence to capture local and national demand."},
    'nashville': {'name': 'Nashville', 'state': 'Tennessee', 'tier': 2, 'region': 'South',
                  'context': "One of America's hottest markets for healthcare, music, hospitality, and tech startups. Nashville's explosive growth means businesses must invest in digital visibility to compete."},
    'portland': {'name': 'Portland', 'state': 'Oregon', 'tier': 2, 'region': 'West',
                 'context': "A hub for creative industries, food and beverage, and sustainable business. Portland's tech-savvy, brand-conscious consumers make digital marketing essential."},
    'charlotte': {'name': 'Charlotte', 'state': 'North Carolina', 'tier': 2, 'region': 'South',
                  'context': "America's second-largest banking center and a rapidly growing business hub. Charlotte's finance, healthcare, and tech sectors drive fierce competition for online visibility."},
    'minneapolis': {'name': 'Minneapolis', 'state': 'Minnesota', 'tier': 2, 'region': 'Midwest',
                    'context': "Home to 16 Fortune 500 companies and a thriving startup ecosystem. Minneapolis businesses compete in a sophisticated market that demands strong digital presence."},
    'raleigh': {'name': 'Raleigh', 'state': 'North Carolina', 'tier': 2, 'region': 'South',
                'context': "Part of the Research Triangle, one of America's top tech and biotech corridors. Raleigh's educated workforce and growing business community make digital marketing essential."},
    'salt-lake-city': {'name': 'Salt Lake City', 'state': 'Utah', 'tier': 2, 'region': 'West',
                       'context': "The heart of the Silicon Slopes tech boom. Salt Lake City's rapidly growing SaaS and outdoor industry ecosystem demands strong digital visibility to compete."},
}


# ---------------------------------------------------------------------------
# CONTENT GENERATION
# ---------------------------------------------------------------------------

def generate_page_content(service_key, industry_key, city_key):
    svc = SERVICES[service_key]
    ind = INDUSTRIES[industry_key]
    cty = CITIES[city_key]

    service_name = svc['name']
    service_short = svc['short']
    industry_name = ind['name']
    city_name = cty['name']
    state = cty['state']

    title = f"Free {service_name} for {industry_name} in {city_name} | SoarAI"
    meta_description = (
        f"Get a free {service_short} for your {industry_name.lower()} business in {city_name}, {state}. "
        f"AI-powered analysis with instant results. No signup required."
    )
    h1 = f"Free {service_name} for {industry_name} Businesses in {city_name}"

    intro = (
        f"Running a {industry_name.lower()} business in {city_name} means competing for attention "
        f"in one of America's most dynamic markets. {cty['context']} "
        f"SoarAI's free {service_short} tool helps {industry_name.lower()} businesses in {city_name} "
        f"gain a competitive edge by providing {svc['description'].lower()}"
    )

    pain_points_heading = f"Why {industry_name} Businesses in {city_name} Need {service_name}"
    pain_points = ind['pain_points']

    city_heading = f"The {city_name} Digital Marketing Landscape"
    city_context = (
        f"{city_name} is home to thousands of {industry_name.lower()} businesses competing for customers online. "
        f"{cty['context']} "
        f"With the US digital advertising market exceeding $300 billion, "
        f"having a strong digital presence is no longer optional for {city_name} businesses — it's essential. "
        f"A {service_short} gives you the data-driven insights you need to stand out."
    )

    how_heading = f"How SoarAI's {service_name} Works for {industry_name}"
    how_content = svc['how_it_helps']
    benefits = svc['benefits']

    cta_text = f"Get Your Free {service_name} Now"
    cta_url = svc['form_url']

    related_services = []
    for sk, sv in SERVICES.items():
        if sk != service_key:
            related_services.append({
                'url': f"/{sk}/{industry_key}/{city_key}",
                'short': sv['name'],
            })

    related_cities = get_related_cities(city_key, service_key, industry_key, limit=10)
    related_industries = get_related_industries(industry_key, service_key, city_key, limit=5)

    schema = {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": f"Free {service_name} for {industry_name} in {city_name}",
        "description": meta_description,
        "provider": {
            "@type": "Organization",
            "name": "SoarAI",
            "url": DOMAIN,
        },
        "areaServed": {
            "@type": "City",
            "name": city_name,
            "containedInPlace": {
                "@type": "State",
                "name": state,
                "containedInPlace": {"@type": "Country", "name": "United States"}
            }
        },
        "serviceType": service_name,
        "audience": {
            "@type": "Audience",
            "audienceType": f"{industry_name} businesses"
        },
        "isAccessibleForFree": True,
    }

    canonical = f"{DOMAIN}/{service_key}/{industry_key}/{city_key}"

    return {
        'title': title, 'meta_description': meta_description, 'h1': h1,
        'intro': intro, 'pain_points_heading': pain_points_heading,
        'pain_points': pain_points, 'city_heading': city_heading,
        'city_context': city_context, 'how_heading': how_heading,
        'how_content': how_content, 'benefits': benefits,
        'cta_text': cta_text, 'cta_url': cta_url,
        'related_services': related_services, 'related_cities': related_cities,
        'related_industries': related_industries, 'schema': schema,
        'canonical': canonical, 'service_key': service_key,
        'industry_key': industry_key, 'city_key': city_key,
        'service': svc, 'industry': ind, 'city': cty,
    }


def get_related_cities(current_city, service_key, industry_key, limit=10):
    current = CITIES[current_city]
    same_region = []
    other = []
    for ckey, cdata in CITIES.items():
        if ckey == current_city:
            continue
        entry = {'key': ckey, 'name': cdata['name'], 'url': f"/{service_key}/{industry_key}/{ckey}"}
        if cdata['region'] == current['region']:
            same_region.append(entry)
        else:
            other.append(entry)
    result = same_region[:limit]
    remaining = limit - len(result)
    if remaining > 0:
        result.extend(other[:remaining])
    return result


def get_related_industries(current_industry, service_key, city_key, limit=5):
    result = []
    for ikey, idata in INDUSTRIES.items():
        if ikey == current_industry:
            continue
        result.append({'key': ikey, 'name': idata['name'], 'url': f"/{service_key}/{ikey}/{city_key}"})
        if len(result) >= limit:
            break
    return result


# ---------------------------------------------------------------------------
# HTML TEMPLATE
# ---------------------------------------------------------------------------

def render_landing_page(c):
    """Render a complete HTML page from content dict."""
    pain_points_html = '\n'.join(f'                <li>{p}</li>' for p in c['pain_points'])
    benefits_html = '\n'.join(
        f'                <div class="benefit-card"><span class="check">&#10003;</span><p>{b}</p></div>'
        for b in c['benefits']
    )
    related_services_html = '\n'.join(
        f'                    <a href="{rs["url"]}">{rs["short"]}</a>' for rs in c['related_services']
    )
    related_cities_html = '\n'.join(
        f'                    <a href="{rc["url"]}">{rc["name"]}</a>' for rc in c['related_cities']
    )
    related_industries_html = '\n'.join(
        f'                    <a href="{ri["url"]}">{ri["name"]}</a>' for ri in c['related_industries']
    )

    svc_color = c['service']['color']
    year = datetime.now().year

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{c['title']}</title>
    <meta name="description" content="{c['meta_description']}">
    <link rel="canonical" href="{c['canonical']}">
    <meta property="og:title" content="{c['title']}">
    <meta property="og:description" content="{c['meta_description']}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{c['canonical']}">
    <meta property="og:site_name" content="SoarAI">
    <script type="application/ld+json">{json.dumps(c['schema'])}</script>
    <script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', '{GA_ID}');
        gtag('event', 'view_programmatic_page', {{
            service: '{c["service_key"]}',
            industry: '{c["industry_key"]}',
            city: '{c["city_key"]}'
        }});
    </script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; color: #1f2937; line-height: 1.7; background: #f9fafb; }}
        .navbar {{ background: #fff; border-bottom: 1px solid #e5e7eb; padding: 16px 24px; display: flex; align-items: center; justify-content: space-between; position: sticky; top: 0; z-index: 100; }}
        .navbar a.logo {{ font-size: 22px; font-weight: 800; text-decoration: none; color: #1B3A5C; }}
        .navbar a.logo span {{ color: #2563EB; }}
        .nav-links {{ display: flex; gap: 20px; align-items: center; }}
        .nav-links a {{ text-decoration: none; color: #4b5563; font-size: 14px; font-weight: 500; transition: color 0.2s; }}
        .nav-links a:hover {{ color: #2563EB; }}
        .nav-links .btn-nav {{ background: #2563EB; color: #fff; padding: 8px 18px; border-radius: 6px; font-weight: 600; }}
        .nav-links .btn-nav:hover {{ background: #1d4ed8; color: #fff; }}
        .hero {{ background: linear-gradient(135deg, #1B3A5C 0%, #2563EB 100%); color: #fff; padding: 80px 24px 60px; text-align: center; }}
        .hero h1 {{ font-size: 2.4rem; font-weight: 800; max-width: 800px; margin: 0 auto 20px; line-height: 1.2; }}
        .hero p {{ font-size: 1.1rem; max-width: 700px; margin: 0 auto 32px; opacity: 0.92; line-height: 1.7; }}
        .hero .btn-cta {{ display: inline-block; background: #fff; color: #1B3A5C; padding: 14px 36px; border-radius: 8px; font-size: 1.05rem; font-weight: 700; text-decoration: none; transition: transform 0.2s, box-shadow 0.2s; }}
        .hero .btn-cta:hover {{ transform: translateY(-2px); box-shadow: 0 8px 20px rgba(0,0,0,0.2); }}
        .container {{ max-width: 900px; margin: 0 auto; padding: 0 24px; }}
        section {{ padding: 50px 0; }}
        section h2 {{ font-size: 1.6rem; font-weight: 700; color: #1B3A5C; margin-bottom: 20px; }}
        section p {{ font-size: 1rem; color: #374151; margin-bottom: 16px; }}
        .pain-points ul {{ list-style: none; padding: 0; }}
        .pain-points li {{ position: relative; padding: 14px 20px 14px 48px; margin-bottom: 10px; background: #fff; border-radius: 8px; border-left: 4px solid #ef4444; box-shadow: 0 1px 3px rgba(0,0,0,0.06); font-size: 0.95rem; color: #374151; }}
        .pain-points li::before {{ content: '\\26A0'; position: absolute; left: 16px; top: 14px; font-size: 1.1rem; }}
        .benefits-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 16px; margin-top: 20px; }}
        .benefit-card {{ background: #fff; border-radius: 10px; padding: 20px; border: 1px solid #e5e7eb; display: flex; align-items: flex-start; gap: 12px; }}
        .benefit-card .check {{ color: #059669; font-size: 1.3rem; flex-shrink: 0; margin-top: 2px; }}
        .benefit-card p {{ font-size: 0.92rem; color: #374151; margin: 0; }}
        .city-context {{ background: #eff6ff; border-radius: 12px; padding: 30px; margin: 10px 0; }}
        .city-context h2 {{ color: #1B3A5C; }}
        .cta-section {{ text-align: center; background: linear-gradient(135deg, {svc_color}22, {svc_color}11); border-radius: 16px; padding: 48px 32px; margin: 20px 0; }}
        .cta-section h2 {{ color: #1B3A5C; margin-bottom: 12px; }}
        .cta-section p {{ max-width: 500px; margin: 0 auto 24px; color: #4b5563; }}
        .cta-section .btn-primary {{ display: inline-block; background: {svc_color}; color: #fff; padding: 16px 40px; border-radius: 8px; font-size: 1.1rem; font-weight: 700; text-decoration: none; transition: transform 0.2s, box-shadow 0.2s; }}
        .cta-section .btn-primary:hover {{ transform: translateY(-2px); box-shadow: 0 8px 20px rgba(0,0,0,0.15); }}
        .internal-links {{ background: #fff; border-radius: 12px; padding: 36px; border: 1px solid #e5e7eb; }}
        .internal-links h3 {{ font-size: 1.1rem; font-weight: 700; color: #1B3A5C; margin: 24px 0 12px; }}
        .internal-links h3:first-child {{ margin-top: 0; }}
        .link-grid {{ display: flex; flex-wrap: wrap; gap: 8px; }}
        .link-grid a {{ display: inline-block; padding: 6px 14px; background: #f3f4f6; color: #2563EB; border-radius: 6px; font-size: 0.85rem; text-decoration: none; transition: background 0.2s; }}
        .link-grid a:hover {{ background: #dbeafe; }}
        .footer {{ background: #1B3A5C; color: #fff; text-align: center; padding: 36px 24px; margin-top: 40px; }}
        .footer p {{ color: rgba(255,255,255,0.8); font-size: 0.85rem; margin-bottom: 8px; }}
        .footer a {{ color: #93c5fd; text-decoration: none; }}
        .footer a:hover {{ text-decoration: underline; }}
        @media (max-width: 768px) {{
            .hero h1 {{ font-size: 1.8rem; }}
            .hero {{ padding: 60px 20px 40px; }}
            .navbar {{ padding: 12px 16px; }}
            .nav-links a:not(.btn-nav) {{ display: none; }}
            .benefits-grid {{ grid-template-columns: 1fr; }}
            .internal-links {{ padding: 24px; }}
        }}
        @media (max-width: 480px) {{
            .hero h1 {{ font-size: 1.5rem; }}
            .hero .btn-cta {{ padding: 12px 28px; font-size: 0.95rem; }}
            section h2 {{ font-size: 1.3rem; }}
        }}
    </style>
</head>
<body>
    <nav class="navbar">
        <a href="/" class="logo">Soar<span>AI</span></a>
        <div class="nav-links">
            <a href="/">Home</a>
            <a href="/SEOAudit/seo-audit-form.html">SEO Audit</a>
            <a href="/keyword-research-form.html">Keywords</a>
            <a href="/lpo-scorecard-form.html">LPO</a>
            <a href="{c['cta_url']}" class="btn-nav">{c['service']['short'].capitalize()} &rarr;</a>
        </div>
    </nav>
    <header class="hero">
        <h1>{c['h1']}</h1>
        <p>{c['intro']}</p>
        <a href="{c['cta_url']}" class="btn-cta">{c['cta_text']}</a>
    </header>
    <div class="container">
        <section class="pain-points">
            <h2>{c['pain_points_heading']}</h2>
            <p>If any of these challenges sound familiar, you're not alone. Here are the top digital marketing obstacles facing {c['industry']['name'].lower()} businesses in {c['city']['name']}:</p>
            <ul>
{pain_points_html}
            </ul>
        </section>
        <section>
            <div class="city-context">
                <h2>{c['city_heading']}</h2>
                <p>{c['city_context']}</p>
            </div>
        </section>
        <section>
            <h2>{c['how_heading']}</h2>
            <p>{c['how_content']}</p>
            <div class="benefits-grid">
{benefits_html}
            </div>
        </section>
        <section>
            <div class="cta-section">
                <h2>Ready to Outrank Your {c['city']['name']} Competitors?</h2>
                <p>Get your free {c['service']['short']} in under 60 seconds. No signup. No credit card. Just actionable insights.</p>
                <a href="{c['cta_url']}" class="btn-primary">{c['cta_text']}</a>
            </div>
        </section>
        <section>
            <div class="internal-links">
                <h3>Other SoarAI Tools for {c['industry']['name']} in {c['city']['name']}</h3>
                <div class="link-grid">
{related_services_html}
                </div>
                <h3>{c['service']['name']} in Other Cities</h3>
                <div class="link-grid">
{related_cities_html}
                </div>
                <h3>{c['service']['name']} for Other Industries in {c['city']['name']}</h3>
                <div class="link-grid">
{related_industries_html}
                </div>
            </div>
        </section>
    </div>
    <footer class="footer">
        <p><a href="{DOMAIN}">SoarAI</a> &mdash; AI-Powered Growth Agency</p>
        <p>&copy; {year} SoarAI. All rights reserved.</p>
        <p style="margin-top:12px;font-size:0.8rem;opacity:0.6;">Free AI-powered marketing tools for {c['industry']['name'].lower()} businesses in {c['city']['name']}, {c['city']['state']}.</p>
    </footer>
</body>
</html>'''


# ---------------------------------------------------------------------------
# BROWSE PAGE TEMPLATE
# ---------------------------------------------------------------------------

def render_browse_page(service_key):
    svc = SERVICES[service_key]
    year = datetime.now().year

    # Build industry × city grid
    grid_html = ""
    for ikey, idata in INDUSTRIES.items():
        grid_html += f'<h3 style="margin:24px 0 10px;font-size:1.1rem;font-weight:700;color:#1B3A5C;">{idata["name"]}</h3>\n'
        grid_html += '<div style="display:flex;flex-wrap:wrap;gap:8px;margin-bottom:12px;">\n'
        for ckey, cdata in CITIES.items():
            grid_html += f'  <a href="/{service_key}/{ikey}/{ckey}" style="padding:6px 14px;background:#fff;color:#2563EB;border-radius:6px;font-size:.85rem;text-decoration:none;border:1px solid #e5e7eb;">{cdata["name"]}</a>\n'
        grid_html += '</div>\n'

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Free {svc['name']} for Every Industry & City | SoarAI</title>
    <meta name="description" content="Browse free {svc['short']} tools for 14 industries across 20 US cities. AI-powered analysis from SoarAI.">
    <link rel="canonical" href="{DOMAIN}/{service_key}/browse">
    <script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', '{GA_ID}');
    </script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif; color: #1f2937; line-height: 1.6; background: #f9fafb; }}
        .navbar {{ background: #fff; border-bottom: 1px solid #e5e7eb; padding: 16px 24px; display: flex; align-items: center; justify-content: space-between; }}
        .navbar a.logo {{ font-size: 22px; font-weight: 800; text-decoration: none; color: #1B3A5C; }}
        .navbar a.logo span {{ color: #2563EB; }}
        .hero {{ background: linear-gradient(135deg, #1B3A5C, #2563EB); color: #fff; padding: 60px 24px; text-align: center; }}
        .hero h1 {{ font-size: 2rem; font-weight: 800; margin-bottom: 12px; }}
        .hero p {{ font-size: 1.05rem; opacity: 0.9; max-width: 600px; margin: 0 auto; }}
        .container {{ max-width: 1100px; margin: 0 auto; padding: 40px 24px; }}
        .footer {{ background: #1B3A5C; color: #fff; text-align: center; padding: 36px 24px; margin-top: 40px; }}
        .footer p {{ color: rgba(255,255,255,0.8); font-size: 0.85rem; margin-bottom: 8px; }}
        .footer a {{ color: #93c5fd; text-decoration: none; }}
    </style>
</head>
<body>
    <nav class="navbar">
        <a href="/" class="logo">Soar<span>AI</span></a>
    </nav>
    <header class="hero">
        <h1>Free {svc['name']} — Browse by Industry & City</h1>
        <p>AI-powered {svc['short']} tools for 14 industries across 20 US cities. Pick yours below.</p>
    </header>
    <div class="container">
{grid_html}
    </div>
    <footer class="footer">
        <p><a href="{DOMAIN}">SoarAI</a> — AI-Powered Growth Agency</p>
        <p>&copy; {year} SoarAI. All rights reserved.</p>
    </footer>
</body>
</html>'''


# ---------------------------------------------------------------------------
# SITEMAP GENERATION
# ---------------------------------------------------------------------------

def generate_sitemap():
    now = datetime.now().strftime('%Y-%m-%d')
    urls = []

    # Main pages
    main_pages = [
        ('/', '1.0', 'weekly'),
        ('/pricing.html', '0.9', 'monthly'),
        ('/SEOAudit/seo-audit-form.html', '0.9', 'monthly'),
        ('/keyword-research-form.html', '0.9', 'monthly'),
        ('/lpo-scorecard-form.html', '0.9', 'monthly'),
        ('/AdCopy/ac-agent-form.html', '0.9', 'monthly'),
    ]
    for path, priority, freq in main_pages:
        urls.append(f'  <url><loc>{DOMAIN}{path}</loc><lastmod>{now}</lastmod><changefreq>{freq}</changefreq><priority>{priority}</priority></url>')

    # Browse pages
    for svc_key in SERVICES:
        urls.append(f'  <url><loc>{DOMAIN}/{svc_key}/browse</loc><lastmod>{now}</lastmod><changefreq>weekly</changefreq><priority>0.8</priority></url>')

    # All programmatic pages
    for svc_key in SERVICES:
        for ind_key in INDUSTRIES:
            for cty_key in CITIES:
                url = f"{DOMAIN}/{svc_key}/{ind_key}/{cty_key}"
                urls.append(f'  <url><loc>{url}</loc><lastmod>{now}</lastmod><changefreq>weekly</changefreq><priority>0.7</priority></url>')

    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    xml += '\n'.join(urls)
    xml += '\n</urlset>'
    return xml


# ---------------------------------------------------------------------------
# MAIN — Generate all files
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.abspath(__file__))
    total = 0

    # 1. Generate landing pages
    for svc_key in SERVICES:
        for ind_key in INDUSTRIES:
            for cty_key in CITIES:
                content = generate_page_content(svc_key, ind_key, cty_key)
                html = render_landing_page(content)

                # Create directory: /free-seo-audit/ecommerce/
                page_dir = os.path.join(base_dir, svc_key, ind_key)
                os.makedirs(page_dir, exist_ok=True)

                # Write file: /free-seo-audit/ecommerce/new-york.html
                # BUT for Cloudflare Pages clean URLs, use folder + index.html
                city_dir = os.path.join(page_dir, cty_key)
                os.makedirs(city_dir, exist_ok=True)
                filepath = os.path.join(city_dir, 'index.html')
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(html)
                total += 1

    print(f'Generated {total} landing pages')

    # 2. Generate browse pages
    for svc_key in SERVICES:
        browse_dir = os.path.join(base_dir, svc_key, 'browse')
        os.makedirs(browse_dir, exist_ok=True)
        html = render_browse_page(svc_key)
        with open(os.path.join(browse_dir, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'Generated browse page: /{svc_key}/browse')

    # 3. Generate sitemap.xml
    sitemap = generate_sitemap()
    with open(os.path.join(base_dir, 'sitemap.xml'), 'w', encoding='utf-8') as f:
        f.write(sitemap)
    print(f'Generated sitemap.xml with {total + 4 + 6} URLs')

    # 4. Generate robots.txt
    robots = f"""User-agent: *
Allow: /

Disallow: /generate_pages.py

Sitemap: {DOMAIN}/sitemap.xml
"""
    with open(os.path.join(base_dir, 'robots.txt'), 'w', encoding='utf-8') as f:
        f.write(robots)
    print('Generated robots.txt')

    print(f'\nDone! {total} landing pages + 4 browse pages + sitemap.xml + robots.txt')
