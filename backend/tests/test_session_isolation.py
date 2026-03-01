"""Minimal test: Prove session isolation works."""

import pytest
from sap_discovery.utils.session_state import set_processes, get_processes

def test_session_isolation():
    """Test that two sessions have isolated data."""
    # Session A
    set_processes("session-a", "job-1", [{"name": "Process A"}])
    
    # Session B
    set_processes("session-b", "job-2", [{"name": "Process B"}])
    
    # Verify isolation
    assert get_processes("session-a", "job-1")[0]["name"] == "Process A"
    assert get_processes("session-b", "job-2")[0]["name"] == "Process B"
    
    # Verify cross-access fails
    assert get_processes("session-a", "job-2") is None
    assert get_processes("session-b", "job-1") is None

def test_job_ownership():
    """Test that jobs are tracked per session."""
    set_processes("session-x", "job-x1", [{"name": "X1"}])
    set_processes("session-x", "job-x2", [{"name": "X2"}])
    
    from sap_discovery.utils.session_state import get_jobs_for_session
    jobs = get_jobs_for_session("session-x")
    
    assert len(jobs) == 2
    assert "job-x1" in jobs
    assert "job-x2" in jobs
