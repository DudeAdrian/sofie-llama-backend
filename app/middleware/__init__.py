"""Middleware package for S.O.F.I.E. Backend."""

from app.middleware.consent import ConsentEnforcementMiddleware, LoggingMiddleware

__all__ = ["ConsentEnforcementMiddleware", "LoggingMiddleware"]
