import loan_repository
import member_repository
import loan_service
import validation
from errors import bad_request, conflict, not_found
from fines import money


def list_members():
    return member_repository.list_members()


def get_member(member_id):
    member = member_repository.get_member(member_id)
    if member is None:
        raise not_found("member not found")
    return member


def create_member(data):
    if not data.get("name"):
        raise bad_request("name is required")
    if not validation.is_valid_email(data.get("email")):
        raise bad_request("invalid email")
    member_type = data.get("type", "student")
    if not validation.is_valid_member_type(member_type):
        raise bad_request("type must be student or staff")
    if member_repository.get_member_by_email(data["email"]) is not None:
        raise conflict("email already registered")
    return member_repository.create_member(data["name"], data["email"], member_type)


def member_account(member_id):
    member = get_member(member_id)
    loans = loan_repository.list_loans_for_member(member_id)
    open_loans = loan_service.count_open_loans(loans)
    limit = 5 if member["type"] == "staff" else 3
    return {
        "loans": [
            {
                "id": loan["id"],
                "book_id": loan["book_id"],
                "due_date": loan["due_date"],
                "returned": bool(loan["returned"]),
                "fine": money(loan["fine"]),
                "fine_paid": bool(loan["fine_paid"]),
            }
            for loan in loans
        ],
        "total_owed": money(loan_service.total_owed(loans)),
        "loans_remaining": limit - open_loans,
    }
