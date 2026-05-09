"""Stage 1 MVP: classify recent emails and propose actions."""
from email_agent.gmail_client import get_gmail_service, fetch_recent_emails, apply_label
from email_agent.classifier import get_classifier, classify_email


def main():
    print("Authenticating with Gmail...")
    service = get_gmail_service()

    print("Loading classifier ...")
    classifier = get_classifier()

    print("Fetching recent unread emails...")
    emails = fetch_recent_emails(service, max_results=10)
    print(f"Found {len(emails)} emails\n")

    for i, email in enumerate(emails, 1):
        print(f"[{i}/{len(emails)}] {email['subject'][:60]}")
        print(f"   From: {email['from'][:60]}")

        try:
            result = classify_email(classifier, email)
            print(f"   → {result.category} ({result.confidence:.2f}) → {result.suggested_action}")
            print(f"   Reasoning: {result.reasoning}")

            # Stage 1: just apply a label, don't take real action yet
            label_name = f"ai/{result.category}"
            apply_label(service, email["id"], label_name)
            print(f"   ✓ Labeled as {label_name}\n")
        except Exception as e:
            print(f"   ✗ Error: {e}\n")


if __name__ == "__main__":
    main()