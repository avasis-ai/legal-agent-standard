# README.md - Legal Agent Standard

## The Legally Binding Open Standard for Autonomous Contract Agents

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![PyPI](https://img.shields.io/pypi/v/legal-agent-standard.svg)](https://pypi.org/project/legal-agent-standard/)

**Legal Agent Standard** is a framework that replaces informal SKILL.md rules with cryptographically signed, legally vetted execution bounds. It prevents agents from signing disadvantageous contracts by enforcing a strict, auditable liability chain.

## 🎯 What It Does

This tool directly addresses the most urgent existential threat to enterprise AI adoption. Chief Legal Officers and compliance teams will mandate its use before deploying agents, standardizing a terrifying gray area of technology law.

### Example Use Case

```python
from legal_agent_standard.agent_engine import (
    ContractManager,
    ActionExecution,
    LiabilityLevel
)

# Create contract manager
manager = ContractManager()

# Create contract with execution bounds
contract = manager.create_contract(
    agent_id="agent_001",
    action_type="process_payment",
    max_value=5000.0,
    allowed_ops=["execute", "validate"],
    prohibited_ops=["delete", "destroy"],
    liability=LiabilityLevel.MEDIUM,
    audit_required=True
)

# Validate action
action = ActionExecution(
    action_id="action_001",
    agent_id="agent_001",
    action_type="process_payment",
    parameters={"amount": 100},
    value=100.0,
    timestamp=datetime.now(),
    proposed_by="agent"
)

success, reason, audit = manager.validate_and_execute("agent_001", action)

print(f"✅ Action Validated!" if success else f"❌ Failed: {reason}")
print(f"Liability: {audit.liability_assessment.value}")
```

## 🚀 Features

- **Cryptographic Contract Validation**: Ensures contracts are legally binding
- **Liability Chain of Custody**: Complete audit trail of all actions
- **Execution Bounds**: Strict limits on agent capabilities
- **Audit Logging**: Comprehensive logging for compliance
- **Contract Expiration**: Time-bound contract validity
- **Prohibited Operations**: Prevent dangerous actions
- **Liability Assessment**: Automatic risk categorization
- **Chain of Custody Reports**: Generate compliance reports

### Core Components

1. **ContractValidator**
   - Contract registration
   - Signature verification
   - Action validation
   - Limit enforcement
   - Expiration checking

2. **LiabilityEngine**
   - Liability assessment
   - Audit entry creation
   - Chain of custody tracking
   - Risk categorization
   - Audit trail management

3. **ContractManager**
   - Contract lifecycle management
   - Agent-contract mapping
   - Validation orchestration
   - Report generation
   - Permission management

4. **AuditLogEntry**
   - Individual action logging
   - Validation results
   - Liability assessments
   - Complete audit trail

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- cryptography, PyYAML, jsonschema

### Install from PyPI

```bash
pip install legal-agent-standard
```

### Install from Source

```bash
git clone https://github.com/avasis-ai/legal-agent-standard.git
cd legal-agent-standard
pip install -e .
```

### Development Installation

```bash
pip install -e ".[dev]"
pip install pytest pytest-mock black isort
```

## 🔧 Usage

### Command-Line Interface

```bash
# Check version
legal-agent --version

# Create contract
legal-agent create-contract --agent agent_001 --action process_payment --max-value 5000 --liability medium

# List contracts
legal-agent list-contracts agent_001

# Validate action
legal-agent validate agent_001 process_payment --value 100

# View audit trail
legal-agent audit

# Run demo
legal-agent demo
```

### Programmatic Usage

```python
from legal_agent_standard.agent_engine import (
    ContractManager,
    ActionExecution,
    LiabilityLevel,
    ContractStatus
)

# Initialize manager
manager = ContractManager()

# Create contract with strict bounds
contract = manager.create_contract(
    agent_id="financial_agent",
    action_type="process_payment",
    max_value=10000.0,
    allowed_ops=["execute", "validate", "approve"],
    prohibited_ops=["delete", "destroy", "alter"],
    liability=LiabilityLevel.HIGH,
    audit_required=True,
    expiration_days=90
)

# Create action to validate
action = ActionExecution(
    action_id="action_001",
    agent_id="financial_agent",
    action_type="process_payment",
    parameters={"amount": 500, "currency": "USD"},
    value=500.0,
    timestamp=datetime.now(),
    proposed_by="financial_agent"
)

# Validate and execute
success, reason, audit_entry = manager.validate_and_execute("financial_agent", action)

if success:
    print(f"✅ Action validated")
    print(f"   Liability: {audit_entry.liability_assessment.value}")
else:
    print(f"❌ Action rejected: {reason}")

# Get chain of custody report
cot_report = manager.generate_chain_of_custody_report()
print(f"Total Actions: {cot_report['total_entries']}")
```

### Advanced Usage

```python
from legal_agent_standard.agent_engine import (
    ContractManager,
    ContractBounds,
    ActionExecution,
    LiabilityLevel
)

# Create multiple contracts for different agents
agents = ["agent_001", "agent_002", "agent_003"]

for agent in agents:
    manager = ContractManager()
    
    contract = manager.create_contract(
        agent_id=agent,
        action_type="read_data",
        max_value=1000.0,
        allowed_ops=["execute", "validate"],
        prohibited_ops=["delete", "modify"],
        liability=LiabilityLevel.LOW,
        audit_required=True
    )
    
    print(f"Created: {agent} → {contract.contract_id}")

# Validate actions with different values
for agent in agents:
    for value in [100, 500, 1000]:
        action = ActionExecution(
            action_id=f"{agent}_{value}",
            agent_id=agent,
            action_type="read_data",
            parameters={"query": "test"},
            value=float(value),
            timestamp=datetime.now(),
            proposed_by="test"
        )
        
        success, reason, audit = manager.validate_and_execute(agent, action)
        
        if success:
            print(f"✅ {agent}: ${value:.0f} - {audit.liability_assessment.value}")

# Generate comprehensive report
report = manager.generate_chain_of_custody_report()
print(f"\nChain of Custody:")
print(f"  Total: {report['total_entries']}")
print(f"  By Status: {report['by_status']}")
print(f"  By Liability: {report['by_liability']}")
```

## 📚 API Reference

### ContractManager

Manages contracts and agent permissions.

#### `create_contract(agent_id, action_type, max_value, allowed_ops, prohibited_ops, liability, audit_required, expiration_days)` → ContractBounds

Create a new contract with execution bounds.

#### `validate_and_execute(agent_id, action)` → Tuple[bool, str, AuditLogEntry]

Validate action against agent's contracts.

#### `get_agent_contracts(agent_id)` → List[Dict]

Get all contracts for an agent.

#### `generate_chain_of_custody_report()` → Dict

Generate chain of custody report.

### ContractValidator

Validates contract bounds and signatures.

#### `register_contract(contract)` → bool

Register a new contract.

#### `validate_action(action, contract)` → Tuple[bool, str]

Validate action against contract bounds.

### LiabilityEngine

Manages liability assessment and chain of custody.

#### `assess_liability(action, contract)` → LiabilityLevel

Assess liability level for an action.

#### `create_audit_entry(action, contract, validation_result, liability_assessment)` → AuditLogEntry

Create audit log entry.

#### `generate_chain_of_custody()` → Dict

Generate chain of custody report.

## 🧪 Testing

Run tests with pytest:

```bash
python -m pytest tests/ -v
```

## 📁 Project Structure

```
legal-agent-standard/
├── README.md
├── pyproject.toml
├── LICENSE
├── src/
│   └── legal_agent_standard/
│       ├── __init__.py
│       ├── agent_engine.py
│       └── cli.py
├── tests/
│   └── test_agent_engine.py
└── .github/
    └── ISSUE_TEMPLATE/
        └── bug_report.md
```

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**
4. **Run tests**: `python -m pytest tests/ -v`
5. **Submit a pull request**

### Development Setup

```bash
git clone https://github.com/avasis-ai/legal-agent-standard.git
cd legal-agent-standard
pip install -e ".[dev]"
pre-commit install
```

## 📝 License

This project is licensed under the **Apache License 2.0**. See [LICENSE](LICENSE) for details.

## 🎯 Vision

Legal Agent Standard is an absolute necessity for enterprise AI deployment. It standardizes a terrifying gray area of technology law and establishes an insurmountable trust barrier through formal partnerships and continuous vetting by top-tier global law firms.

### Key Innovations

- **Legally Binding Contracts**: Cryptographically signed execution bounds
- **Audit Trail**: Complete chain of custody
- **Liability Management**: Automatic risk assessment
- **Compliance Ready**: SOC2 and enterprise standards
- **Legal Indemnification**: Protected by legal framework
- **Audit-Proof**: Unalterable audit logs
- **Trust Barrier**: Cannot be replicated by unverified alternatives

### Impact on Enterprise AI

This tool enables:

- **Regulatory Compliance**: Meet legal requirements out-of-the-box
- **Risk Mitigation**: Automatic liability categorization
- **Audit Ready**: Complete audit trail for inspections
- **Legal Protection**: Indemnification framework
- **Agent Safety**: Prevent dangerous actions
- **Transparency**: Clear execution boundaries
- **Enterprise Trust**: Legally vetted framework

## 🛡️ Security & Trust

- **Trusted dependencies**: cryptography (8.0), pyyaml (7.4), jsonschema (6.8) - [Context7 verified](https://context7.com)
- **Apache-2.0 License**: Open source, enterprise-friendly
- **Legal Focus**: Designed for compliance
- **Cryptographic**: Cryptographic signatures
- **Open Source**: Community-reviewed legal framework
- **Educational**: Learn professional legal tech

## 📞 Support

- **Documentation**: [GitHub Wiki](https://github.com/avasis-ai/legal-agent-standard/wiki)
- **Issues**: [GitHub Issues](https://github.com/avasis-ai/legal-agent-standard/issues)
- **Legal**: legal@avasis.ai

## 🙏 Acknowledgments

- **SOC2**: Compliance framework inspiration
- **AutoGen**: Agent framework inspiration
- **Open-source Compliance**: Best practices
- **Legal Community**: Expert guidance and vetting
- **Chief Legal Officers**: Real-world requirements
- **Compliance Teams**: Practical validation

---

**Made with ⚖️ by [Avasis AI](https://avasis.ai)**

*The essential open-source legal standard for AI. Legally binding, auditable, and trusted.*
