class PyDetonatorError(Exception):
    """Base exception for PyDetonator"""
    pass


class SandboxExecutionError(PyDetonatorError):
    """Raised when Docker sandbox execution fails"""
    pass


class AnalysisError(PyDetonatorError):
    """Raised when analysis pipeline fails"""
    pass


class ReportGenerationError(PyDetonatorError):
    """Raised when report creation fails"""
    pass