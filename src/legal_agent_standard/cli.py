"""Command-line interface for Legal Agent Standard."""

import click
import json
from typing import Optional

from .agent_engine import (
    ContractManager,
    ContractBounds,
    ActionExecution,
    AuditLogEntry,
    ContractStatus,
    LiabilityLevel
)


@click.group()
@click.version_option(version="0.1.0", prog_name="legal-agent")
def main() -> None:
    """Legal Agent Standard - Legally binding open standard for autonomous contract agents."""
    pass


@main.command()
@click.option("--agent", "-a", required=True, help="Agent ID")
@click.option("--action", "-t", required=True, help="Action type")
@click.option("--max-value", "-m", default=10000.0, help="Maximum value limit")
@click.option("--liability", "-l", type=click.Choice(["low", "medium", "high", "critical"]),
              default="medium", help="Liability level")
@click.option("--audit", "-u", is_flag=True, default=True, help="Require audit")
@click.option("--days", "-d", default=30, help="Expiration days")
def create_contract(agent: str, action: str, max_value: float,
                    liability: str, audit: bool, days: int) -> None:
    """Create a new contract with execution bounds."""
    manager = ContractManager()
    
    liability_enum = LiabilityLevel[liability.upper()]
    
    # Define allowed and prohibited operations
    allowed_ops = ["execute", "validate", "approve"]
    prohibited_ops = ["delete", "destroy", "alter"]
    
    contract = manager.create_contract(
        agent_id=agent,
        action_type=action,
        max_value=max_value,
        allowed_ops=allowed_ops,
        prohibited_ops=prohibited_ops,
        liability=liability_enum,
        audit_required=audit,
        expiration_days=days
    )
    
    click.echo(f"\n✅ Contract Created!")
    click.echo(f"   ID: {contract.contract_id}")
    click.echo(f"   Agent: {contract.agent_id}")
    click.echo(f"   Action: {contract.action_type}")
    click.echo(f"   Max Value: ${contract.max_value_limit:,.2f}")
    click.echo(f"   Liability: {contract.liability_level.value}")
    click.echo(f"   Audit Required: {contract.audit_required}")
    
    if contract.expiration_date:
        click.echo(f"   Expires: {contract.expiration_date.strftime('%Y-%m-%d')}")


@main.command()
@click.argument("agent_id")
def list_contracts(agent_id: str) -> None:
    """List all contracts for an agent."""
    manager = ContractManager()
    
    # Create some demo contracts first
    manager.create_contract(
        agent_id=agent_id,
        action_type="process_payment",
        max_value=5000.0,
        allowed_ops=["execute", "validate"],
        prohibited_ops=["delete"],
        liability=LiabilityLevel.MEDIUM,
        audit_required=True
    )
    
    contracts = manager.get_agent_contracts(agent_id)
    
    if not contracts:
        click.echo(f"No contracts found for agent: {agent_id}")
        return
    
    click.echo(f"\n📋 Contracts for Agent: {agent_id}")
    click.echo("=" * 60)
    
    for i, contract in enumerate(contracts, 1):
        click.echo(f"\n{i}. {contract['contract_id']}")
        click.echo(f"   Action: {contract['action_type']}")
        click.echo(f"   Max Value: ${contract['max_value_limit']:,.2f}")
        click.echo(f"   Liability: {contract['liability_level']}")
        click.echo(f"   Audit: {contract['audit_required']}")


@main.command()
@click.argument("agent_id")
@click.argument("action_type")
@click.option("--value", "-v", default=100.0, help="Action value")
@click.option("--test", "-t", is_flag=True, help="Run validation test")
def validate(agent_id: str, action_type: str, value: float, test: bool) -> None:
    """Validate an action against contracts."""
    manager = ContractManager()
    
    # Create contract first
    manager.create_contract(
        agent_id=agent_id,
        action_type=action_type,
        max_value=10000.0,
        allowed_ops=["execute", "validate", "approve"],
        prohibited_ops=["delete", "destroy"],
        liability=LiabilityLevel.MEDIUM,
        audit_required=True
    )
    
    # Create action
    action = ActionExecution(
        action_id=f"ACTION_{datetime.now().timestamp():.0f}",
        agent_id=agent_id,
        action_type=action_type,
        parameters={"test": "data"},
        value=value,
        timestamp=datetime.now(),
        proposed_by="test_agent"
    )
    
    # Validate
    success, reason, audit_entry = manager.validate_and_execute(agent_id, action)
    
    if success:
        click.echo(f"\n✅ Action Validated!")
        click.echo(f"   Agent: {agent_id}")
        click.echo(f"   Action: {action_type}")
        click.echo(f"   Value: ${value:,.2f}")
        click.echo(f"   Reason: {reason}")
        
        if audit_entry:
            click.echo(f"   Liability: {audit_entry.liability_assessment.value}")
    else:
        click.echo(f"\n❌ Validation Failed!")
        click.echo(f"   Reason: {reason}")


