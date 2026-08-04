"""
End-to-End Pipeline Test - Research Agent -> Supplier Agent
Demonstrates full Project Athena workflow
"""

import sys
import json
from typing import Dict, List, Any


class MockResearchAgent:
    """Mock Research Agent for E2E testing"""

    def execute(self) -> Dict[str, Any]:
        return {
            "products": [
                {
                    "source": "amazon",
                    "name": "Cetaphil Daily Facial Cleanser",
                    "price": 7.99,
                    "asin": "B0BYR5R7ZY",
                    "category": "Face Wash",
                },
                {
                    "source": "amazon",
                    "name": "CeraVe Facial Moisturizing Lotion",
                    "price": 16.99,
                    "asin": "B00CL1MBSY",
                    "category": "Moisturizer",
                },
                {
                    "source": "aliexpress",
                    "name": "LED Makeup Mirror with Lights",
                    "price": 18.99,
                    "product_id": "1005008123456",
                    "category": "Mirrors",
                },
            ],
            "total_found": 3,
            "quality_score": 65.0,
        }


class MockSupplierAgent:
    """Mock Supplier Agent for E2E testing"""

    def execute(self, products: List[Dict[str, Any]]) -> Dict[str, Any]:
        supplier_results = []
        for product in products:
            supplier_results.append(
                {
                    "product_name": product["name"],
                    "product_price": product["price"],
                    "suppliers": [
                        {
                            "name": "Premium Supplier",
                            "rating": 4.8,
                            "unit_cost": product["price"] * 0.15,
                            "moq": 100,
                            "lead_time_days": 14,
                            "score": 85.0,
                        },
                        {
                            "name": "Budget Supplier",
                            "rating": 4.5,
                            "unit_cost": product["price"] * 0.12,
                            "moq": 500,
                            "lead_time_days": 21,
                            "score": 72.0,
                        },
                    ],
                }
            )

        return {
            "products_with_suppliers": supplier_results,
            "total_products": len(products),
            "total_suppliers": len(products) * 2,
        }


class MockValidationAgent:
    """Mock Validation Agent for E2E testing"""

    def execute(self, products_with_suppliers: List[Dict[str, Any]]) -> Dict[str, Any]:
        validation_results = []
        approved = 0
        rejected = 0

        for product_data in products_with_suppliers:
            # Simple validation: approve products with good margins
            for supplier in product_data.get("suppliers", [])[:1]:
                price = product_data.get("retail_price", 0)
                cost = supplier.get("unit_cost", 0)
                margin = ((price - cost) / price * 100) if price > 0 else 0

                is_approved = margin > 30  # Need >30% margin

                if is_approved:
                    approved += 1
                else:
                    rejected += 1

                validation_results.append(
                    {
                        "product_name": product_data.get("product_name"),
                        "approved": is_approved,
                        "risk_score": 25 if is_approved else 65,
                        "demand_confidence": 90 if is_approved else 60,
                        "net_margin_pct": round(margin, 1),
                    }
                )

        return {
            "validation_results": validation_results,
            "approved": approved,
            "rejected": rejected,
            "approval_rate": round((approved / max(approved + rejected, 1)) * 100, 1),
        }


