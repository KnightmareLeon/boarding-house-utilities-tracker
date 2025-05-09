import random
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta

unit_types = ["Residential", "Commercial", "Industrial", "Mixed-Use", "Office", "Retail"]
statuses = ["Active", "Inactive"]
payment_statuses = ["Paid", "Unpaid", "Overdue", "Partially Paid"]
street_names = ["Main", "Side", "Back", "Central", "Elm", "Pine", "Maple", "Oak", "Hill", "River"]

utility_types = ["Water", "Electricity", "Internet", "Gas", "Cable", "Waste"]
unit_names = [f"Unit {name}" for name in ["Alpha", "Beta", "Gamma", "Delta", "Epsilon", "Zeta", "Eta", "Theta", "Iota", "Kappa"]]
utility_statuses = ["Active", "Inactive"]
billing_cycles = ["Monthly", "Quarterly", "Yearly"]

bill_types = ["Electricity", "Water", "Internet", "Gas", "Cable", "Waste", "Miscellaneous"]
unit_names = [f"Unit {name}" for name in ["Alpha", "Beta", "Gamma", "Delta", "Epsilon", "Zeta", "Eta", "Theta", "Iota", "Kappa"]]
bill_statuses = ["Unpaid", "Paid", "Overdue", "Partially Paid"]

def generateUnitData():
    sampleData1 = []

    for i in range(1, 51):
        unit_id = f"U{i:03}"
        name = f"Unit {chr(64 + ((i - 1) % 26 + 1))}{i}"
        address = f"{100 + i * 3} {random.choice(street_names)} St"
        unit_type = random.choice(unit_types)
        status = random.choice(statuses)

        sampleData1.append({
            "UnitID": unit_id,
            "Name": name,
            "Address": address,
            "Type": unit_type,
            "Status": status,
        })

    return sampleData1

def generateUtilityData():
    sampleData2 = []

    for i in range(1, 51):
        utility_id = f"UT{i:03}"
        utility_type = random.choice(utility_types)
        unit_name = random.choice(unit_names)
        status = random.choice(utility_statuses)
        billing_cycle = random.choice(billing_cycles)

        sampleData2.append({
            "UtilityID": utility_id,
            "Type": utility_type,
            "UnitName": unit_name,
            "Status": status,
            "BillingCycle": billing_cycle
        })
    
    return sampleData2

def generateBillData():
    sampleData3 = []

    for i in range(1, 51):
        bill_id = f"BILL{i:03}"
        unit_name = random.choice(unit_names)
        bill_type = random.choice(bill_types)
        amount = f"₱{random.uniform(500, 10000):,.2f}"  
        days_offset = random.randint(-10, 30)
        due_date = (date.today() + timedelta(days=days_offset)).isoformat()
        status = random.choice(bill_statuses)

        sampleData3.append({
            "BillID": bill_id,
            "UnitName": unit_name,
            "Type": bill_type,
            "TotalAmount": amount,
            "DueDate": due_date,
            "Status": status
        })
    
    return sampleData3

