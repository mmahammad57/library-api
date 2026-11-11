from datetime import date

import book_repository
import loan_repository
import report_repository
import loan_service
from fines import fine_for, money


def overdue_report():
    items = []
    total = 0
    for row in report_repository.list_open_loans_with_details():
        days_late = (date.today() - date.fromisoformat(row["due_date"])).days
        if days_late > 0:
            fine = fine_for(row["due_date"])
            total += fine
            items.append(
                {
                    "loan_id": row["id"],
                    "title": row["title"],
                    "member": row["name"],
                    "days_late": days_late,
                    "fine": money(fine),
                }
            )
    return {"items": items, "total_fines": money(total)}


def summary_report():
    loans = loan_repository.list_loans()
    return {
        "total_books": book_repository.count_books(),
        "on_loan": loan_service.count_open_loans(loans),
        "fines_outstanding": money(loan_service.total_owed(loans)),
    }
