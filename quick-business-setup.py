#!/usr/bin/env python3
"""
QUICK BUSINESS SETUP AGENT
Generates complete Amazon business plan in ONE smart Claude call
"""

import os
import sys
import json
from pathlib import Path

# Suppress type annotation warnings
import warnings
warnings.filterwarnings('ignore')

import anthropic
from secrets_manager import get_secret

PROJECT_ROOT = Path(__file__).parent

# Get API key
API_KEY = get_secret("ANTHROPIC_API_KEY", "api_key")
if not API_KEY:
    print("ERROR: Need API key. Run: python secrets_manager.py setup")
    exit(1)

client = anthropic.Anthropic(api_key=API_KEY)

print("\n" + "=" * 70)
print("QUICK AMAZON BUSINESS SETUP AGENT")
print("Generating complete lash serum mascara business plan...")
print("=" * 70 + "\n")

# ONE powerful Claude call that generates EVERYTHING
prompt = """You are an expert Amazon seller with 15+ years of experience building $10K+/month beauty ecommerce businesses.

TASK: Generate a COMPLETE business plan for a lash serum + mascara combo product.

Generate this in valid JSON format with ALL the following sections:

{
  "amazon_listing": {
    "title": "Perfect 100-char title with keywords",
    "bullets": ["5", "conversion-optimized", "bullet points"],
    "description": "300-400 word product description",
    "keywords": ["10", "high-volume", "keywords"]
  },
  "pricing": {
    "launch_price": 34.99,
    "launch_price_reasoning": "Get reviews fast",
    "scale_price": 44.99,
    "premium_price": 54.99,
    "profit_per_unit": {
      "at_launch": 12.50,
      "at_scale": 18.50,
      "at_premium": 23.50
    },
    "amazon_fees_percentage": 45,
    "break_even_units": 12
  },
  "suppliers": {
    "recommendation": "Top 3 suppliers for lash serum mascara combo",
    "supplier_1": {
      "name": "Supplier name",
      "alibaba_category": "Cosmetics",
      "moq": 100,
      "price_per_unit": 18,
      "lead_time_days": 18,
      "quality_score": 9.2
    },
    "supplier_2": {"...": "..."},
    "supplier_3": {"...": "..."}
  },
  "images": {
    "description": "5 image descriptions for professional product photography",
    "image_1_lifestyle": "Woman wearing mascara with description...",
    "image_2_product": "Product closeup with description...",
    "image_3_serum": "Serum detail with description...",
    "image_4_application": "Application process with description...",
    "image_5_before_after": "Before/after transformation with description..."
  },
  "market_research": {
    "trend_score": "8/10 - Growing 5.7% annually",
    "competition_level": "4/10 - Low competition vs other mascara niches",
    "monthly_searches": "60,000",
    "customer_pain_point": "Want lash growth AND mascara in one product",
    "key_advantage": "Only combo product on market"
  },
  "marketing_strategy": {
    "week_1_target": "Launch with 30+ sales",
    "week_4_target": "30+ reviews minimum",
    "month_2_target": "50+ daily sales",
    "month_3_target": "$2,500+ monthly profit",
    "discount_strategy": "Offer $10 discount on first 50 sales for reviews"
  },
  "timeline": {
    "day_1": "Order supplier samples, launch listing",
    "week_1": "Get first 10 sales, collect reviews",
    "week_4": "Raise price to $44.99 with 30+ reviews",
    "month_2": "Scale ads, orders increasing",
    "month_3": "$2,500+ profit, plan second product"
  }
}

Be EXPERT-LEVEL. This is for someone starting their Amazon lash serum mascara business with $200 initial inventory investment.
Include REAL, ACTIONABLE, SPECIFIC numbers and recommendations.
Make JSON valid and well-structured."""

print("[AGENT] Calling Claude to generate complete business plan...")
print("[AGENT] This takes 30-60 seconds...\n")

try:
    response = client.messages.create(
        model="claude-opus-5",
        max_tokens=4096,
        messages=[{
            "role": "user",
            "content": prompt
        }]
    )

    result_text = response.content[0].text

    # Parse and save JSON
    try:
        # Try to extract JSON from response
        import re
        json_match = re.search(r'\{[\s\S]*\}', result_text)
        if json_match:
            business_plan = json.loads(json_match.group())
        else:
            # If no JSON found, save the full response
            business_plan = {"raw_response": result_text}
    except:
        business_plan = {"raw_response": result_text}

    # Save to file
    output_file = PROJECT_ROOT / "amazon_business_plan.json"
    with open(output_file, 'w') as f:
        json.dump(business_plan, f, indent=2)

    print(f"[SUCCESS] Business plan saved to: amazon_business_plan.json\n")

    # Print key sections
    print("=" * 70)
    print("YOUR AMAZON LASH SERUM MASCARA BUSINESS PLAN")
    print("=" * 70 + "\n")

    if "amazon_listing" in business_plan:
        listing = business_plan["amazon_listing"]
        print("AMAZON LISTING")
        print("-" * 70)
        print(f"Title: {listing.get('title', 'N/A')}\n")
        print("Bullets:")
        for i, bullet in enumerate(listing.get('bullets', []), 1):
            print(f"  {i}. {bullet}")
        print()

    if "pricing" in business_plan:
        pricing = business_plan["pricing"]
        print("PRICING STRATEGY")
        print("-" * 70)
        print(f"Launch price: ${pricing.get('launch_price', 'N/A')} (get reviews)")
        print(f"Scale price: ${pricing.get('scale_price', 'N/A')} (optimize profit)")
        print(f"Premium price: ${pricing.get('premium_price', 'N/A')} (maximize)")
        print(f"Profit per unit at launch: ${pricing.get('profit_per_unit', {}).get('at_launch', 'N/A')}")
        print(f"Break-even: {pricing.get('break_even_units', 'N/A')} units\n")

    if "suppliers" in business_plan:
        suppliers = business_plan["suppliers"]
        print("SUPPLIER RECOMMENDATIONS")
        print("-" * 70)
        print(suppliers.get('recommendation', 'Check full plan for details\n'))

    if "market_research" in business_plan:
        research = business_plan["market_research"]
        print("MARKET RESEARCH")
        print("-" * 70)
        print(f"Trend score: {research.get('trend_score', 'N/A')}")
        print(f"Competition: {research.get('competition_level', 'N/A')}")
        print(f"Monthly searches: {research.get('monthly_searches', 'N/A')}")
        print(f"Customer pain point: {research.get('customer_pain_point', 'N/A')}\n")

    if "timeline" in business_plan:
        timeline = business_plan["timeline"]
        print("GROWTH TIMELINE")
        print("-" * 70)
        for period, target in timeline.items():
            print(f"  {period}: {target}")
        print()

    print("=" * 70)
    print("FULL PLAN SAVED TO: amazon_business_plan.json")
    print("=" * 70)
    print("\nNext steps:")
    print("1. Review amazon_business_plan.json for all details")
    print("2. Copy listing to Amazon Seller account")
    print("3. Contact supplier #1")
    print("4. Order 100 units of lash serum mascara combo")
    print("5. Launch on Amazon at recommended price")
    print("6. Run Amazon ads to get first 30 reviews")
    print("7. Watch profits grow! 🚀\n")

except Exception as e:
    print(f"[ERROR] {str(e)}")
    print("\nTroubleshooting:")
    print("- Check API key is set correctly")
    print("- Check internet connection")
    print("- Check Claude API has quota remaining")
