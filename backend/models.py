from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field

class TestCase(BaseModel):
    id: str
    input: Any
    expected_output: Any
    is_hidden: bool = False

class Question(BaseModel):
    id: str
    title: str
    slug: str
    difficulty: str  # "Easy", "Medium", "Hard"
    category: str    # "Algorithms", "Data Structures", "SQL", "System Design"
    company_tags: List[str]
    description: str
    starter_code: Dict[str, str]  # language -> template code
    test_cases: List[TestCase]
    hints: List[str] = []

class SubmissionRequest(BaseModel):
    question_id: str
    user_id: str = "guest_user"
    language: str
    code: str

class TestResult(BaseModel):
    test_case_id: str
    passed: bool
    input: Any
    expected_output: Any
    actual_output: Optional[Any] = None
    stdout: str = ""
    runtime_ms: float = 0.0
    error: Optional[str] = None

class SubmissionResponse(BaseModel):
    submission_id: str
    question_id: str
    status: str  # "Accepted", "Wrong Answer", "Time Limit Exceeded", "Runtime Error"
    total_tests: int
    passed_tests: int
    runtime_ms: float
    results: List[TestResult]
    timestamp: str

class UserProgress(BaseModel):
    user_id: str
    total_solved: int
    solved_by_difficulty: Dict[str, int]
    solved_by_category: Dict[str, int]
    solved_question_ids: List[str]
    attempted_question_ids: List[str]
    streak_days: int
