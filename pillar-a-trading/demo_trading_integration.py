#!/usr/bin/env python3
"""
Demo Trading Integration System
Integrates sandbox environment, strategies, and task automation with Quantum AI

This module brings together:
1. Sandbox Environment Manager (demo/paper trading)
2. Long and Short Trading Strategies
3. Task Automation Framework (100 tasks)
4. Quantum AI System integration

Features:
- Complete integration with existing quantum_ai_system.py
- Seamless operation in demo/paper/sandbox environments
- Automated testing of long and short strategies
- Execution of 100 predetermined tasks
"""

import sys
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

# Add paths for imports
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / 'ai-models'))
sys.path.insert(0, str(Path(__file__).parent / 'strategies'))

# Import our components
from sandbox_environment_manager import SandboxEnvironmentManager
from task_automation_framework import TaskAutomationFramework

# Import quantum AI
try:
    from quantum_ai_system import QuantumAISystem, QuantumVersion
    QUANTUM_AI_AVAILABLE = True
except ImportError:
    QUANTUM_AI_AVAILABLE = False
    logging.warning("Quantum AI System not available for import")

# Import strategies
try:
    from long_position_strategy import LongPositionStrategy
    LONG_STRATEGY_AVAILABLE = True
except ImportError:
    LONG_STRATEGY_AVAILABLE = False
    logging.warning("Long Position Strategy not available")

try:
    from big_short_strategy import BigShortStrategy
    SHORT_STRATEGY_AVAILABLE = True
except ImportError:
    SHORT_STRATEGY_AVAILABLE = False
    logging.warning("Big Short Strategy not available")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('DemoTradingIntegration')