@main.command()
def audit() -> None:
    """Show audit trail and chain of custody."""
    manager = ContractManager()
    
    # Create some demo actions
    agent_id = "test_agent_001"
    
    manager.create_contract(
        agent_id=agent_id,
        action_type="process_payment",
        max_value=10000.0,
        allowed_ops=["execute", "validate"],
        prohibited_ops=["delete"],
        liability=LiabilityLevel.MEDIUM,
        audit_required=True
    )
    
    # Validate some actions
    for i in range(3):
        action = ActionExecution(
            action_id=f"ACTION_{i}",
            agent_id=agent_id,
            action_type="process_payment",
            parameters={"test": i},
            value=100.0 * (i + 1),
            timestamp=datetime.now(),
            proposed_by="test_agent"
        )
        manager.validate_and_execute(agent_id, action)
    
    # Show audit trail
    click.echo(f"\n📜 Audit Trail")
    click.echo("=" * 60)
    
    log_entries = manager._liability_engine.get_audit_trail()
    
    for i, entry in enumerate(log_entries, 1):
        click.echo(f"\n{i}. Log ID: {entry.log_id}")
        click.echo(f"   Action: {entry.action_id}")
        click.echo(f"   Contract: {entry.contract_id}")
        click.echo(f"   Status: {entry.validation_result.value}")
        click.echo(f"   Liability: {entry.liability_assessment.value}")
    
    # Show chain of custody
    click.echo(f"\n📊 Chain of Custody Report")
    click.echo("-" * 60)
    
    report = manager.generate_chain_of_custody_report()
    
    click.echo(f"Total Entries: {report['total_entries']}")
    click.echo(f"By Status: {report['by_status']}")
    click.echo(f"By Liability: {report['by_liability']}")
    click.echo(f"Generated: {report['generated_at']}")


@main.command()
def demo() -> None:
    """Run a contract validation demo."""
    click.echo("\n🧪 Legal Agent Standard Demo")
    click.echo("=" * 60)
    
    manager = ContractManager()
    
    # Create contracts
    click.echo("\n📝 Creating Contracts...")
    
    agent_id = "demo_agent_001"
    
    contract = manager.create_contract(
        agent_id=agent_id,
        action_type="process_payment",
        max_value=5000.0,
        allowed_ops=["execute", "validate", "approve"],
        prohibited_ops=["delete", "destroy"],
        liability=LiabilityLevel.MEDIUM,
        audit_required=True,
        expiration_days=30
    )
    
    click.echo(f"\n✅ Created: {contract.contract_id}")
    click.echo(f"   Max Value: ${contract.max_value_limit:,.2f}")
    click.echo(f"   Liability: {contract.liability_level.value}")
    
    # Validate actions
    click.echo(f"\n🔍 Validating Actions...")
    
    for value in [100.0, 500.0, 1000.0]:
        action = ActionExecution(
            action_id=f"DEMO_ACTION_{value}",
            agent_id=agent_id,
            action_type="process_payment",
            parameters={"amount": value},
            value=value,
            timestamp=datetime.now(),
            proposed_by="demo"
        )
        
        success, reason, audit = manager.validate_and_execute(agent_id, action)
        
        status = "✅" if success else "❌"
        liability = audit.liability_assessment.value if audit else "N/A"
        
        click.echo(f"\n{status} Action: ${value:,.2f}")
        click.echo(f"   Liability: {liability}")
    
    # Show report
    click.echo(f"\n📊 Chain of Custody Report")
    click.echo("=" * 60)
    
    report = manager.generate_chain_of_custody_report()
    click.echo(f"Total Actions: {report['total_entries']}")
    click.echo(f"By Liability: {report['by_liability']}")


def main_entry() -> None:
    """Main entry point."""
    main(prog_name="legal-agent")


if __name__ == "__main__":
    main_entry()
