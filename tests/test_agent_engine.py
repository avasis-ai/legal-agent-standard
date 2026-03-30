"""Tests for Legal Agent Standard."""

import pytest
import sys
import os
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from legal_agent_standard.agent_engine import (
    ContractManager,
    ContractBounds,
    ActionExecution,
    AuditLogEntry,
    ContractValidator,
    LiabilityEngine,
    ContractStatus,
    LiabilityLevel
)


class TestContractStatus:
    """Tests for ContractStatus enum."""
    
    def test_status_values(self):
        """Test contract status values."""
        assert ContractStatus.VALID.value == "valid"
        assert ContractStatus.INVALID.value == "invalid"
        assert ContractStatus.EXPIRED.value == "expired"


class TestLiabilityLevel:
    """Tests for LiabilityLevel enum."""
    
    def test_liability_values(self):
        """Test liability level values."""
        assert LiabilityLevel.LOW.value == "low"
        assert LiabilityLevel.HIGH.value == "high"
        assert LiabilityLevel.CRITICAL.value == "critical"


class TestContractBounds:
    """Tests for ContractBounds."""
    
    def test_bounds_creation(self):
        """Test creating contract bounds."""
        bounds = ContractBounds(
            contract_id="CONTRACT_001",
            agent_id="agent_001",
            action_type="execute",
            max_value_limit=1000.0,
            allowed_operations=["execute", "validate"],
            prohibited_operations=["delete"],
            liability_level=LiabilityLevel.MEDIUM,
            audit_required=True,
            expiration_date=datetime.now(),
            signer_public_key="test_key",
            terms={"version": "1.0"}
        )
        
        assert bounds.contract_id == "CONTRACT_001"
        assert bounds.max_value_limit == 1000.0
    
    def test_bounds_to_dict(self):
        """Test converting bounds to dictionary."""
        bounds = ContractBounds(
            contract_id="CONTRACT_002",
            agent_id="agent_002",
            action_type="approve",
            max_value_limit=5000.0,
            allowed_operations=["execute"],
            prohibited_operations=[],
            liability_level=LiabilityLevel.LOW,
            audit_required=False,
            expiration_date=None,
            signer_public_key="key2",
            terms={}
        )
        
        data = bounds.to_dict()
        
        assert data['contract_id'] == "CONTRACT_002"
        assert data['liability_level'] == "low"


class TestActionExecution:
    """Tests for ActionExecution."""
    
    def test_action_creation(self):
        """Test creating an action execution."""
        action = ActionExecution(
            action_id="ACTION_001",
            agent_id="agent_001",
            action_type="execute",
            parameters={"test": "data"},
            value=100.0,
            timestamp=datetime.now(),
            proposed_by="test"
        )
        
        assert action.action_id == "ACTION_001"
        assert action.value == 100.0
    
    def test_action_to_dict(self):
        """Test converting action to dictionary."""
        action = ActionExecution(
            action_id="ACTION_002",
            agent_id="agent_002",
            action_type="validate",
            parameters={"query": "test"},
            value=500.0,
            timestamp=datetime.now(),
            proposed_by="agent"
        )
        
        data = action.to_dict()
        
        assert data['action_id'] == "ACTION_002"
        assert data['value'] == 500.0


class TestAuditLogEntry:
    """Tests for AuditLogEntry."""
    
    def test_entry_creation(self):
        """Test creating audit log entry."""
        entry = AuditLogEntry(
            log_id="LOG_001",
            action_id="ACTION_001",
            contract_id="CONTRACT_001",
            validation_result=ContractStatus.VALID,
            liability_assessment=LiabilityLevel.MEDIUM,
            audit_trail={"test": "data"},
            timestamp=datetime.now()
        )
        
        assert entry.log_id == "LOG_001"
        assert entry.validation_result == ContractStatus.VALID
    
    def test_entry_to_dict(self):
        """Test converting entry to dictionary."""
        entry = AuditLogEntry(
            log_id="LOG_002",
            action_id="ACTION_002",
            contract_id="CONTRACT_002",
            validation_result=ContractStatus.INVALID,
            liability_assessment=LiabilityLevel.LOW,
            audit_trail={"details": "test"},
            timestamp=datetime.now()
        )
        
        data = entry.to_dict()
        
        assert data['log_id'] == "LOG_002"
        assert data['validation_result'] == "invalid"


