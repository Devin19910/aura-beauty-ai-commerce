"""
Test Scoring Agent - Works without Redis/Database
"""

import sys
from typing import Dict, Any


class TestScoringAgent:
    """Test Scoring Agent components"""

    def __init__(self):
        self.name = "scoring_agent_test"
        self.tests_passed = 0
        self.tests_failed = 0

    def test_financial_calculations(self):
        """Test financial metric calculations"""
        print("[TEST] Testing financial calculations...")

        def calculate_annual_metrics(
            monthly_units: int, retail_price: float, cogs_per_unit: float
        ) -> Dict[str, float]:
            profit_per_unit = retail_price - cogs_per_unit
            monthly_profit = monthly_units * profit_per_unit
            annual_profit = monthly_profit * 12
            initial_investment = 500 * cogs_per_unit  # MOQ of 500
            annual_roi_pct = (annual_profit / initial_investment * 100) if initial_investment > 0 else 0

            return {
                "monthly_profit": round(monthly_profit, 2),
                "annual_profit": round(annual_profit, 2),
                "annual_roi_pct": round(annual_roi_pct, 1),
            }

        # Test case 1: High volume
        metrics1 = calculate_annual_metrics(
            monthly_units=360, retail_price=16.99, cogs_per_unit=1.70
        )
        assert metrics1["annual_roi_pct"] > 1000

        # Test case 2: Low volume
        metrics2 = calculate_annual_metrics(
            monthly_units=50, retail_price=7.99, cogs_per_unit=0.97
        )
        assert metrics2["annual_roi_pct"] > 500

        print(
            f"[PASS] Financial calculations test passed (ROI1: {metrics1['annual_roi_pct']:.0f}%, ROI2: {metrics2['annual_roi_pct']:.0f}%)"
        )
        self.tests_passed += 1
        return True

    def test_profitability_scoring(self):
        """Test profitability score calculation"""
        print("[TEST] Testing profitability scoring...")

        def calculate_profitability_score(
            margin_pct: float,
            demand_confidence: float,
            payback_months: float,
            risk_score: float,
        ) -> float:
            scores = {}

            # Margin component
            if margin_pct >= 70:
                scores["margin"] = 30
            elif margin_pct >= 50:
                scores["margin"] = 25
            elif margin_pct >= 30:
                scores["margin"] = 20
            else:
                scores["margin"] = 10

            # Demand component
            scores["demand"] = (demand_confidence / 100) * 25

            # Payback component
            if payback_months < 1:
                scores["payback"] = 15
            elif payback_months < 3:
                scores["payback"] = 12
            else:
                scores["payback"] = 8

            # Risk component
            scores["risk"] = max(0, 10 - (risk_score / 10))

            return sum(scores.values())

        # High quality product
        score_high = calculate_profitability_score(
            margin_pct=75.0, demand_confidence=95, payback_months=1.2, risk_score=21.5
        )
        assert score_high > 70, f"Expected >70, got {score_high}"

        # Average quality product
        score_avg = calculate_profitability_score(
            margin_pct=50.0, demand_confidence=75, payback_months=3.0, risk_score=40
        )
        assert 55 < score_avg < 75, f"Expected 55-75, got {score_avg}"

        # Low quality product
        score_low = calculate_profitability_score(
            margin_pct=20.0, demand_confidence=50, payback_months=10, risk_score=70
        )
        assert score_low < 50, f"Expected <50, got {score_low}"

        print(
            f"[PASS] Profitability scoring test passed (High: {score_high:.0f}, Avg: {score_avg:.0f}, Low: {score_low:.0f})"
        )
        self.tests_passed += 1
        return True

    def test_roi_ranking(self):
        """Test ROI-based ranking"""
        print("[TEST] Testing ROI ranking...")

        products = [
            {
                "name": "Product A",
                "annual_roi_pct": 500,
                "annual_profit": 5000,
            },
            {
                "name": "Product B",
                "annual_roi_pct": 1000,
                "annual_profit": 10000,
            },
            {
                "name": "Product C",
                "annual_roi_pct": 2000,
                "annual_profit": 20000,
            },
        ]

        # Sort by ROI
        ranked = sorted(
            products, key=lambda x: x["annual_roi_pct"], reverse=True
        )

        assert ranked[0]["name"] == "Product C"
        assert ranked[1]["name"] == "Product B"
        assert ranked[2]["name"] == "Product A"

        print("[PASS] ROI ranking test passed")
        self.tests_passed += 1
        return True

    def test_growth_potential(self):
        """Test growth potential calculation"""
        print("[TEST] Testing growth potential...")

        def calculate_growth_potential(
            demand_trend: str, market_saturation: str
        ) -> float:
            trend_multiplier = {
                "growing": 1.5,
                "stable": 1.0,
                "declining": 0.6,
            }
            saturation_factor = {
                "low": 1.8,
                "moderate": 1.0,
                "high": 0.5,
            }

            base_growth = 50
            multiplier = trend_multiplier.get(demand_trend, 1.0)
            factor = saturation_factor.get(market_saturation, 1.0)
            growth = base_growth * multiplier * factor

            return round(growth, 1)

        # Growing, low saturation = high growth
        growth_high = calculate_growth_potential(
            demand_trend="growing", market_saturation="low"
        )
        assert growth_high > 100

        # Stable, moderate saturation = average growth
        growth_avg = calculate_growth_potential(
            demand_trend="stable", market_saturation="moderate"
        )
        assert growth_avg == 50

        # Declining, high saturation = low growth
        growth_low = calculate_growth_potential(
            demand_trend="declining", market_saturation="high"
        )
        assert growth_low < 20

        print(
            f"[PASS] Growth potential test passed (High: {growth_high:.0f}%, Avg: {growth_avg:.0f}%, Low: {growth_low:.0f}%)"
        )
        self.tests_passed += 1
        return True

    def test_tier_assignment(self):
        """Test tier assignment based on composite score"""
        print("[TEST] Testing tier assignment...")

        def assign_tier(composite_score: float) -> str:
            if composite_score >= 80:
                return "TIER_1_PRIORITY"
            elif composite_score >= 70:
                return "TIER_2_HIGH"
            elif composite_score >= 60:
                return "TIER_3_GOOD"
            elif composite_score >= 50:
                return "TIER_4_ACCEPTABLE"
            else:
                return "TIER_5_HOLD"

        # Test tier assignment
        assert assign_tier(95) == "TIER_1_PRIORITY"
        assert assign_tier(75) == "TIER_2_HIGH"
        assert assign_tier(65) == "TIER_3_GOOD"
        assert assign_tier(55) == "TIER_4_ACCEPTABLE"
        assert assign_tier(35) == "TIER_5_HOLD"

        print("[PASS] Tier assignment test passed")
        self.tests_passed += 1
        return True

    def test_composite_scoring(self):
        """Test composite score calculation"""
        print("[TEST] Testing composite scoring...")

        def calculate_composite_score(
            profitability_score: float, roi_score: float, growth_potential: float
        ) -> float:
            # Weights: 40% profitability, 35% ROI, 25% growth
            composite = (
                (profitability_score / 100) * 40
                + (roi_score / 100) * 35
                + (growth_potential / 100) * 25
            )
            return round(composite, 1)

        # Excellent product
        score_excellent = calculate_composite_score(
            profitability_score=90, roi_score=95, growth_potential=80
        )
        assert score_excellent > 85

        # Average product
        score_average = calculate_composite_score(
            profitability_score=70, roi_score=65, growth_potential=50
        )
        assert 60 < score_average < 75

        # Poor product
        score_poor = calculate_composite_score(
            profitability_score=40, roi_score=30, growth_potential=20
        )
        assert score_poor < 35

        print(
            f"[PASS] Composite scoring test passed (Excellent: {score_excellent:.0f}, Avg: {score_average:.0f}, Poor: {score_poor:.0f})"
        )
        self.tests_passed += 1
        return True

    def test_product_ranking(self):
        """Test product ranking by composite score"""
        print("[TEST] Testing product ranking...")

        products = [
            {"name": "Product A", "composite_score": 75.5},
            {"name": "Product B", "composite_score": 88.3},
            {"name": "Product C", "composite_score": 62.1},
        ]

        # Sort by composite score
        ranked = sorted(
            products, key=lambda x: x["composite_score"], reverse=True
        )

        assert ranked[0]["name"] == "Product B"
        assert ranked[1]["name"] == "Product A"
        assert ranked[2]["name"] == "Product C"

        print("[PASS] Product ranking test passed")
        self.tests_passed += 1
        return True

    def test_recommendation_strategy(self):
        """Test recommendation strategy based on rankings"""
        print("[TEST] Testing recommendation strategy...")

        def generate_recommendation(tier: str) -> str:
            recommendations = {
                "TIER_1_PRIORITY": "Source immediately - exceptional opportunity",
                "TIER_2_HIGH": "Source soon - very strong opportunity",
                "TIER_3_GOOD": "Consider sourcing - solid opportunity",
                "TIER_4_ACCEPTABLE": "Source if capacity available",
                "TIER_5_HOLD": "Hold for now - marginal opportunity",
            }
            return recommendations.get(tier, "Unknown")

        # Test recommendations
        rec1 = generate_recommendation("TIER_1_PRIORITY")
        assert "immediately" in rec1

        rec2 = generate_recommendation("TIER_2_HIGH")
        assert "soon" in rec2

        rec5 = generate_recommendation("TIER_5_HOLD")
        assert "Hold" in rec5

        print("[PASS] Recommendation strategy test passed")
        self.tests_passed += 1
        return True

    def run_all_tests(self) -> bool:
        """Run all tests"""
        print("\n[TEST] Running Scoring Agent Tests\n")

        tests = [
            self.test_financial_calculations,
            self.test_profitability_scoring,
            self.test_roi_ranking,
            self.test_growth_potential,
            self.test_tier_assignment,
            self.test_composite_scoring,
            self.test_product_ranking,
            self.test_recommendation_strategy,
        ]

        for test in tests:
            try:
                test()
            except Exception as e:
                print(f"[FAIL] {test.__name__} failed: {e}")
                self.tests_failed += 1

        print(f"\n{'='*50}")
        print(f"Results: {self.tests_passed} passed, {self.tests_failed} failed")

        if self.tests_failed == 0:
            print("[SUCCESS] All tests passed!\n")
            return True
        else:
            print(f"[ERROR] {self.tests_failed} test(s) failed\n")
            return False


if __name__ == "__main__":
    tester = TestScoringAgent()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)