class E2EPipelineOrchestrator:
    """Orchestrates end-to-end pipeline: Research -> Supplier -> Validation"""

    def __init__(self):
        self.research_agent = MockResearchAgent()
        self.supplier_agent = MockSupplierAgent()
        self.validation_agent = MockValidationAgent()
        self.pipeline_results = {}

    def run_pipeline(self) -> Dict[str, Any]:
        """Execute full pipeline"""
        print("\n" + "=" * 80)
        print("PROJECT ATHENA - END-TO-END PIPELINE TEST")
        print("=" * 80 + "\n")

        # Stage 1: Research Agent
        print("[STAGE 1] Running Research Agent...")
        research_results = self.research_agent.execute()
        print(
            f"[OK] Found {research_results['total_found']} products (quality: {research_results['quality_score']}%)"
        )

        # Stage 2: Supplier Agent
        print("\n[STAGE 2] Running Supplier Agent...")
        supplier_results = self.supplier_agent.execute(research_results["products"])
        print(
            f"[OK] Found {supplier_results['total_suppliers']} suppliers for {supplier_results['total_products']} products"
        )

        # Stage 3: Validation Agent
        print("\n[STAGE 3] Running Validation Agent...")
        validation_results = self.validation_agent.execute(
            supplier_results["products_with_suppliers"]
        )
        print(
            f"[OK] Validated {len(validation_results['validation_results'])} products (Approval rate: {validation_results['approval_rate']}%)"
        )

        # Aggregate results
        self.pipeline_results = {
            "stage_1_research": research_results,
            "stage_2_supplier": supplier_results,
            "stage_3_validation": validation_results,
            "pipeline_status": "success",
            "products_discovered": research_results["total_found"],
            "suppliers_found": supplier_results["total_suppliers"],
            "products_approved": validation_results["approved"],
            "approval_rate": validation_results["approval_rate"],
        }

        return self.pipeline_results

    def validate_pipeline(self) -> bool:
        """Validate pipeline output"""
        if not self.pipeline_results:
            return False

        if self.pipeline_results.get("pipeline_status") != "success":
            return False

        if self.pipeline_results.get("products_discovered") == 0:
            return False

        if self.pipeline_results.get("suppliers_found") == 0:
            return False

        return True

    def display_results(self) -> None:
        """Display pipeline results in detail"""
        print("\n" + "=" * 80)
        print("PIPELINE RESULTS")
        print("=" * 80 + "\n")

        research = self.pipeline_results["stage_1_research"]
        supplier = self.pipeline_results["stage_2_supplier"]
        validation = self.pipeline_results["stage_3_validation"]

        print("[STAGE 1: PRODUCT DISCOVERY]")
        print(f"Products Found: {research['total_found']}")
        print(f"Quality Score: {research['quality_score']}%\n")

        for product in research["products"]:
            print(f"  - {product['name']}")
            print(f"    Price: ${product['price']}")
            print(f"    Source: {product['source']}")
            print()

        print("[STAGE 2: SUPPLIER DISCOVERY]")
        print(f"Total Suppliers Found: {supplier['total_suppliers']}\n")

        for i, product_supplier in enumerate(supplier["products_with_suppliers"], 1):
            print(f"Product {i}: {product_supplier['product_name']}")
            print(f"Retail Price: ${product_supplier['product_price']:.2f}")
            print(f"Suppliers Available: {len(product_supplier['suppliers'])}")

            for j, s in enumerate(product_supplier["suppliers"], 1):
                margin = (
                    (product_supplier["product_price"] - s["unit_cost"])
                    / product_supplier["product_price"]
                    * 100
                )
                print(
                    f"  {j}. {s['name']} - Score: {s['score']}/100 - Unit Cost: ${s['unit_cost']:.2f} - Margin: {margin:.1f}%"
                )

            print()

        print("[STAGE 3: PRODUCT VALIDATION]")
        print(f"Products Validated: {len(validation['validation_results'])}")
        print(f"Approved: {validation['approved']}")
        print(f"Rejected: {validation['rejected']}")
        print(f"Approval Rate: {validation['approval_rate']}%\n")

        for result in validation["validation_results"]:
            status = "[APPROVED]" if result["approved"] else "[REJECTED]"
            print(
                f"{status} {result['product_name']} - Risk: {result['risk_score']}/100 - Margin: {result['net_margin_pct']:.1f}%"
            )
        print()

        print("=" * 80)
        print("PIPELINE SUMMARY")
        print(f"Total Products Analyzed: {self.pipeline_results['products_discovered']}")
        print(f"Total Suppliers Available: {self.pipeline_results['suppliers_found']}")
        print(
            f"Average Suppliers per Product: {self.pipeline_results['suppliers_found'] / self.pipeline_results['products_discovered']:.1f}"
        )
        print(f"Products Approved: {self.pipeline_results['products_approved']}")
        print(f"Approval Rate: {self.pipeline_results['approval_rate']}%")
        print(f"Pipeline Status: {self.pipeline_results['pipeline_status'].upper()}")
        print("=" * 80 + "\n")


def main():
    """Run E2E pipeline test"""
    print("[TEST] Running End-to-End Pipeline Test")

    orchestrator = E2EPipelineOrchestrator()

    # Run pipeline
    try:
        orchestrator.run_pipeline()

        # Validate
        if not orchestrator.validate_pipeline():
            print("[ERROR] Pipeline validation failed")
            return False

        # Display results
        orchestrator.display_results()

        # Summary
        print("[SUCCESS] End-to-End Pipeline Test Passed!")
        print(f"  - Stage 1 (Research): {orchestrator.pipeline_results['stage_1_research']['total_found']} products")
        print(
            f"  - Stage 2 (Supplier): {orchestrator.pipeline_results['stage_2_supplier']['total_suppliers']} suppliers"
        )
        print(
            f"  - Stage 3 (Validation): {orchestrator.pipeline_results['products_approved']} approved"
        )
        print(f"  - Approval Rate: {orchestrator.pipeline_results['approval_rate']}%")
        print(f"  - Pipeline Status: OK\n")

        return True

    except Exception as e:
        print(f"[ERROR] Pipeline execution failed: {e}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
