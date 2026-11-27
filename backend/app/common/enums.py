from enum import StrEnum


class Role(StrEnum):
    ADMIN = "admin"
    COORDINATOR = "coordinator"
    MANAGER = "manager"
    APPROVER = "approver"
    EMPLOYEE = "employee"


class ProjectStatus(StrEnum):
    DRAFT = "draft"
    ACTIVE = "active"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class ActivityStatus(StrEnum):
    PLANNED = "planned"
    IN_PROGRESS = "inProgress"
    MANAGER_REVIEW = "managerReview"
    APPROVER_REVIEW = "approverReview"
    RETURNED = "returned"
    INTERNALLY_APPROVED = "internallyApproved"


class ExternalStatus(StrEnum):
    NOT_SENT = "notSent"
    SENT = "sent"
    ACCEPTED = "accepted"
    RETURNED = "returned"


class DocumentKind(StrEnum):
    REPORT = "report"
    CALCULATION = "calculation"
    CONFIRMATION = "confirmation"
    OTHER = "other"


class ReviewStage(StrEnum):
    MANAGER = "manager"
    APPROVER = "approver"


class ReviewDecision(StrEnum):
    APPROVE = "approve"
    RETURN = "return"


class EffectType(StrEnum):
    ACTUAL = "actual"
    POTENTIAL = "potential"
    RELEASED_FUNDS = "releasedFunds"
