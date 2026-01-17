#!/usr/bin/env python3
"""
Sandbox Environment Manager
Manages demo and paper trading platforms for testing
Integrates with AgentX5 and Quantum AI System

Features:
- Activate demo accounts
- Manage sandbox environments
- Compatible with paper trading platforms
- Integration with quantum_ai_system.py
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('SandboxManager')


class SandboxEnvironmentManager:
    """
    Manages demo and paper trading environments
    Activates accounts and ensures compatibility with sandbox platforms
    """

    def __init__(self):
        """Initialize Sandbox Environment Manager"""
        self.config_dir = Path(__file__).parent / 'config'
        self.accounts_config = self._load_accounts_config()
        self.active_accounts = []
        self.sandbox_status = {
            'initialized': datetime.now().isoformat(),
            'demo_accounts': 0,
            'paper_accounts': 0,
            'sandbox_accounts': 0,
            'total_active': 0
        }
        logger.info("=" * 70)
        logger.info("🎮 SANDBOX ENVIRONMENT MANAGER INITIALIZED")
        logger.info("=" * 70)

    def _load_accounts_config(self) -> Dict:
        """Load multi-account configuration"""
        config_file = self.config_dir / 'multi_account_config.json'
        
        if not config_file.exists():
            logger.warning("⚠️ Multi-account config not found, using defaults")
            return self._create_default_config()
        
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            logger.info(f"✅ Loaded configuration for {config.get('total_accounts', 0)} accounts")
            return config
        except Exception as e:
            logger.error(f"❌ Error loading config: {e}")
            return self._create_default_config()

    def _create_default_config(self) -> Dict:
        """Create default configuration for demo/paper trading"""
        return {
            "description": "Demo and paper trading configuration",
            "total_accounts": 0,
            "accounts": [],
            "monitoring": {
                "check_interval_seconds": 60,
                "performance_tracking": True,
                "daily_reports": True
            }
        }

    def activate_demo_accounts(self) -> Dict[str, Any]:
        """
        Activate all demo and paper trading accounts
        
        Returns:
            Dict with activation status and account details
        """
        logger.info("\n" + "=" * 70)
        logger.info("🚀 ACTIVATING DEMO AND PAPER TRADING ACCOUNTS")
        logger.info("=" * 70 + "\n")

        activation_results = {
            'timestamp': datetime.now().isoformat(),
            'activated_accounts': [],
            'failed_accounts': [],
            'summary': {}
        }

        accounts = self.accounts_config.get('accounts', [])
        
        for account in accounts:
            try:
                # Activate accounts in paper or sandbox environments
                if account.get('environment') in ['paper', 'sandbox', 'demo']:
                    if account.get('enabled', True):
                        activated = self._activate_single_account(account)
                        if activated:
                            self.active_accounts.append(account)
                            activation_results['activated_accounts'].append({
                                'id': account.get('id'),
                                'name': account.get('name'),
                                'environment': account.get('environment'),
                                'capital': account.get('initial_capital'),
                                'status': 'ACTIVE'
                            })
                            
                            # Update counters
                            env = account.get('environment')
                            if env == 'paper':
                                self.sandbox_status['paper_accounts'] += 1
                            elif env == 'sandbox':
                                self.sandbox_status['sandbox_accounts'] += 1
                            elif env == 'demo':
                                self.sandbox_status['demo_accounts'] += 1
                        else:
                            activation_results['failed_accounts'].append(account.get('id'))
                            
            except Exception as e:
                logger.error(f"❌ Failed to activate {account.get('id')}: {e}")
                activation_results['failed_accounts'].append(account.get('id'))

        # Update total active
        self.sandbox_status['total_active'] = len(self.active_accounts)

        # Prepare summary
        activation_results['summary'] = {
            'total_activated': len(activation_results['activated_accounts']),
            'total_failed': len(activation_results['failed_accounts']),
            'paper_accounts': self.sandbox_status['paper_accounts'],
            'sandbox_accounts': self.sandbox_status['sandbox_accounts'],
            'demo_accounts': self.sandbox_status['demo_accounts'],
            'total_capital': sum(acc.get('initial_capital', 0) for acc in self.active_accounts)
        }

        logger.info("\n" + "=" * 70)
        logger.info("📊 ACTIVATION SUMMARY")
        logger.info("=" * 70)
        logger.info(f"✅ Total Activated: {activation_results['summary']['total_activated']}")
        logger.info(f"📄 Paper Trading Accounts: {self.sandbox_status['paper_accounts']}")
        logger.info(f"🏖️  Sandbox Accounts: {self.sandbox_status['sandbox_accounts']}")
        logger.info(f"🎮 Demo Accounts: {self.sandbox_status['demo_accounts']}")
        logger.info(f"💰 Total Capital: ${activation_results['summary']['total_capital']:,.2f}")
        
        if activation_results['failed_accounts']:
            logger.warning(f"⚠️  Failed Accounts: {len(activation_results['failed_accounts'])}")
        
        logger.info("=" * 70 + "\n")

        return activation_results

    def _activate_single_account(self, account: Dict) -> bool:
        """
        Activate a single demo/paper trading account
        
        Note: This is a sandbox/demo implementation that validates account configuration.
        For production use with live APIs, implement:
        1. Broker API connection
        2. Account credential verification
        3. Trading session initialization
        4. Risk parameter configuration
        
        Args:
            account: Account configuration dictionary
            
        Returns:
            bool: True if activated successfully
        """
        account_id = account.get('id', 'UNKNOWN')
        account_name = account.get('name', 'UNKNOWN')
        environment = account.get('environment', 'unknown')
        
        try:
            logger.info(f"🔄 Activating {account_name} ({account_id}) in {environment.upper()}")
            
            # Simulate account activation
            # In a real implementation, this would:
            # 1. Connect to broker API
            # 2. Verify account credentials
            # 3. Initialize trading session
            # 4. Set up risk parameters
            
            # For now, we just validate the account structure
            required_fields = ['id', 'name', 'environment', 'initial_capital']
            if all(field in account for field in required_fields):
                logger.info(f"✅ {account_name} activated successfully")
                return True
            else:
                logger.error(f"❌ {account_name} missing required fields")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error activating {account_name}: {e}")
            return False

    def get_active_accounts(self, environment: Optional[str] = None) -> List[Dict]:
        """
        Get list of active accounts, optionally filtered by environment
        
        Args:
            environment: Filter by environment type (paper, sandbox, demo)
            
        Returns:
            List of active account dictionaries
        """
        if environment:
            return [acc for acc in self.active_accounts if acc.get('environment') == environment]
        return self.active_accounts

    def verify_sandbox_compatibility(self) -> Dict[str, Any]:
        """
        Verify that sandbox environment is properly configured
        
        Returns:
            Dict with compatibility check results
        """
        logger.info("\n" + "=" * 70)
        logger.info("🔍 VERIFYING SANDBOX COMPATIBILITY")
        logger.info("=" * 70 + "\n")

        compatibility_checks = {
            'timestamp': datetime.now().isoformat(),
            'checks': [],
            'compatible': True
        }

        # Check 1: Configuration file exists
        config_exists = (self.config_dir / 'multi_account_config.json').exists()
        compatibility_checks['checks'].append({
            'name': 'Configuration File',
            'status': 'PASS' if config_exists else 'FAIL',
            'critical': True
        })
        if not config_exists:
            compatibility_checks['compatible'] = False

        # Check 2: At least one account configured
        has_accounts = len(self.accounts_config.get('accounts', [])) > 0
        compatibility_checks['checks'].append({
            'name': 'Accounts Configured',
            'status': 'PASS' if has_accounts else 'FAIL',
            'critical': True
        })
        if not has_accounts:
            compatibility_checks['compatible'] = False

        # Check 3: Demo/Paper/Sandbox accounts available
        demo_paper_accounts = [
            acc for acc in self.accounts_config.get('accounts', [])
            if acc.get('environment') in ['paper', 'sandbox', 'demo']
        ]
        has_demo_accounts = len(demo_paper_accounts) > 0
        compatibility_checks['checks'].append({
            'name': 'Demo/Paper Accounts Available',
            'status': 'PASS' if has_demo_accounts else 'FAIL',
            'critical': True,
            'details': f'{len(demo_paper_accounts)} accounts found'
        })
        if not has_demo_accounts:
            compatibility_checks['compatible'] = False

        # Check 4: Risk profiles configured
        risk_profiles_file = self.config_dir / 'trading_risk_profiles.json'
        risk_profiles_exist = risk_profiles_file.exists()
        compatibility_checks['checks'].append({
            'name': 'Risk Profiles',
            'status': 'PASS' if risk_profiles_exist else 'WARN',
            'critical': False
        })

        # Log results
        for check in compatibility_checks['checks']:
            status_icon = '✅' if check['status'] == 'PASS' else '⚠️' if check['status'] == 'WARN' else '❌'
            logger.info(f"{status_icon} {check['name']}: {check['status']}")
            if 'details' in check:
                logger.info(f"   └─ {check['details']}")

        logger.info("\n" + "=" * 70)
        if compatibility_checks['compatible']:
            logger.info("✅ SANDBOX ENVIRONMENT IS COMPATIBLE")
        else:
            logger.error("❌ SANDBOX ENVIRONMENT COMPATIBILITY ISSUES DETECTED")
        logger.info("=" * 70 + "\n")

        return compatibility_checks

    def get_status(self) -> Dict[str, Any]:
        """Get current status of sandbox environment"""
        return {
            'status': self.sandbox_status,
            'active_accounts': len(self.active_accounts),
            'total_configured': len(self.accounts_config.get('accounts', []))
        }


def main():
    """Demo of Sandbox Environment Manager"""
    print("""
    ╔═══════════════════════════════════════════════════════════════════╗
    ║           SANDBOX ENVIRONMENT MANAGER                             ║
    ║        Demo & Paper Trading Platform Activation                   ║
    ╚═══════════════════════════════════════════════════════════════════╝
    """)

    # Initialize manager
    manager = SandboxEnvironmentManager()

    # Verify compatibility
    compatibility = manager.verify_sandbox_compatibility()

    if compatibility['compatible']:
        # Activate all demo accounts
        results = manager.activate_demo_accounts()

        # Show status
        status = manager.get_status()
        print(f"\n📊 Current Status:")
        print(f"   Active Accounts: {status['active_accounts']}")
        print(f"   Total Configured: {status['total_configured']}")
        print(f"   Paper Accounts: {status['status']['paper_accounts']}")
        print(f"   Sandbox Accounts: {status['status']['sandbox_accounts']}")
        print(f"   Demo Accounts: {status['status']['demo_accounts']}")
    else:
        print("\n⚠️  Cannot activate accounts - compatibility issues detected")
        print("   Please check configuration files")


if __name__ == "__main__":
    main()
