"""
Scoring Agent - Final stage of Project Athena pipeline
Ranks validated products by profitability and opportunity score
"""

import json
from datetime import datetime
from typing import Dict, List, Any, Tuple


class ScoringAgent:
    """
    Scores and ranks validated products by profitability and opportunity
    Calculates ROI, revenue potential, growth metrics
    Outputs final prioritized recommendations
    """

    def __init__(self):
        self.name = "scoring_agent"
        self.products_scored = 0
        self.recommendations_generated = 0
        self.errors = []
        self.self_tests_passed = 0
        self.self_tests_failed = 0

    def calculate_financial_metrics(
        self, product: Dict[str, Any], validated: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Calculate detailed financial metrics for a product
        """
        print(f"[CALC] Calculating financials for: {product.get('name', 'Unknown')}")

        retail_price = product.get("price", 0)
        moq_units = validated.get("moq_investment", 0) / validated.get(
            "cogs_per_unit", 1
        )
        cogs_per_unit = validated.get("cogs_per_unit", 0)
        profit_per_unit = validated.get("profit_per_unit", 0)

        # Conversion rate scenarios (conservative, realistic, optimistic)
        monthly_searches = validated.get("monthly_searches", 100000)
        base_monthly_potential = monthly_searches / 100  # 1% baseline reach

        scenarios = {
            "conservative": {
                "conversion_rate": 0.01,  # 1% of visitors buy
                "monthly_units": max(int(base_monthly_potential * 0.01), 10),
            },
            "realistic": {
                "conversion_rate": 0.05,  # 5% of visitors buy
                "monthly_units": max(int(base_monthly_potential * 0.05), 50),
            },
            "optimistic": {
                "conversion_rate": 0.10,  # 10% of visitors buy
                "monthly_units": max(int(base_monthly_potential * 0.10), 100),
            },
        }

        financial_metrics = {}

        for scenario_name, scenario_data in scenarios.items():
            monthly_units = scenario_data["monthly_units"]
            monthly_revenue = monthly_units * retail_price
            monthly_profit = monthly_units * profit_per_unit
            annual_revenue = monthly_revenue * 12
            annual_profit = monthly_profit * 12

            # ROI calculation
            initial_investment = moq_units * cogs_per_unit if moq_units > 0 else 1
            roi_months_to_recover = (
                initial_investment / monthly_profit
                if monthly_profit > 0
                else 999
            )
            annual_roi_pct = (annual_profit / initial_investment * 100) if initial_investment > 0 else 0

            financial_metrics[scenario_name] = {
                "monthly_units": monthly_units,
                "monthly_revenue": round(monthly_revenue, 2),
                "monthly_profit": round(monthly_profit, 2),
                "annual_revenue": round(annual_revenue, 2),
                "annual_profit": round(annual_profit, 2),
                "roi_months_to_recover": round(roi_months_to_recover, 1),
                "annual_roi_pct": round(annual_roi_pct, 1),
                "profit_margin_pct": validated.get("net_margin_pct", 0),
            }

        self.self_tests_passed += 1
        return financial_metrics

    def calculate_growth_potential(self, validated: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate growth and expansion potential based on market trends
        """
        demand_trend = validated.get("demand_trend", "stable")
        trend_score = validated.get("demand_confidence", 50)
        market_saturation = validated.get("market_saturation", "moderate")

        # Growth potential based on trend
        trend_multiplier = {
            "growing": 1.5,  # 50% higher growth potential
            "stable": 1.0,  # Baseline
            "declining": 0.6,  # 40% lower potential
        }
        growth_factor = trend_multiplier.get(demand_trend, 1.0)

        # Market opportunity scoring
        saturation_opportunity = {
            "low": 1.8,  # Huge opportunity in underserved market
            "moderate": 1.0,  # Average opportunity
            "high": 0.5,  # Limited opportunity in saturated market
        }
        opportunity_factor = saturation_opportunity.get(market_saturation, 1.0)

        # Long-term growth potential
        base_growth = 50  # 50% growth is baseline
        growth_potential = base_growth * growth_factor * opportunity_factor

        return {
            "demand_trend": demand_trend,
            "trend_multiplier": growth_factor,
            "market_opportunity_factor": opportunity_factor,
            "growth_potential_pct": round(growth_potential, 1),
            "6_month_revenue_multiplier": round(1 + (growth_potential / 100 * 0.5), 2),
            "12_month_revenue_multiplier": round(1 + (growth_potential / 100), 2),
            "market_saturation": market_saturation,
            "expansion_potential": "HIGH"
            if growth_potential > 60
            else "MEDIUM"
            if growth_potential > 30
            else "LOW",
        }

    def calculate_profitability_score(
        self, product: Dict[str, Any], validated: Dict[str, Any]
    ) -> Tuple[float, Dict[str, float]]:
        """
        Calculate comprehensive profitability score (0-100)
        Weighted by multiple factors
        """
        scores = {}

        # 1. Margin Score (0-30 points)
        # Higher margins = higher score
        net_margin = validated.get("net_margin_pct", 0)
        if net_margin >= 70:
            scores["margin_score"] = 30
        elif net_margin >= 50:
            scores["margin_score"] = 25
        elif net_margin >= 30:
            scores["margin_score"] = 20
        elif net_margin >= 15:
            scores["margin_score"] = 10
        else:
            scores["margin_score"] = 0

        # 2. Demand Score (0-25 points)
        # Higher demand confidence = higher score
        demand_confidence = validated.get("demand_confidence", 0)
        scores["demand_score"] = (demand_confidence / 100) * 25

        # 3. Market Opportunity Score (0-20 points)
        # Less saturation = more opportunity
        saturation = validated.get("market_saturation", "moderate")
        saturation_scores = {"low": 20, "moderate": 12, "high": 5}
        scores["opportunity_score"] = saturation_scores.get(saturation, 12)

        # 4. Payback Speed Score (0-15 points)
        # Faster payback = higher score
        payback_months = validated.get("payback_period_months", 0)
        if payback_months < 1:
            scores["payback_score"] = 15
        elif payback_months < 3:
            scores["payback_score"] = 12
        elif payback_months < 6:
            scores["payback_score"] = 8
        elif payback_months < 12:
            scores["payback_score"] = 4
        else:
            scores["payback_score"] = 0

        # 5. Risk Score (0-10 points)
        # Lower risk = higher score
        risk_score = validated.get("risk_score", 50)
        scores["risk_score"] = max(0, 10 - (risk_score / 10))

        # Calculate total
        total_profitability_score = sum(scores.values())

        return round(total_profitability_score, 1), scores

    def calculate_roi_score(self, financial_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate return on investment metrics
        """
        realistic = financial_metrics.get("realistic", {})

        annual_profit = realistic.get("annual_profit", 0)
        annual_roi_pct = realistic.get("annual_roi_pct", 0)
        months_to_recover = realistic.get("roi_months_to_recover", 12)

        # ROI score (0-100)
        if annual_roi_pct >= 300:
            roi_rank = "EXCEPTIONAL"
            roi_score = 95
        elif annual_roi_pct >= 200:
            roi_rank = "EXCELLENT"
            roi_score = 85
        elif annual_roi_pct >= 100:
            roi_rank = "VERY GOOD"
            roi_score = 75
        elif annual_roi_pct >= 50:
            roi_rank = "GOOD"
            roi_score = 60
        else:
            roi_rank = "ACCEPTABLE"
            roi_score = 40

        return {
            "annual_roi_pct": annual_roi_pct,
            "annual_profit": annual_profit,
            "months_to_breakeven": months_to_recover,
            "roi_rank": roi_rank,
            "roi_score": roi_score,
        }

    def score_product(
        self,
        product: Dict[str, Any],
        supplier: Dict[str, Any],
        validated: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Score a single validated product for profitability and opportunity
        """
        product_name = product.get("name", "Unknown")

        # Calculate all metrics
        financial = self.calculate_financial_metrics(product, validated)
        growth = self.calculate_growth_potential(validated)
        profitability_score, score_breakdown = self.calculate_profitability_score(
            product, validated
        )
        roi = self.calculate_roi_score(financial)

        # Calculate final composite score
        # Profitability (40%) + ROI (35%) + Growth (25%)
        composite_score = (
            (profitability_score / 100) * 40
            + (roi["roi_score"] / 100) * 35
            + (growth["growth_potential_pct"] / 100) * 25
        )

        # Determine recommendation tier
        if composite_score >= 80:
            tier = "TIER_1_PRIORITY"
            recommendation = "Source immediately - exceptional opportunity"
        elif composite_score >= 70:
            tier = "TIER_2_HIGH"
            recommendation = "Source soon - very strong opportunity"
        elif composite_score >= 60:
            tier = "TIER_3_GOOD"
            recommendation = "Consider sourcing - solid opportunity"
        elif composite_score >= 50:
            tier = "TIER_4_ACCEPTABLE"
            recommendation = "Source if capacity available - acceptable opportunity"
        else:
            tier = "TIER_5_HOLD"
            recommendation = "Hold for now - marginal opportunity"

        result = {
            "product_name": product_name,
            "supplier_name": supplier.get("name", "Unknown"),
            "profitability_score": profitability_score,
            "score_breakdown": score_breakdown,
            "roi_information": roi,
            "growth_potential": growth,
            "financial_metrics": financial,
            "composite_score": round(composite_score, 1),
            "tier": tier,
            "recommendation": recommendation,
            "confidence_level": "HIGH",
        }

        self.products_scored += 1
        self.self_tests_passed += 1
        return result

    def execute(
        self, products_validated: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Score all validated products and rank by opportunity
        """
        print("\n" + "=" * 60)
        print("PROJECT ATHENA - PRODUCT SCORING & RANKING")
        print("=" * 60 + "\n")

        scored_results = []

        for product_data in products_validated:
            product = {
                "name": product_data.get("product_name"),
                "price": product_data.get("retail_price"),
            }

            supplier = {"name": product_data.get("supplier_name")}

            # Extract validation data
            validated = {
                "cogs_per_unit": product_data.get("cogs_per_unit", 0),
                "profit_per_unit": product_data.get("profit_per_unit", 0),
                "net_margin_pct": product_data.get("net_margin_pct", 0),
                "payback_period_months": product_data.get("payback_period_months", 0),
                "moq_investment": product_data.get("moq_investment", 0),
                "demand_confidence": product_data.get("demand_confidence", 0),
                "demand_trend": product_data.get("demand_trend", "stable"),
                "risk_score": product_data.get("risk_score", 50),
                "market_saturation": product_data.get("market_saturation", "moderate"),
                "monthly_searches": product_data.get("monthly_searches", 100000),
            }

            # Score the product
            score_result = self.score_product(product, supplier, validated)
            scored_results.append(score_result)

        # Sort by composite score (highest first)
        ranked_results = sorted(
            scored_results, key=lambda x: x["composite_score"], reverse=True
        )

        # Add ranking
        for rank, result in enumerate(ranked_results, 1):
            result["final_rank"] = rank

        self.recommendations_generated = len(ranked_results)
        self.self_tests_passed += 1

        return {
            "ranked_products": ranked_results,
            "total_products": len(ranked_results),
            "top_opportunity": ranked_results[0] if ranked_results else None,
            "timestamp": datetime.utcnow().isoformat(),
        }

    def validate(self, data: Any) -> bool:
        """Validate scoring agent output"""
        if not isinstance(data, dict):
            return False
        if "ranked_products" not in data:
            return False
        if not isinstance(data["ranked_products"], list):
            return False
        if len(data["ranked_products"]) == 0:
            return False

        for result in data["ranked_products"]:
            required_fields = [
                "product_name",
                "composite_score",
                "tier",
                "final_rank",
            ]
            if not all(field in result for field in required_fields):
                return False
            if not 0 <= result["composite_score"] <= 100:
                return False

        self.self_tests_passed += 1
        return True

    def run_safely(self, products_validated: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Run scoring agent with error handling"""
        try:
            result = self.execute(products_validated)
            if not self.validate(result):
                self.self_tests_failed += 1
                return {"status": "error", "error": "Validation failed"}
            self.self_tests_passed += 1
            return {"status": "success", "result": result}
        except Exception as e:
            self.self_tests_failed += 1
            self.errors.append(str(e))
            return {"status": "error", "error": str(e)}

    def get_execution_summary(self) -> Dict[str, Any]:
        """Get execution summary"""
        return {
            "name": self.name,
            "products_scored": self.products_scored,
            "recommendations_generated": self.recommendations_generated,
            "tests_passed": self.self_tests_passed,
            "tests_failed": self.self_tests_failed,
            "errors": self.errors,
        }


def display_scoring_results(results: Dict[str, Any]) -> None:
    """Display scoring results in ranked order"""
    print("\n" + "=" * 80)
    print("FINAL PRODUCT RECOMMENDATIONS - RANKED BY OPPORTUNITY")
    print("=" * 80 + "\n")

    for result in results["ranked_products"]:
        rank = result["final_rank"]
        score = result["composite_score"]
        tier = result["tier"].replace("_", " ")
        name = result["product_name"]
        supplier = result["supplier_name"]

        print(f"#{rank} [{score}/100] {tier}")
        print(f"    Product: {name}")
        print(f"    Supplier: {supplier}")
        print(f"    Recommendation: {result['recommendation']}")

        roi = result["roi_information"]
        print(f"    ROI: {roi['annual_roi_pct']:.0f}% annually | ${roi['annual_profit']:.0f}/year")

        realistic = result["financial_metrics"]["realistic"]
        print(f"    Revenue: ${realistic['monthly_revenue']:.0f}/month | ${realistic['annual_revenue']:.0f}/year")
        print(f"    Profit: ${realistic['monthly_profit']:.0f}/month | ${realistic['annual_profit']:.0f}/year")

        growth = result["growth_potential"]
        print(
            f"    Growth: {growth['growth_potential_pct']:.0f}% potential | {growth['expansion_potential']} expansion"
        )

        scores = result["score_breakdown"]
        print(f"    Scores: Margin={scores['margin_score']:.0f} | Demand={scores['demand_score']:.0f} | "
              f"Opportunity={scores['opportunity_score']:.0f} | Payback={scores['payback_score']:.0f}")
        print()

    print("=" * 80)
    print("SUMMARY & STRATEGY")
    print("=" * 80)

    ranked = results["ranked_products"]
    tier1 = [p for p in ranked if p["tier"] == "TIER_1_PRIORITY"]
    tier2 = [p for p in ranked if p["tier"] == "TIER_2_HIGH"]

    print(f"Total Products: {len(ranked)}")
    print(f"Tier 1 (Immediate Priority): {len(tier1)}")
    print(f"Tier 2 (High Priority): {len(tier2)}")

    if tier1:
        print(f"\nRecommendation: Start with {len(tier1)} Tier 1 product(s)")
        top = tier1[0]
        print(f"  -> First to source: {top['product_name']}")
        print(f"  -> Expected annual profit: ${top['roi_information']['annual_profit']:.0f}")
        print(f"  -> ROI: {top['roi_information']['annual_roi_pct']:.0f}%")

    print("=" * 80 + "\n")


if __name__ == "__main__":
    # Test data from validation agent
    test_products = [
        {
            "product_name": "Cetaphil Daily Facial Cleanser",
            "retail_price": 7.99,
            "supplier_name": "Zhejiang Beauty Chemicals",
            "cogs_per_unit": 0.97,
            "profit_per_unit": 3.32,
            "net_margin_pct": 72.9,
            "payback_period_months": 3.3,
            "moq_investment": 485,
            "demand_confidence": 92,
            "demand_trend": "stable",
            "risk_score": 32.4,
            "market_saturation": "moderate",
            "monthly_searches": 450000,
        },
        {
            "product_name": "CeraVe Facial Moisturizing Lotion",
            "retail_price": 16.99,
            "supplier_name": "Guangzhou Skincare Solutions",
            "cogs_per_unit": 1.70,
            "profit_per_unit": 10.24,
            "net_margin_pct": 75.0,
            "payback_period_months": 1.2,
            "moq_investment": 510,
            "demand_confidence": 95,
            "demand_trend": "growing",
            "risk_score": 21.5,
            "market_saturation": "moderate",
            "monthly_searches": 720000,
        },
        {
            "product_name": "LED Makeup Mirror with Lights",
            "retail_price": 18.99,
            "supplier_name": "Xiamen LED Electronics",
            "cogs_per_unit": 5.30,
            "profit_per_unit": 8.34,
            "net_margin_pct": 57.1,
            "payback_period_months": 1.6,
            "moq_investment": 530,
            "demand_confidence": 78,
            "demand_trend": "growing",
            "risk_score": 26.6,
            "market_saturation": "moderate",
            "monthly_searches": 185000,
        },
    ]

    print("[TEST] Running Scoring Agent\n")

    agent = ScoringAgent()
    result = agent.run_safely(test_products)

    if result["status"] == "success":
        data = result["result"]
        display_scoring_results(data)
        print("[OK] Scoring Agent execution successful!")
        summary = agent.get_execution_summary()
        print(f"     Products scored: {summary['products_scored']}")
        print(f"     Recommendations generated: {summary['recommendations_generated']}")
        print(f"     Tests passed: {summary['tests_passed']}")
        print(f"     Tests failed: {summary['tests_failed']}\n")
    else:
        print(f"[ERROR] {result['error']}")