class TestContractValidator:
    """Tests for ContractValidator."""
    
    def test_register_contract(self):
        """Test registering a contract."""
        validator = ContractValidator()
        
        bounds = ContractBounds(
            contract_id="CONTRACT_001",
            agent_id="agent_001",
            action_type="execute",
            max_value_limit=1000.0,
            allowed_operations=["execute"],
            prohibited_operations=[],
            liability_level=LiabilityLevel.MEDIUM,
            audit_required=True,
            expiration_date=datetime.now(),
            signer_public_key="key",
            terms={}
        )
        
        result = validator.register_contract(bounds)
        
        assert result is True
        assert "CONTRACT_001" in validator._contracts
    
    def test_validate_action_allowed(self):
        """Test validating allowed action."""
        validator = ContractValidator()
        
        bounds = ContractBounds(
            contract_id="CONTRACT_001",
            agent_id="agent_001",
            action_type="execute",
            max_value_limit=1000.0,
            allowed_operations=["execute", "validate"],
            prohibited_operations=[],
            liability_level=LiabilityLevel.MEDIUM,
            audit_required=True,
            expiration_date=datetime.now(),
            signer_public_key="key",
            terms={}
        )
        
        validator.register_contract(bounds)
        
        action = ActionExecution(
            action_id="ACTION_001",
            agent_id="agent_001",
            action_type="execute",
            parameters={},
            value=500.0,
            timestamp=datetime.now(),
            proposed_by="test"
        )
        
        is_valid, reason = validator.validate_action(action, bounds)
        
        assert is_valid is True
    
    def test_validate_action_prohibited(self):
        """Test validating prohibited action."""
        validator = ContractValidator()
        
        bounds = ContractBounds(
            contract_id="CONTRACT_001",
            agent_id="agent_001",
            action_type="execute",
            max_value_limit=1000.0,
            allowed_operations=["execute"],
            prohibited_operations=["delete"],
            liability_level=LiabilityLevel.MEDIUM,
            audit_required=True,
            expiration_date=datetime.now(),
            signer_public_key="key",
            terms={}
        )
        
        validator.register_contract(bounds)
        
        action = ActionExecution(
            action_id="ACTION_001",
            agent_id="agent_001",
            action_type="delete",
            parameters={},
            value=100.0,
            timestamp=datetime.now(),
            proposed_by="test"
        )
        
        is_valid, reason = validator.validate_action(action, bounds)
        
        assert is_valid is False
        assert "prohibited" in reason.lower()
    
    def test_validate_action_exceeds_limit(self):
        """Test validating action that exceeds limit."""
        validator = ContractValidator()
        
        bounds = ContractBounds(
            contract_id="CONTRACT_001",
            agent_id="agent_001",
            action_type="execute",
            max_value_limit=500.0,
            allowed_operations=["execute"],
            prohibited_operations=[],
            liability_level=LiabilityLevel.MEDIUM,
            audit_required=True,
            expiration_date=datetime.now(),
            signer_public_key="key",
            terms={}
        )
        
        validator.register_contract(bounds)
        
        action = ActionExecution(
            action_id="ACTION_001",
            agent_id="agent_001",
            action_type="execute",
            parameters={},
            value=1000.0,
            timestamp=datetime.now(),
            proposed_by="test"
        )
        
        is_valid, reason = validator.validate_action(action, bounds)
        
        assert is_valid is False
        assert "exceeds" in reason.lower()


class TestLiabilityEngine:
    """Tests for LiabilityEngine."""
    
    def test_assess_liability_low(self):
        """Test liability assessment for low value."""
        engine = LiabilityEngine()
        
        bounds = ContractBounds(
            contract_id="CONTRACT_001",
            agent_id="agent_001",
            action_type="execute",
            max_value_limit=10000.0,
            allowed_operations=["execute"],
            prohibited_operations=[],
            liability_level=LiabilityLevel.LOW,
            audit_required=True,
            expiration_date=None,
            signer_public_key="key",
            terms={}
        )
        
        action = ActionExecution(
            action_id="ACTION_001",
            agent_id="agent_001",
            action_type="execute",
            parameters={},
            value=100.0,
            timestamp=datetime.now(),
            proposed_by="test"
        )
        
        liability = engine.assess_liability(action, bounds)
        
        assert liability == LiabilityLevel.LOW
    
    def test_assess_liability_critical(self):
        """Test liability assessment for critical value."""
        engine = LiabilityEngine()
        
        bounds = ContractBounds(
            contract_id="CONTRACT_001",
            agent_id="agent_001",
            action_type="execute",
            max_value_limit=1000000.0,
            allowed_operations=["execute"],
            prohibited_operations=[],
            liability_level=LiabilityLevel.MEDIUM,
            audit_required=True,
            expiration_date=None,
            signer_public_key="key",
            terms={}
        )
        
        action = ActionExecution(
            action_id="ACTION_001",
            agent_id="agent_001",
            action_type="execute",
            parameters={},
            value=2000000.0,
            timestamp=datetime.now(),
            proposed_by="test"
        )
        
        liability = engine.assess_liability(action, bounds)
        
        assert liability == LiabilityLevel.CRITICAL
    
    def test_create_audit_entry(self):
        """Test creating audit entry."""
        engine = LiabilityEngine()
        
        bounds = ContractBounds(
            contract_id="CONTRACT_001",
            agent_id="agent_001",
            action_type="execute",
            max_value_limit=10000.0,
            allowed_operations=["execute"],
            prohibited_operations=[],
            liability_level=LiabilityLevel.MEDIUM,
            audit_required=True,
            expiration_date=None,
            signer_public_key="key",
            terms={}
        )
        
        action = ActionExecution(
            action_id="ACTION_001",
            agent_id="agent_001",
            action_type="execute",
            parameters={},
            value=500.0,
            timestamp=datetime.now(),
            proposed_by="test"
        )
        
        entry = engine.create_audit_entry(
            action, bounds, ContractStatus.VALID, LiabilityLevel.MEDIUM
        )
        
        assert entry.log_id is not None
        assert entry.action_id == "ACTION_001"
    
    def test_get_audit_trail(self):
        """Test getting audit trail."""
        engine = LiabilityEngine()
        
        entry = engine.create_audit_entry(
            ActionExecution(
                action_id="ACTION_001",
                agent_id="agent_001",
                action_type="execute",
                parameters={},
                value=100.0,
                timestamp=datetime.now(),
                proposed_by="test"
            ),
            ContractBounds(
                contract_id="CONTRACT_001",
                agent_id="agent_001",
                action_type="execute",
                max_value_limit=10000.0,
                allowed_operations=["execute"],
                prohibited_operations=[],
                liability_level=LiabilityLevel.MEDIUM,
                audit_required=True,
                expiration_date=None,
                signer_public_key="key",
                terms={}
            ),
            ContractStatus.VALID,
            LiabilityLevel.MEDIUM
        )
        
        trail = engine.get_audit_trail()
        
        assert len(trail) == 1
        assert trail[0].action_id == "ACTION_001"


