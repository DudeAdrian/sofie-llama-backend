#!/usr/bin/env python3
"""
Quick test script for S.O.F.I.E. Backend API.
Demonstrates the consent-before-computation workflow.
"""

import requests
import json
from typing import Dict, Any

# Configuration
BASE_URL = "http://localhost:8000"
USER_ID = "test_user_123"


def print_response(title: str, response: requests.Response):
    """Pretty print API response."""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)


def main():
    """Run through the complete API workflow."""
    
    print("\n🌟 S.O.F.I.E. Backend API Test")
    print("=" * 60)
    
    # 1. Health check
    print("\n1️⃣  Checking service health...")
    response = requests.get(f"{BASE_URL}/api/v1/health")
    print_response("Health Check", response)
    
    # 2. Try to get guidance WITHOUT consent (should fail)
    print("\n2️⃣  Attempting to get wellness guidance WITHOUT consent...")
    response = requests.post(
        f"{BASE_URL}/api/v1/wellness/guidance",
        json={
            "user_id": USER_ID,
            "query": "What are some stress reduction techniques?",
        }
    )
    print_response("Wellness Guidance (No Consent) - Expected: 403 Forbidden", response)
    
    # 3. Grant consent
    print("\n3️⃣  Granting consent for wellness guidance...")
    response = requests.post(
        f"{BASE_URL}/api/v1/consent/grant",
        json={
            "user_id": USER_ID,
            "consent_type": "wellness_guidance",
            "purpose": "Receive personalized wellness guidance for stress reduction"
        }
    )
    print_response("Grant Consent", response)
    
    # 4. Check consent status
    print("\n4️⃣  Checking consent status...")
    response = requests.get(
        f"{BASE_URL}/api/v1/consent/check/{USER_ID}/wellness_guidance"
    )
    print_response("Check Consent Status", response)
    
    # 5. Get wellness guidance WITH consent (should succeed)
    print("\n5️⃣  Getting wellness guidance WITH consent...")
    response = requests.post(
        f"{BASE_URL}/api/v1/wellness/guidance",
        json={
            "user_id": USER_ID,
            "query": "What are some gentle exercises I can do to reduce stress?",
            "context": {
                "mood": "anxious",
                "stress_level": 7,
                "energy_level": 5,
                "goals": ["reduce stress", "improve sleep"]
            }
        }
    )
    print_response("Wellness Guidance (With Consent) - Expected: 200 OK", response)
    
    # 6. Revoke consent
    print("\n6️⃣  Revoking consent...")
    response = requests.delete(
        f"{BASE_URL}/api/v1/consent/revoke/{USER_ID}/wellness_guidance"
    )
    print_response("Revoke Consent", response)
    
    # 7. Try again after revocation (should fail)
    print("\n7️⃣  Attempting to get wellness guidance AFTER revocation...")
    response = requests.post(
        f"{BASE_URL}/api/v1/wellness/guidance",
        json={
            "user_id": USER_ID,
            "query": "Another wellness question?",
        }
    )
    print_response("Wellness Guidance (After Revocation) - Expected: 403 Forbidden", response)
    
    print("\n" + "="*60)
    print("✅ Test workflow complete!")
    print("="*60)
    print("\nThis demonstrates:")
    print("  • Consent is REQUIRED before computation")
    print("  • Users can grant and revoke consent")
    print("  • Revocation immediately blocks further processing")
    print("  • All operations are logged and auditable")
    print("="*60 + "\n")


if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to the API server.")
        print("   Make sure the server is running: python -m app.main")
    except Exception as e:
        print(f"\n❌ Error: {e}")
