from grievance_repository import save_grievance

try:
    grievance_id = save_grievance(
        complaint="The WiFi in our college library is not working.",
        category="Technical",
        severity="Urgent",
        department="IT",
        similarity=0.8809
    )

    print("✅ Grievance saved successfully!")
    print("Generated ID:", grievance_id)

except Exception as e:
    print("❌ Failed to save grievance:")
    print(e)