class DemoTradingIntegration:
    """
    Complete integration system for demo trading, strategies, and automation
    """

    def __init__(self):
        """Initialize Demo Trading Integration System"""
        logger.info("=" * 70)
        logger.info("🚀 DEMO TRADING INTEGRATION SYSTEM")
        logger.info("   Initializing all components...")
        logger.info("=" * 70)

        # Initialize components
        self.sandbox_manager = SandboxEnvironmentManager()
        self.task_framework = TaskAutomationFramework(max_tasks=100)
        
        # Initialize Quantum AI if available
        if QUANTUM_AI_AVAILABLE:
            self.quantum_ai = QuantumAISystem(version=QuantumVersion.V4_0)
            logger.info("✅ Quantum AI System loaded (v4.0)")
        else:
            self.quantum_ai = None
            logger.warning("⚠️  Quantum AI System not available")

        # Initialize strategies
        if LONG_STRATEGY_AVAILABLE:
            self.long_strategy = LongPositionStrategy()
            logger.info("✅ Long Position Strategy loaded")
        else:
            self.long_strategy = None
            logger.warning("⚠️  Long Position Strategy not available")

        if SHORT_STRATEGY_AVAILABLE:
            self.short_strategy = BigShortStrategy()
            logger.info("✅ Big Short Strategy loaded")
        else:
            self.short_strategy = None
            logger.warning("⚠️  Big Short Strategy not available")

        self.integration_status = {
            'initialized': datetime.now().isoformat(),
            'sandbox_active': False,
            'strategies_loaded': 0,
            'quantum_ai_active': QUANTUM_AI_AVAILABLE,
            'tasks_ready': False
        }

        logger.info("=" * 70 + "\n")

    def activate_all_systems(self) -> Dict[str, Any]:
        """
        Activate all systems in the integration
        
        Returns:
            Dict with activation results
        """
        logger.info("\n" + "=" * 70)
        logger.info("🔄 ACTIVATING ALL SYSTEMS")
        logger.info("=" * 70 + "\n")

        results = {
            'timestamp': datetime.now().isoformat(),
            'components': []
        }

        # 1. Verify sandbox compatibility
        logger.info("Step 1: Verifying Sandbox Compatibility...")
        compatibility = self.sandbox_manager.verify_sandbox_compatibility()
        results['components'].append({
            'name': 'Sandbox Compatibility',
            'status': 'PASS' if compatibility['compatible'] else 'FAIL',
            'details': compatibility
        })

        # 2. Activate demo accounts
        if compatibility['compatible']:
            logger.info("\nStep 2: Activating Demo/Paper Trading Accounts...")
            activation = self.sandbox_manager.activate_demo_accounts()
            results['components'].append({
                'name': 'Account Activation',
                'status': 'SUCCESS',
                'details': activation['summary']
            })
            self.integration_status['sandbox_active'] = True
        else:
            logger.warning("\n⚠️  Skipping account activation due to compatibility issues")
            results['components'].append({
                'name': 'Account Activation',
                'status': 'SKIPPED',
                'details': 'Compatibility check failed'
            })

        # 3. Test strategies
        logger.info("\nStep 3: Testing Trading Strategies...")
        strategy_results = self._test_strategies()
        results['components'].append({
            'name': 'Strategy Testing',
            'status': 'SUCCESS' if strategy_results['tested'] > 0 else 'WARNING',
            'details': strategy_results
        })
        self.integration_status['strategies_loaded'] = strategy_results['tested']

        # 4. Generate automation tasks
        logger.info("\nStep 4: Generating Automation Tasks...")
        tasks = self.task_framework.generate_predetermined_tasks()
        results['components'].append({
            'name': 'Task Generation',
            'status': 'SUCCESS',
            'details': {
                'total_tasks': len(tasks),
                'task_categories': 8
            }
        })
        self.integration_status['tasks_ready'] = True

        # 5. Test Quantum AI integration
        if self.quantum_ai:
            logger.info("\nStep 5: Testing Quantum AI Integration...")
            quantum_test = self._test_quantum_ai()
            results['components'].append({
                'name': 'Quantum AI',
                'status': 'SUCCESS' if quantum_test['success'] else 'WARNING',
                'details': quantum_test
            })

        logger.info("\n" + "=" * 70)
        logger.info("✅ ALL SYSTEMS ACTIVATED")
        logger.info("=" * 70 + "\n")

        return results

    def _test_strategies(self) -> Dict[str, Any]:
        """Test both long and short strategies"""
        results = {
            'tested': 0,
            'long_strategy': None,
            'short_strategy': None
        }

        # Test data
        test_market_data = {
            'symbol': 'TEST',
            'pe_ratio': 12.5,
            'pb_ratio': 1.8,
            'roe': 20,
            'debt_equity': 0.9,
            'rsi': 45,
            'macd': 0.5,
            'macd_signal': 0.3,
            'volume_ratio': 1.3,
            'momentum': 0.02,
            'market_sentiment': 'bullish',
            'sector_strength': 65
        }

        # Test long strategy
        if self.long_strategy:
            try:
                signal = self.long_strategy.analyze_for_long('TEST', test_market_data)
                results['long_strategy'] = {
                    'status': 'TESTED',
                    'action': signal['action'],
                    'confidence': signal['confidence']
                }
                results['tested'] += 1
                logger.info(f"   ✅ Long Strategy: {signal['action']} (Confidence: {signal['confidence']:.1f}%)")
            except Exception as e:
                logger.error(f"   ❌ Long Strategy test failed: {e}")
                results['long_strategy'] = {'status': 'FAILED', 'error': str(e)}

        # Test short strategy
        if self.short_strategy:
            try:
                # Adjust data for short test (overvalued scenario)
                short_test_data = test_market_data.copy()
                short_test_data['pe_ratio'] = 60
                short_test_data['pb_ratio'] = 12
                short_test_data['rsi'] = 75
                
                signal = self.short_strategy.analyze_for_short('TEST', short_test_data)
                results['short_strategy'] = {
                    'status': 'TESTED',
                    'action': signal['action'],
                    'confidence': signal['confidence']
                }
                results['tested'] += 1
                logger.info(f"   ✅ Short Strategy: {signal['action']} (Confidence: {signal['confidence']:.1f}%)")
            except Exception as e:
                logger.error(f"   ❌ Short Strategy test failed: {e}")
                results['short_strategy'] = {'status': 'FAILED', 'error': str(e)}

        return results

    def _test_quantum_ai(self) -> Dict[str, Any]:
        """Test Quantum AI integration"""
        try:
            import numpy as np
            
            # Create test market data
            market_data = {
                'volatility': 0.25,
                'momentum': 0.5,
                'volume_ratio': 1.2,
                'price_data': np.random.randn(100).cumsum(),
                'streams': [
                    {'source': 'Technical', 'data': np.random.randn(50)},
                    {'source': 'Fundamental', 'data': np.random.randn(50)}
                ]
            }
            
            # Run quantum analysis
            result = self.quantum_ai.analyze_market(market_data)
            
            logger.info(f"   ✅ Quantum AI: {result['recommendation']} (Confidence: {result['confidence_level']:.1%})")
            
            return {
                'success': True,
                'recommendation': result['recommendation'],
                'confidence': result['confidence_level'],
                'version': result['version']
            }
        except Exception as e:
            logger.error(f"   ❌ Quantum AI test failed: {e}")
            return {
                'success': False,
                'error': str(e)
            }

    def execute_automation_loop(self, loop_count: int = 1) -> Dict[str, Any]:
        """
        Execute the complete automation loop
        
        Args:
            loop_count: Number of times to execute all tasks
            
        Returns:
            Dict with execution results
        """
        logger.info("\n" + "=" * 70)
        logger.info("🔁 STARTING AUTOMATION LOOP")
        logger.info(f"   Loop Count: {loop_count}")
        logger.info(f"   Total Tasks: {len(self.task_framework.tasks)}")
        logger.info("=" * 70 + "\n")

        # Execute all tasks
        summary = self.task_framework.execute_all_tasks(loop_count=loop_count)

        return summary

    def run_complete_demo(self) -> Dict[str, Any]:
        """
        Run complete demo: activate systems, test strategies, execute tasks
        
        Returns:
            Dict with complete demo results
        """
        logger.info("\n" + "=" * 70)
        logger.info("🎯 RUNNING COMPLETE DEMO")
        logger.info("=" * 70 + "\n")

        demo_results = {
            'timestamp': datetime.now().isoformat(),
            'phases': {}
        }

        # Phase 1: Activate all systems
        logger.info("📍 PHASE 1: System Activation")
        activation_results = self.activate_all_systems()
        demo_results['phases']['activation'] = activation_results

        # Phase 2: Test trading with sample data
        logger.info("\n📍 PHASE 2: Trading Strategy Test")
        trading_results = self._run_trading_test()
        demo_results['phases']['trading_test'] = trading_results

        # Phase 3: Execute automation tasks
        logger.info("\n📍 PHASE 3: Task Automation Execution")
        automation_results = self.execute_automation_loop(loop_count=1)
        demo_results['phases']['automation'] = automation_results

        # Final summary
        logger.info("\n" + "=" * 70)
        logger.info("🎉 COMPLETE DEMO FINISHED")
        logger.info("=" * 70)
        logger.info(f"✅ Sandbox Accounts Active: {self.integration_status['sandbox_active']}")
        logger.info(f"✅ Strategies Tested: {self.integration_status['strategies_loaded']}")
        logger.info(f"✅ Quantum AI Active: {self.integration_status['quantum_ai_active']}")
        logger.info(f"✅ Tasks Completed: {automation_results['completed']}/{automation_results['total_tasks']}")
        logger.info(f"📈 Success Rate: {automation_results['success_rate']:.1f}%")
        logger.info("=" * 70 + "\n")

        # Save demo results
        self._save_demo_results(demo_results)

        return demo_results

    def _run_trading_test(self) -> Dict[str, Any]:
        """Run a complete trading test cycle"""
        test_results = {
            'timestamp': datetime.now().isoformat(),
            'tests': []
        }

        # Get active accounts
        active_accounts = self.sandbox_manager.get_active_accounts()
        logger.info(f"Testing with {len(active_accounts)} active accounts")

        # Test with sample market scenarios
        scenarios = [
            {
                'name': 'Bullish Market',
                'data': {
                    'symbol': 'LONG_TEST',
                    'pe_ratio': 12,
                    'pb_ratio': 1.5,
                    'roe': 22,
                    'debt_equity': 0.7,
                    'rsi': 48,
                    'macd': 0.6,
                    'macd_signal': 0.4,
                    'volume_ratio': 1.5,
                    'momentum': 0.03,
                    'market_sentiment': 'bullish',
                    'sector_strength': 75
                }
            },
            {
                'name': 'Bearish Market',
                'data': {
                    'symbol': 'SHORT_TEST',
                    'pe_ratio': 65,
                    'pb_ratio': 15,
                    'roe': 5,
                    'debt_equity': 4,
                    'rsi': 78,
                    'macd': -0.5,
                    'macd_signal': -0.2,
                    'volume_ratio': 1.8,
                    'momentum': -0.02,
                    'market_sentiment': 'bearish',
                    'sector_strength': 25
                }
            }
        ]

        for scenario in scenarios:
            logger.info(f"\n   Testing: {scenario['name']}")
            scenario_result = {'scenario': scenario['name'], 'signals': []}

            # Test long strategy
            if self.long_strategy:
                long_signal = self.long_strategy.analyze_for_long(
                    scenario['data']['symbol'],
                    scenario['data']
                )
                scenario_result['signals'].append({
                    'strategy': 'Long',
                    'action': long_signal['action'],
                    'confidence': long_signal['confidence']
                })
                logger.info(f"      Long: {long_signal['action']} ({long_signal['confidence']:.1f}%)")

            # Test short strategy
            if self.short_strategy:
                short_signal = self.short_strategy.analyze_for_short(
                    scenario['data']['symbol'],
                    scenario['data']
                )
                scenario_result['signals'].append({
                    'strategy': 'Short',
                    'action': short_signal['action'],
                    'confidence': short_signal['confidence']
                })
                logger.info(f"      Short: {short_signal['action']} ({short_signal['confidence']:.1f}%)")

            test_results['tests'].append(scenario_result)

        return test_results

    def _save_demo_results(self, results: Dict[str, Any]):
        """Save demo results to file"""
        logs_dir = Path(__file__).parent.parent / 'logs'
        logs_dir.mkdir(exist_ok=True)
        
        results_file = logs_dir / f'demo_trading_integration_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"💾 Demo results saved to: {results_file}")

    def get_status(self) -> Dict[str, Any]:
        """Get current integration status"""
        return {
            'integration_status': self.integration_status,
            'sandbox_status': self.sandbox_manager.get_status(),
            'task_progress': self.task_framework.get_progress()
        }


def main():
    """Main demo execution"""
    print("""
    ╔═══════════════════════════════════════════════════════════════════╗
    ║        DEMO TRADING INTEGRATION SYSTEM                            ║
    ║   Sandbox • Strategies • Automation • Quantum AI                  ║
    ╚═══════════════════════════════════════════════════════════════════╝
    """)

    # Initialize integration system
    integration = DemoTradingIntegration()

    # Run complete demo
    results = integration.run_complete_demo()

    # Display final status
    status = integration.get_status()
    print(f"\n📊 Final System Status:")
    print(f"   Integration Active: ✅")
    print(f"   Sandbox Active: {'✅' if status['integration_status']['sandbox_active'] else '❌'}")
    print(f"   Strategies Loaded: {status['integration_status']['strategies_loaded']}")
    print(f"   Quantum AI: {'✅' if status['integration_status']['quantum_ai_active'] else '❌'}")
    print(f"   Task Progress: {status['task_progress']['progress_percentage']:.1f}%")


if __name__ == "__main__":
    main()
