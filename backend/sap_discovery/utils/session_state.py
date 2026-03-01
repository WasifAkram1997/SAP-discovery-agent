"""Simple in-memory session state management."""

from typing import Dict, List, Optional

# job_id → list of processes
_processes: Dict[str, List[dict]] = {}

# job_id → result JSON string
_results: Dict[str, str] = {}

# session_id → list of job_ids (ownership tracking)
_session_jobs: Dict[str, List[str]] = {}


def set_processes(session_id: str, job_id: str, processes: List[dict]):
    """Store processes for a specific job and track ownership."""
    _processes[job_id] = processes

    if session_id not in _session_jobs:
        _session_jobs[session_id] = []
    _session_jobs[session_id].append(job_id)


def get_processes(session_id: str, job_id: str) -> Optional[List[dict]]:
    """Retrieve processes for a job, only if it belongs to this session."""
    if job_id not in _session_jobs.get(session_id, []):
        return None  # job doesn't belong to this user
    return _processes.get(job_id)


def set_result(job_id: str, result_json: str):
    """Store discovery results for a specific job."""
    _results[job_id] = result_json


def get_result(session_id: str, job_id: str) -> Optional[str]:
    """Retrieve results for a job, only if it belongs to this session."""
    if job_id not in _session_jobs.get(session_id, []):
        return None  # job doesn't belong to this user
    return _results.get(job_id)


def get_jobs_for_session(session_id: str) -> List[str]:
    """Get all job_ids for a specific session."""
    return _session_jobs.get(session_id, [])


def clear_job(session_id: str, job_id: str):
    """Clear a specific job, only if it belongs to this session."""
    if job_id not in _session_jobs.get(session_id, []):
        return
    _processes.pop(job_id, None)
    _results.pop(job_id, None)
    _session_jobs[session_id].remove(job_id)