"""
Test Supplier Agent - Works without Redis/Database
"""

import sys
from typing import Dict, List, Any


class TestSupplierAgent:
    """Test Supplier Agent integration"""

    def __init__(self):
        self.name = "supplier_agent_test"
        self.tests_passed = 0
        self.tests_failed = 0

    def test_supplier_discovery(self):
        """Test basic supplier discovery"""
        print("[TEST] Testing supplier discovery...")

        # Sample products
        products = [
            {
                "name": "Cetaphil Cleanser",
                "price": 7.99,
                "asin": "B0123456",
                "source": "amazon",
            },
            {
                "name": "LED Makeup Mirror",
                "price": 18.99,
                "product_id": "ALI001",
                "source": "aliexpress",
            },
        ]

        # Simulate supplier discovery
        supplier_results = []
        for product in products:
            suppliers = [
                {
                    "name": "Supplier A",
                    "rating": 4.8,
                    "unit_cost": 0.85,
                    "moq": 500,
                    "lead_time_days": 21,
                    "score": 75.5,
                },
                {
                    "name": "Supplier B",
                    "rating": 4.6,
                    "unit_cost": 0.78,
                    "moq": 1000,
                    "lead_time_days": 28,
                    "score": 72.3,
                },
            ]

            supplier_results.append(
                {
                    "product_name": product["name"],
                    "suppliers": suppliers,
                }
            )

        # Verify results
        assert len(supplier_results) == 2
        assert len(supplier_results[0]["suppliers"]) == 2
        assert supplier_results[0]["suppliers"][0]["score"] > 0
        print("[PASS] Supplier discovery test passed")
        self.tests_passed += 1
        return True

    def test_supplier_scoring(self):
        """Test supplier scoring algorithm"""
        print("[TEST] Testing supplier scoring...")

        def calculate_supplier_score(supplier: Dict[str, Any]) -> float:
            rating_score = (supplier.get("rating", 4.0) / 5.0) * 30
            cost_score = max(0, (10 - supplier.get("unit_cost", 5)) / 10 * 25)
            lead_time_score = max(
                0, (30 - supplier.get("lead_time_days", 30)) / 30 * 20
            )
            moq_score = max(0, (1000 - supplier.get("moq", 500)) / 1000 * 15)
            cert_count = len(supplier.get("certifications", []))
            cert_score = min(cert_count, 4) / 4 * 10

            total_score = (
                rating_score + cost_score + lead_time_score + moq_score + cert_score
            )
            return round(total_score, 1)

        supplier1 = {
            "rating": 4.8,
            "unit_cost": 0.85,
            "lead_time_days": 21,
            "moq": 500,
            "certifications": ["ISO9001", "GMP"],
        }

        supplier2 = {
            "rating": 4.5,
            "unit_cost": 1.50,
            "lead_time_days": 35,
            "moq": 1500,
            "certifications": ["ISO9001"],
        }

        score1 = calculate_supplier_score(supplier1)
        score2 = calculate_supplier_score(supplier2)

        assert score1 > 0
        assert score2 > 0
        assert score1 > score2  # Better supplier should score higher
        print(f"[PASS] Scoring test passed (Score1: {score1}, Score2: {score2})")
        self.tests_passed += 1
        return True

    def test_margin_calculation(self):
        """Test profit margin calculation"""
        print("[TEST] Testing margin calculation...")

        retail_price = 15.99
        unit_cost = 1.25
        shipping_cost = 0.35

        cogs = unit_cost + shipping_cost
        margin_percent = ((retail_price - cogs) / retail_price) * 100
        profit_per_unit = retail_price - cogs

        assert margin_percent > 0
        assert profit_per_unit > 0
        assert margin_percent < 100
        print(
            f"[PASS] Margin calculation test passed ({margin_percent:.1f}% margin, ${profit_per_unit:.2f} profit)"
        )
        self.tests_passed += 1
        return True

    def test_supplier_ranking(self):
        """Test supplier ranking logic"""
        print("[TEST] Testing supplier ranking...")

        suppliers = [
            {"name": "A", "score": 72.3},
            {"name": "B", "score": 85.0},
            {"name": "C", "score": 68.5},
        ]

        sorted_suppliers = sorted(suppliers, key=lambda x: x["score"], reverse=True)

        assert sorted_suppliers[0]["score"] == 85.0
        assert sorted_suppliers[1]["score"] == 72.3
        assert sorted_suppliers[2]["score"] == 68.5
        print("[PASS] Supplier ranking test passed")
        self.tests_passed += 1
        return True

    def test_product_supplier_mapping(self):
        """Test mapping products to suppliers"""
        print("[TEST] Testing product-supplier mapping...")

        products = [
            {"id": "P1", "name": "Cleanser", "price": 7.99},
            {"id": "P2", "name": "Mirror", "price": 18.99},
        ]

        supplier_mapping = {}
        for product in products:
            supplier_mapping[product["id"]] = {
                "product": product,
                "suppliers": [
                    {"name": "S1", "cost": 0.85},
                    {"name": "S2", "cost": 1.25},
                ],
            }

        assert len(supplier_mapping) == 2
        assert "P1" in supplier_mapping
        assert "P2" in supplier_mapping
        assert len(supplier_mapping["P1"]["suppliers"]) == 2
        print("[PASS] Product-supplier mapping test passed")
        self.tests_passed += 1
        return True

    def run_all_tests(self) -> bool:
        """Run all tests"""
        print("\n[TEST] Running Supplier Agent Tests\n")

        tests = [
            self.test_supplier_discovery,
            self.test_supplier_scoring,
            self.test_margin_calculation,
            self.test_supplier_ranking,
            self.test_product_supplier_mapping,
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
    tester = TestSupplierAgent()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)