class TestContractManager:
    """Tests for ContractManager."""
    
    def test_create_contract(self):
        """Test creating a contract."""
        manager = ContractManager()
        
        contract = manager.create_contract(
            agent_id="agent_001",
            action_type="execute",
            max_value=5000.0,
            allowed_ops=["execute", "validate"],
            prohibited_ops=["delete"],
            liability=LiabilityLevel.MEDIUM,
            audit_required=True
        )
        
        assert contract.contract_id is not None
        assert contract.agent_id == "agent_001"
    
    def test_validate_and_execute_success(self):
        """Test successful validation."""
        manager = ContractManager()
        
        # Create contract
        manager.create_contract(
            agent_id="agent_001",
            action_type="execute",
            max_value=10000.0,
            allowed_ops=["execute", "validate"],
            prohibited_ops=[],
            liability=LiabilityLevel.MEDIUM,
            audit_required=True
        )
        
        # Create action
        action = ActionExecution(
            action_id="ACTION_001",
            agent_id="agent_001",
            action_type="execute",
            parameters={},
            value=500.0,
            timestamp=datetime.now(),
            proposed_by="test"
        )
        
        success, reason, audit = manager.validate_and_execute("agent_001", action)
        
        assert success is True
        assert audit is not None
    
    def test_validate_and_execute_fail(self):
        """Test failed validation."""
        manager = ContractManager()
        
        # Create contract
        manager.create_contract(
            agent_id="agent_001",
            action_type="execute",
            max_value=10000.0,
            allowed_ops=["execute"],
            prohibited_ops=["delete"],
            liability=LiabilityLevel.MEDIUM,
            audit_required=True
        )
        
        # Create prohibited action
        action = ActionExecution(
            action_id="ACTION_001",
            agent_id="agent_001",
            action_type="delete",
            parameters={},
            value=100.0,
            timestamp=datetime.now(),
            proposed_by="test"
        )
        
        success, reason, audit = manager.validate_and_execute("agent_001", action)
        
        assert success is False
    
    def test_get_agent_contracts(self):
        """Test getting agent contracts."""
        manager = ContractManager()
        
        manager.create_contract(
            agent_id="agent_001",
            action_type="execute",
            max_value=5000.0,
            allowed_ops=["execute"],
            prohibited_ops=[],
            liability=LiabilityLevel.MEDIUM,
            audit_required=True
        )
        
        contracts = manager.get_agent_contracts("agent_001")
        
        assert len(contracts) == 1
    
    def test_generate_chain_of_custody(self):
        """Test generating chain of custody report."""
        manager = ContractManager()
        
        # Add some entries
        manager.create_contract(
            agent_id="agent_001",
            action_type="execute",
            max_value=10000.0,
            allowed_ops=["execute"],
            prohibited_ops=[],
            liability=LiabilityLevel.MEDIUM,
            audit_required=True
        )
        
        action = ActionExecution(
            action_id="ACTION_001",
            agent_id="agent_001",
            action_type="execute",
            parameters={},
            value=500.0,
            timestamp=datetime.now(),
            proposed_by="test"
        )
        manager.validate_and_execute("agent_001", action)
        
        report = manager.generate_chain_of_custody_report()
        
        assert 'total_entries' in report
        assert 'by_status' in report
        assert 'by_liability' in report
