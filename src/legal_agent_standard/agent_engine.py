"""Legal agent execution engine with cryptographic contract validation."""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import hashlib
import json
import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend


class ContractStatus(Enum):
    """Status of contract validation."""
    PENDING = "pending"
    VALID = "valid"
    INVALID = "invalid"
    EXPIRED = "expired"
    REVOKED = "revoked"


class LiabilityLevel(Enum):
    """Liability level for contract actions."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class ContractBounds:
    """Defines legal execution bounds for an agent."""
    contract_id: str
    agent_id: str
    action_type: str
    max_value_limit: float
    allowed_operations: List[str]
    prohibited_operations: List[str]
    liability_level: LiabilityLevel
    audit_required: bool
    expiration_date: Optional[datetime]
    signer_public_key: str
    terms: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "contract_id": self.contract_id,
            "agent_id": self.agent_id,
            "action_type": self.action_type,
            "max_value_limit": self.max_value_limit,
            "allowed_operations": self.allowed_operations,
            "prohibited_operations": self.prohibited_operations,
            "liability_level": self.liability_level.value,
            "audit_required": self.audit_required,
            "expiration_date": self.expiration_date.isoformat() if self.expiration_date else None,
            "signer_public_key": self.signer_public_key,
            "terms": self.terms
        }


@dataclass
class ActionExecution:
    """Represents a proposed agent action."""
    action_id: str
    agent_id: str
    action_type: str
    parameters: Dict[str, Any]
    value: float
    timestamp: datetime
    proposed_by: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "action_id": self.action_id,
            "agent_id": self.agent_id,
            "action_type": self.action_type,
            "parameters": self.parameters,
            "value": self.value,
            "timestamp": self.timestamp.isoformat(),
            "proposed_by": self.proposed_by
        }


@dataclass
class AuditLogEntry:
    """Entry in the audit log."""
    log_id: str
    action_id: str
    contract_id: str
    validation_result: ContractStatus
    liability_assessment: LiabilityLevel
    audit_trail: Dict[str, Any]
    timestamp: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "log_id": self.log_id,
            "action_id": self.action_id,
            "contract_id": self.contract_id,
            "validation_result": self.validation_result.value,
            "liability_assessment": self.liability_assessment.value,
            "audit_trail": self.audit_trail,
            "timestamp": self.timestamp.isoformat()
        }


class ContractValidator:
    """Validates contract bounds and signatures."""
    
    def __init__(self):
        """Initialize contract validator."""
        self._contracts: Dict[str, ContractBounds] = {}
        self._signing_keys: Dict[str, rsa.RSAPrivateKey] = {}
    
    def register_contract(self, contract: ContractBounds) -> bool:
        """
        Register a new contract.
        
        Args:
            contract: Contract bounds to register
            
        Returns:
            True if registered successfully
        """
        if contract.contract_id in self._contracts:
            return False
        
        self._contracts[contract.contract_id] = contract
        return True
    
    def verify_signature(self, contract_id: str, signature: str) -> bool:
        """
        Verify cryptographic signature of contract.
        
        Args:
            contract_id: Contract identifier
            signature: Base64 encoded signature
            
        Returns:
            True if signature is valid
        """
        contract = self._contracts.get(contract_id)
        if not contract:
            return False
        
        # In production, would verify against actual cryptographic signature
        # This is a simulation for demonstration
        return True
    
    def validate_action(self, action: ActionExecution, contract: ContractBounds) -> Tuple[bool, str]:
        """
        Validate action against contract bounds.
        
        Args:
            action: Proposed action
            contract: Contract bounds
            
        Returns:
            Tuple of (is_valid, reason)
        """
        # Check if action type is allowed
        if action.action_type not in contract.allowed_operations:
            return False, f"Action type '{action.action_type}' not allowed"
        
        # Check if action type is prohibited
        if action.action_type in contract.prohibited_operations:
            return False, f"Action type '{action.action_type}' is prohibited"
        
        # Check value limit
        if action.value > contract.max_value_limit:
            return False, f"Action value {action.value} exceeds limit {contract.max_value_limit}"
        
        # Check expiration
        if contract.expiration_date and action.timestamp > contract.expiration_date:
            return False, "Contract has expired"
        
        return True, "Action validated successfully"


class LiabilityEngine:
    """Manages liability assessment and chain of custody."""
    
    def __init__(self):
        """Initialize liability engine."""
        self._audit_logs: List[AuditLogEntry] = []
        self._liability_thresholds = {
            LiabilityLevel.LOW: 1000.0,
            LiabilityLevel.MEDIUM: 10000.0,
            LiabilityLevel.HIGH: 100000.0,
            LiabilityLevel.CRITICAL: 1000000.0
        }
    
    def assess_liability(self, action: ActionExecution, contract: ContractBounds) -> LiabilityLevel:
        """
        Assess liability level for an action.
        
        Args:
            action: Action to assess
            contract: Contract bounds
            
        Returns:
            LiabilityLevel
        """
        # Base liability from contract
        base_level = contract.liability_level
        
        # Adjust based on action value
        value = action.value
        if value > self._liability_thresholds[LiabilityLevel.CRITICAL]:
            return LiabilityLevel.CRITICAL
        elif value > self._liability_thresholds[LiabilityLevel.HIGH]:
            return LiabilityLevel.HIGH
        elif value > self._liability_thresholds[LiabilityLevel.MEDIUM]:
            return LiabilityLevel.MEDIUM
        else:
            return base_level
    
    def create_audit_entry(self, 
                          action: ActionExecution,
                          contract: ContractBounds,
                          validation_result: ContractStatus,
                          liability_assessment: LiabilityLevel) -> AuditLogEntry:
        """
        Create audit log entry.
        
        Args:
            action: Action being logged
            contract: Contract bounds
            validation_result: Validation result
            liability_assessment: Liability assessment
            
        Returns:
            AuditLogEntry
        """
        log_id = f"LOG_{len(self._audit_logs) + 1}_{datetime.now().timestamp():.0f}"
        
        entry = AuditLogEntry(
            log_id=log_id,
            action_id=action.action_id,
            contract_id=contract.contract_id,
            validation_result=validation_result,
            liability_assessment=liability_assessment,
            audit_trail={
                "action": action.to_dict(),
                "contract": contract.contract_id,
                "validated_at": datetime.now().isoformat()
            },
            timestamp=datetime.now()
        )
        
        self._audit_logs.append(entry)
        return entry
    
    def get_audit_trail(self) -> List[AuditLogEntry]:
        """Get complete audit trail."""
        return self._audit_logs.copy()
    
    def generate_chain_of_custody(self) -> Dict[str, Any]:
        """
        Generate chain of custody report.
        
        Returns:
            Chain of custody summary
        """
        total_actions = len(self._audit_logs)
        by_status = {}
        by_liability = {}
        
        for entry in self._audit_logs:
            status = entry.validation_result.value
            by_status[status] = by_status.get(status, 0) + 1
            
            liability = entry.liability_assessment.value
            by_liability[liability] = by_liability.get(liability, 0) + 1
        
        return {
            "total_entries": total_actions,
            "by_status": by_status,
            "by_liability": by_liability,
            "generated_at": datetime.now().isoformat()
        }


class ContractManager:
    """Manages contracts and agent permissions."""
    
    def __init__(self):
        """Initialize contract manager."""
        self._validator = ContractValidator()
        self._liability_engine = LiabilityEngine()
        self._agent_contracts: Dict[str, List[str]] = {}
    
    def create_contract(self,
                       agent_id: str,
                       action_type: str,
                       max_value: float,
                       allowed_ops: List[str],
                       prohibited_ops: List[str],
                       liability: LiabilityLevel,
                       audit_required: bool,
                       expiration_days: Optional[int] = None) -> ContractBounds:
        """
        Create a new contract with execution bounds.
        
        Args:
            agent_id: Agent identifier
            action_type: Type of action allowed
            max_value: Maximum value limit
            allowed_ops: List of allowed operations
            prohibited_ops: List of prohibited operations
            liability: Liability level
            audit_required: Whether audit is required
            expiration_days: Days until expiration (optional)
            
        Returns:
            Created ContractBounds
        """
        import random
        
        contract_id = f"CONTRACT_{len(self._agent_contracts) + 1}_{datetime.now().timestamp():.0f}"
        
        # Generate timestamp
        if expiration_days:
            expiration = datetime.now()
            from datetime import timedelta
            expiration = expiration + timedelta(days=expiration_days)
        else:
            expiration = None
        
        # Create contract bounds
        contract = ContractBounds(
            contract_id=contract_id,
            agent_id=agent_id,
            action_type=action_type,
            max_value_limit=max_value,
            allowed_operations=allowed_ops,
            prohibited_operations=prohibited_ops,
            liability_level=liability,
            audit_required=audit_required,
            expiration_date=expiration,
            signer_public_key="DUMMY_PUBLIC_KEY",
            terms={
                "created_at": datetime.now().isoformat(),
                "version": "1.0"
            }
        )
        
        # Register contract
        if self._validator.register_contract(contract):
            # Link to agent
            if agent_id not in self._agent_contracts:
                self._agent_contracts[agent_id] = []
            self._agent_contracts[agent_id].append(contract_id)
        
        return contract
    
    def validate_and_execute(self, agent_id: str, action: ActionExecution) -> Tuple[bool, str, Optional[AuditLogEntry]]:
        """
        Validate action against agent's contracts and execute.
        
        Args:
            agent_id: Agent identifier
            action: Proposed action
            
        Returns:
            Tuple of (success, reason, audit_entry)
        """
        # Get agent's contracts
        agent_contract_ids = self._agent_contracts.get(agent_id, [])
        
        if not agent_contract_ids:
            return False, "No contracts found for agent", None
        
        # Find matching contract
        for contract_id in agent_contract_ids:
            contract = self._validator._contracts.get(contract_id)
            if contract:
                # Validate action
                is_valid, reason = self._validator.validate_action(action, contract)
                
                if is_valid:
                    # Assess liability
                    liability = self._liability_engine.assess_liability(action, contract)
                    
                    # Create audit entry
                    audit_entry = self._liability_engine.create_audit_entry(
                        action, contract, ContractStatus.VALID, liability
                    )
                    
                    return True, reason, audit_entry
        
        return False, "No matching contract found", None
    
    def get_agent_contracts(self, agent_id: str) -> List[Dict[str, Any]]:
        """Get all contracts for an agent."""
        agent_contract_ids = self._agent_contracts.get(agent_id, [])
        return [
            self._validator._contracts[cid].to_dict()
            for cid in agent_contract_ids
            if cid in self._validator._contracts
        ]
    
    def generate_chain_of_custody_report(self) -> Dict[str, Any]:
        """Generate chain of custody report."""
        return self._liability_engine.generate_chain_of_custody()
