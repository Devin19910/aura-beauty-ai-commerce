"""
Test Validation Agent - Works without Redis/Database
"""

import sys
from typing import Dict, List, Any


class TestValidationAgent:
    """Test Validation Agent components"""

    def __init__(self):
        self.name = "validation_agent_test"
        self.tests_passed = 0
        self.tests_failed = 0

    def test_demand_scoring(self):
        """Test demand confidence scoring"""
        print("[TEST] Testing demand scoring...")

        def calculate_demand_confidence(
            trend_score: int, mention_count: int, search_volume: int
        ) -> int:
            trend_weight = (trend_score / 100) * 40
            mention_weight = min((mention_count / 10000) * 40, 40)
            search_weight = min((search_volume / 500000) * 20, 20)
            confidence = trend_weight + mention_weight + search_weight
            return int(min(confidence, 100))

        # High demand case
        confidence_high = calculate_demand_confidence(92, 28500, 720000)
        assert confidence_high >= 85

        # Low demand case
        confidence_low = calculate_demand_confidence(55, 3000, 80000)
        assert confidence_low < 50

        print(
            f"[PASS] Demand scoring test passed (High: {confidence_high}%, Low: {confidence_low}%)"
        )
        self.tests_passed += 1
        return True

    def test_margin_validation(self):
        """Test profit margin validation logic"""
        print("[TEST] Testing margin validation...")

        def validate_margin(net_margin: float, minimum_threshold: float = 15.0) -> bool:
            return net_margin >= minimum_threshold

        # Approved case
        assert validate_margin(72.9) == True

        # Rejected case
        assert validate_margin(8.5) == False

        # Borderline case
        assert validate_margin(15.0) == True

        print("[PASS] Margin validation test passed")
        self.tests_passed += 1
        return True

    def test_risk_scoring(self):
        """Test overall risk score calculation"""
        print("[TEST] Testing risk scoring...")

        def calculate_risk_score(
            demand_confidence: float,
            margin_pct: float,
            competitor_count: int,
            moq: int,
        ) -> float:
            # Demand risk (0-30)
            demand_risk = max(0, 30 - (demand_confidence / 100 * 30))

            # Margin risk (0-25)
            if margin_pct < 10:
                margin_risk = 25
            elif margin_pct < 20:
                margin_risk = 15
            elif margin_pct < 30:
                margin_risk = 8
            else:
                margin_risk = 3

            # Competition risk (0-25)
            if competitor_count > 18:
                competition_risk = 25
            elif competitor_count > 12:
                competition_risk = 15
            elif competitor_count > 6:
                competition_risk = 8
            else:
                competition_risk = 3

            # MOQ risk (0-20)
            if moq > 2000:
                moq_risk = 20
            elif moq > 1000:
                moq_risk = 12
            elif moq > 500:
                moq_risk = 6
            else:
                moq_risk = 2

            total = demand_risk + margin_risk + competition_risk + moq_risk
            return round(min(100, total), 1)

        # Low risk case
        low_risk = calculate_risk_score(92, 72.9, 12, 500)
        assert low_risk < 40

        # High risk case
        high_risk = calculate_risk_score(55, 8.5, 20, 2500)
        assert high_risk > 60

        print(
            f"[PASS] Risk scoring test passed (Low risk: {low_risk}/100, High risk: {high_risk}/100)"
        )
        self.tests_passed += 1
        return True

    def test_payback_calculation(self):
        """Test payback period calculation"""
        print("[TEST] Testing payback calculation...")

        def calculate_payback_months(
            moq: int, unit_profit: float, monthly_sales_estimate: int
        ) -> float:
            if monthly_sales_estimate == 0:
                return 999
            total_investment = moq * (0.85 + 0.12)  # cost + shipping
            monthly_profit = monthly_sales_estimate * unit_profit
            if monthly_profit == 0:
                return 999
            return total_investment / monthly_profit

        # Fast payback
        payback_fast = calculate_payback_months(300, 10.24, 360)
        assert payback_fast < 2

        # Slow payback
        payback_slow = calculate_payback_months(2000, 3.32, 100)
        assert payback_slow > 5

        print(
            f"[PASS] Payback calculation test passed (Fast: {payback_fast:.1f}mo, Slow: {payback_slow:.1f}mo)"
        )
        self.tests_passed += 1
        return True

    def test_approval_logic(self):
        """Test product approval decision logic"""
        print("[TEST] Testing approval logic...")

        def should_approve(
            net_margin: float, demand_confidence: float, risk_score: float
        ) -> bool:
            return (
                net_margin >= 15 and demand_confidence >= 75 and risk_score <= 50
            )

        # Approved case
        assert should_approve(72.9, 92, 32.4) == True

        # Rejected - low margin
        assert should_approve(8.5, 92, 32.4) == False

        # Rejected - low demand
        assert should_approve(72.9, 60, 32.4) == False

        # Rejected - high risk
        assert should_approve(72.9, 92, 65) == False

        # Borderline approved
        assert should_approve(15.0, 75.0, 50.0) == True

        print("[PASS] Approval logic test passed")
        self.tests_passed += 1
        return True

    def test_compliance_check(self):
        """Test compliance requirement checking"""
        print("[TEST] Testing compliance checking...")

        def get_compliance_risk(category: str) -> str:
            if any(word in category.lower() for word in ["face", "skin", "cleanser", "moistur"]):
                return "low"
            elif any(word in category.lower() for word in ["makeup", "mascara"]):
                return "low"
            elif any(word in category.lower() for word in ["brush", "tool", "mirror"]):
                return "very_low"
            return "unknown"

        # Skincare compliance
        assert get_compliance_risk("Face Wash") == "low"
        assert get_compliance_risk("Moisturizer") == "low"

        # Makeup compliance
        assert get_compliance_risk("Mascara") == "low"

        # Tools compliance
        assert get_compliance_risk("Brush Set") == "very_low"
        assert get_compliance_risk("Mirror") == "very_low"

        print("[PASS] Compliance checking test passed")
        self.tests_passed += 1
        return True

    def test_validation_output_structure(self):
        """Test validation output data structure"""
        print("[TEST] Testing validation output structure...")

        validation_result = {
            "product_name": "Test Product",
            "supplier_name": "Test Supplier",
            "approved": True,
            "approval_reason": "All criteria met",
            "risk_score": 32.4,
            "demand_confidence": 92,
            "demand_trend": "growing",
            "net_margin_pct": 72.9,
            "profit_per_unit": 3.32,
            "monthly_profit_optimistic": 747,
            "payback_period_months": 3.3,
        }

        # Validate structure
        required_fields = [
            "product_name",
            "approved",
            "risk_score",
            "demand_confidence",
            "net_margin_pct",
        ]

        assert all(field in validation_result for field in required_fields)
        assert isinstance(validation_result["risk_score"], (int, float))
        assert 0 <= validation_result["risk_score"] <= 100
        assert 0 <= validation_result["demand_confidence"] <= 100

        print("[PASS] Validation output structure test passed")
        self.tests_passed += 1
        return True

    def run_all_tests(self) -> bool:
        """Run all tests"""
        print("\n[TEST] Running Validation Agent Tests\n")

        tests = [
            self.test_demand_scoring,
            self.test_margin_validation,
            self.test_risk_scoring,
            self.test_payback_calculation,
            self.test_approval_logic,
            self.test_compliance_check,
            self.test_validation_output_structure,
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
    tester = TestValidationAgent()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)
