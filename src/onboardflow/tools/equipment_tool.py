"""Equipment Provisioning tool - orders and tracks equipment."""

from datetime import datetime, timedelta


def provision_equipment(
    employee_name: str,
    role: str,
    department: str,
    location: str = "Remote",
) -> dict:
    """Provision equipment for new hire based on role.
    
    Args:
        employee_name: Name of the new hire
        role: Job title/role
        department: Department name
        location: Work location (Remote/Office/Hybrid)
    
    Returns:
        dict with equipment order details
    """
    # Role-based equipment packages
    equipment_packages = {
        "engineering": {
            "standard": ["Laptop (16GB RAM)", "Monitor (27\")", "Keyboard", "Mouse"],
            "premium": ["Laptop (32GB RAM)", "Dual Monitor Setup", "Mechanical Keyboard", "Ergonomic Mouse"],
        },
        "design": {
            "standard": ["Laptop (16GB RAM)", "Monitor (27\" 4K)", "Graphics Tablet", "Color Calibrator"],
            "premium": ["MacBook Pro", "Pro Display XDR", "Wacom Tablet", "Color Calibrator"],
        },
        "sales": {
            "standard": ["Laptop (8GB RAM)", "Monitor (24\")", "Headset", "Webcam"],
            "premium": ["Laptop (16GB RAM)", "Dual Monitor", "Premium Headset", "4K Webcam"],
        },
        "default": {
            "standard": ["Laptop (8GB RAM)", "Monitor (24\")", "Keyboard", "Mouse"],
        }
    }
    
    # Determine package tier based on role level
    is_senior = any(word in role.lower() for word in ["senior", "lead", "principal", "manager", "director"])
    tier = "premium" if is_senior else "standard"
    
    # Get equipment list
    dept_key = department.lower()
    package = equipment_packages.get(dept_key, equipment_packages["default"])
    equipment_list = package.get(tier, package["standard"])
    
    # Add location-specific items
    if location.lower() == "remote":
        equipment_list.extend(["Laptop Stand", "External Webcam", "Noise-Canceling Headset"])
    
    # Calculate delivery date (5 business days)
    order_date = datetime.now()
    delivery_date = order_date + timedelta(days=7)
    
    order_id = f"equip-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    order_data = {
        "order_id": order_id,
        "employee_name": employee_name,
        "role": role,
        "department": department,
        "location": location,
        "equipment": equipment_list,
        "tier": tier,
        "estimated_delivery": delivery_date.isoformat(),
        "shipping_address": "To be confirmed by HR",
        "tracking_number": None,
        "status": "ordered",
        "created_at": datetime.now().isoformat(),
    }
    
    print(f"[EQUIPMENT] Ordered {len(equipment_list)} items for {employee_name} ({tier} package)")
    
    return {
        "success": True,
        "order_id": order_id,
        "data": order_data,
    }