def generateRandomUtilityData(startDate=None, endDate=None):
    if startDate is None:
        startDate = datetime(2023, 4, 1)
    if endDate is None:
        endDate = datetime(2025, 4, 22)

    def month_range(start, end):
        current = start.replace(day=1)
        while current <= end:
            yield current
            current += relativedelta(months=1)

    def random_date(start, end):
        delta = end - start
        return start + timedelta(days=random.randint(0, delta.days))

    monthly_categories = {
        "Electricity": (1000, 10000),
        "Water": (50, 250),
        "Trash": (500, 500),
        "Internet": (1000, 3500),
    }

    random_categories = {
        "Gas": (1000, 2000),
        "Maintenance": (100, 5000),
        "Miscellaneous": (0, 5000)
    }

    data = {}
    bill_id_counter = 1

    # Generate monthly bills
    for category, (min_amt, max_amt) in monthly_categories.items():
        bills = []
        for month in month_range(startDate, endDate):
            amount = random.randint(min_amt, max_amt)
            bill_date = (month + relativedelta(day=28))  # Approx last day of month
            bills.append({
                "BillID": bill_id_counter,
                "TotalAmount": str(amount),
                "BillingPeriodEnd": bill_date.strftime("%Y-%m-%d")
            })
            bill_id_counter += 1
        data[category] = bills

    # Generate random bills
    for category, (min_amt, max_amt) in random_categories.items():
        bills = []
        num_entries = random.randint(0, 10)
        for _ in range(num_entries):
            bill_date = random_date(startDate, endDate)
            amount = random.randint(min_amt, max_amt)
            bills.append({
                "BillID": bill_id_counter,
                "TotalAmount": str(amount),
                "BillingPeriodEnd": bill_date.strftime("%Y-%m-%d")
            })
            bill_id_counter += 1
        bills.sort(key=lambda b: b["BillingPeriodEnd"])
        data[category] = bills

    return data

def generateBillsDataFromUtility():
    raw_data = generateRandomUtilityData()
    flat_list = []
    bill_id = 1

    for category, bills in raw_data.items():
        for bill in bills:
            due_date = datetime.strptime(bill["BillingPeriodEnd"], "%Y-%m-%d")
            flat_list.append({
                "BillID": bill_id,
                "Type": category,
                "TotalAmount": float(bill["TotalAmount"]),
                "DueDate": due_date.strftime("%b %d"),
                "Status": random.choice(["Unpaid", "Partially Paid", "Overdue"]),
                "_sort_key": due_date  # temporary key for sorting
            })
            bill_id += 1

    # Sort by the actual date
    flat_list.sort(key=lambda b: b["_sort_key"])

    # Remove the temporary sort key
    for bill in flat_list:
        del bill["_sort_key"]

    return flat_list

def generateRandomeUtilityBills(utility, startDate=None, endDate=None):
    if startDate is None:
        startDate = datetime(2023, 4, 1)
    if endDate is None:
        endDate = datetime(2025, 4, 22)

    def month_range(start, end):
        current = start.replace(day=1)
        while current <= end:
            yield current
            current += relativedelta(months=1)

    def random_date(start, end):
        delta = end - start
        return start + timedelta(days=random.randint(0, delta.days))

    # Define the utility categories and their ranges
    monthly_categories = {
        "Electricity": (1000, 10000),
        "Water": (50, 250),
        "Trash": (500, 500),
        "Internet": (1000, 3500),
    }

    random_categories = {
        "Gas": (1000, 2000),
        "Maintenance": (100, 5000),
        "Miscellaneous": (0, 5000)
    }

    data = {}
    bill_id_counter = 1

    # Check if the utility is in the predefined categories
    if utility in monthly_categories:
        category = utility
        min_amt, max_amt = monthly_categories[category]
        bills = []
        for month in month_range(startDate, endDate):
            amount = random.randint(min_amt, max_amt)
            bill_date = (month + relativedelta(day=28))  # Approx last day of month
            bills.append({
                "BillID": bill_id_counter,
                "TotalAmount": str(amount),
                "BillingPeriodEnd": bill_date.strftime("%Y-%m-%d")
            })
            bill_id_counter += 1
        data[category] = bills
    elif utility in random_categories:
        category = utility
        min_amt, max_amt = random_categories[category]
        bills = []
        num_entries = random.randint(0, 10)
        for _ in range(num_entries):
            bill_date = random_date(startDate, endDate)
            amount = random.randint(min_amt, max_amt)
            bills.append({
                "BillID": bill_id_counter,
                "TotalAmount": str(amount),
                "BillingPeriodEnd": bill_date.strftime("%Y-%m-%d")
            })
            bill_id_counter += 1
        bills.sort(key=lambda b: b["BillingPeriodEnd"])
        data[category] = bills
    else:
        return f"Utility '{utility}' not found."

    return data