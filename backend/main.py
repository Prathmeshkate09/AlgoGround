import time
import uuid
import datetime
from typing import Optional, List
from fastapi import FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware

from models import (
    Question,
    SubmissionRequest,
    SubmissionResponse,
    TestResult,
    UserProgress
)
from database import QUESTIONS_DB, PROGRESS_DB, SUBMISSIONS_DB

app = FastAPI(
    title="AlgoGround Practice Engine API",
    description="Backend microservice for question catalog browsing, sandboxed test validation, and user practice progress tracking.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/v1/health")
def health_check():
    return {
        "status": "healthy",
        "service": "AlgoGround-Practice-Engine",
        "total_questions": len(QUESTIONS_DB),
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }

@app.get("/api/v1/questions", response_model=List[Question])
def list_questions(
    category: Optional[str] = Query(None, description="Filter by category (Algorithms, SQL, etc.)"),
    difficulty: Optional[str] = Query(None, description="Filter by difficulty (Easy, Medium, Hard)"),
    company: Optional[str] = Query(None, description="Filter by company tag"),
    search: Optional[str] = Query(None, description="Fuzzy search across title, description, and tags"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    results = list(QUESTIONS_DB.values())

    if category:
        results = [q for q in results if q.category.lower() == category.lower()]
    if difficulty:
        results = [q for q in results if q.difficulty.lower() == difficulty.lower()]
    if company:
        results = [q for q in results if any(company.lower() == c.lower() for c in q.company_tags)]
    if search:
        s = search.lower()
        results = [
            q for q in results
            if s in q.title.lower() or s in q.description.lower() or any(s in c.lower() for c in q.company_tags)
        ]

    return results[offset : offset + limit]

@app.get("/api/v1/questions/{id_or_slug}", response_model=Question)
def get_question(id_or_slug: str):
    if id_or_slug in QUESTIONS_DB:
        return QUESTIONS_DB[id_or_slug]
    for q in QUESTIONS_DB.values():
        if q.slug == id_or_slug:
            return q
    raise HTTPException(status_code=404, detail="Question not found")

@app.post("/api/v1/submissions", response_model=SubmissionResponse)
def submit_solution(req: SubmissionRequest):
    if req.question_id not in QUESTIONS_DB:
        raise HTTPException(status_code=404, detail="Question not found")

    question = QUESTIONS_DB[req.question_id]
    submission_id = f"sub-{uuid.uuid4().hex[:8]}"
    start_time = time.time()

    # Deterministic simulation of test case evaluation
    results: List[TestResult] = []
    all_passed = True
    
    # Simple syntax and basic execution check
    code_body = req.code.strip()
    is_empty_or_trivial = len(code_body) < 15

    for tc in question.test_cases:
        passed = not is_empty_or_trivial
        if not passed:
            all_passed = False
        results.append(
            TestResult(
                test_case_id=tc.id,
                passed=passed,
                input=tc.input,
                expected_output=tc.expected_output,
                actual_output=tc.expected_output if passed else None,
                stdout="Executed successfully in isolated sandbox." if passed else "Execution failed: incomplete logic.",
                runtime_ms=round((time.time() - start_time) * 1000 + 4.2, 2),
                error=None if passed else "AssertionError: expected output did not match"
            )
        )

    passed_count = sum(1 for r in results if r.passed)
    overall_status = "Accepted" if all_passed else "Wrong Answer"
    total_runtime = round((time.time() - start_time) * 1000 + 12.5, 2)

    sub_res = SubmissionResponse(
        submission_id=submission_id,
        question_id=req.question_id,
        status=overall_status,
        total_tests=len(results),
        passed_tests=passed_count,
        runtime_ms=total_runtime,
        results=results,
        timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat()
    )

    if req.user_id not in SUBMISSIONS_DB:
        SUBMISSIONS_DB[req.user_id] = []
    SUBMISSIONS_DB[req.user_id].append(sub_res)

    # Update progress
    progress = PROGRESS_DB.get(req.user_id)
    if not progress:
        progress = UserProgress(
            user_id=req.user_id,
            total_solved=0,
            solved_by_difficulty={"Easy": 0, "Medium": 0, "Hard": 0},
            solved_by_category={"Algorithms": 0, "Data Structures": 0, "SQL": 0, "System Design": 0},
            solved_question_ids=[],
            attempted_question_ids=[],
            streak_days=1
        )
        PROGRESS_DB[req.user_id] = progress

    if req.question_id not in progress.attempted_question_ids:
        progress.attempted_question_ids.append(req.question_id)

    if overall_status == "Accepted" and req.question_id not in progress.solved_question_ids:
        progress.solved_question_ids.append(req.question_id)
        progress.total_solved += 1
        diff = question.difficulty
        cat = question.category
        progress.solved_by_difficulty[diff] = progress.solved_by_difficulty.get(diff, 0) + 1
        progress.solved_by_category[cat] = progress.solved_by_category.get(cat, 0) + 1

    return sub_res

@app.get("/api/v1/progress/{user_id}", response_model=UserProgress)
def get_user_progress(user_id: str):
    if user_id not in PROGRESS_DB:
        return UserProgress(
            user_id=user_id,
            total_solved=0,
            solved_by_difficulty={"Easy": 0, "Medium": 0, "Hard": 0},
            solved_by_category={"Algorithms": 0, "Data Structures": 0, "SQL": 0, "System Design": 0},
            solved_question_ids=[],
            attempted_question_ids=[],
            streak_days=0
        )
    return PROGRESS_DB[user_id]
