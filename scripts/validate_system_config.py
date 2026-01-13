#!/usr/bin/env python3
"""
System Configuration Loader and Validator
Agent X5.0 - Project Rapunzel

This script demonstrates loading and validating the new system configuration files.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any


# Constants
SUMMARY_MAX_LENGTH = 50


class AgentX5ConfigLoader:
    """Load and validate Agent X5.0 configuration files."""
    
    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self.configs = {}
        
    def load_all_configs(self) -> Dict[str, Any]:
        """Load all configuration files."""
        config_files = {
            'main': 'agent_3_config.json',
            'persona': 'system_persona_config.json',
            'allocation': 'agent_allocation_config.json',
            'cfo_protocol': 'cfo_diamond_protocol_config.json'
        }
        
        for key, filename in config_files.items():
            filepath = self.config_dir / filename
            try:
                with open(filepath, 'r') as f:
                    self.configs[key] = json.load(f)
                print(f"✓ Loaded {filename}")
            except FileNotFoundError:
                print(f"✗ Error: {filename} not found")
                raise
            except json.JSONDecodeError as e:
                print(f"✗ Error: Invalid JSON in {filename}: {e}")
                raise
                
        return self.configs
    
    def validate_agent_allocation(self) -> bool:
        """Validate agent allocation totals to 750."""
        allocation = self.configs.get('allocation', {})
        squads = allocation.get('squads', {})
        
        total_agents = sum(squad.get('units', 0) for squad in squads.values())
        expected_total = allocation.get('total_agents', 750)
        
        if total_agents == expected_total:
            print(f"✓ Agent allocation validated: {total_agents} agents")
            print(f"  - Squad A: {squads.get('squad_a', {}).get('units', 0)} units")
            print(f"  - Squad B: {squads.get('squad_b', {}).get('units', 0)} units")
            print(f"  - Task Force C: {squads.get('task_force_c', {}).get('units', 0)} units")
            return True
        else:
            print(f"✗ Agent allocation error: Expected {expected_total}, got {total_agents}")
            return False
    
    def validate_cfo_protocol(self) -> bool:
        """Validate CFO Diamond Protocol has all three filters."""
        protocol = self.configs.get('cfo_protocol', {})
        filters = protocol.get('filters', {})
        
        required_filters = ['filter_1', 'filter_2', 'filter_3']
        filter_names = {
            'filter_1': 'The CPA',
            'filter_2': 'The General Counsel',
            'filter_3': 'The Quantum Architect'
        }
        
        all_present = all(f in filters for f in required_filters)
        
        if all_present:
            print("✓ CFO Diamond Protocol validated:")
            for filter_id, expected_name in filter_names.items():
                actual_name = filters[filter_id].get('name', 'Unknown')
                print(f"  - {filter_id}: {actual_name}")
            return True
        else:
            print("✗ CFO Diamond Protocol error: Missing filters")
            return False
    
    def validate_persona(self) -> bool:
        """Validate system persona configuration."""
        persona_config = self.configs.get('persona', {})
        persona = persona_config.get('persona', {})
        
        required_fields = ['voice', 'authority_sources', 'tone', 'style']
        all_present = all(field in persona for field in required_fields)
        
        if all_present:
            voice = persona.get('voice', 'Unknown')
            num_sources = len(persona.get('authority_sources', []))
            print(f"✓ System persona validated:")
            print(f"  - Voice: {voice}")
            print(f"  - Authority sources: {num_sources} institutions")
            
            miracle = persona_config.get('miracle_directive', {})
            if miracle:
                print(f"  - Miracle Directive: {miracle.get('goal', 'Not defined')[:SUMMARY_MAX_LENGTH]}...")
            
            return True
        else:
            print("✗ System persona error: Missing required fields")
            return False
    
    def validate_cross_device_sync(self) -> bool:
        """Validate cross-device sync configuration."""
        persona_config = self.configs.get('persona', {})
        sync = persona_config.get('cross_device_sync', {})
        
        protocol = sync.get('protocol', '')
        devices = sync.get('active_devices', [])
        
        if protocol and devices:
            print(f"✓ Cross-device sync validated:")
            print(f"  - Protocol: {protocol}")
            print(f"  - Active devices: {', '.join(devices)}")
            print(f"  - Sync interval: {sync.get('sync_interval_seconds', 'Unknown')} seconds")
            return True
        else:
            print("✗ Cross-device sync error: Missing configuration")
            return False
    
    def display_system_summary(self):
        """Display a summary of the system configuration."""
        print("\n" + "="*70)
        print("AGENT X5.0 - PROJECT RAPUNZEL")
        print("System Configuration Summary")
        print("="*70)
        
        main = self.configs.get('main', {})
        print(f"\nSystem Name: {main.get('system_name', 'Unknown')}")
        print(f"Version: {main.get('version', 'Unknown')}")
        print(f"Deployment Date: {main.get('deployment_date', 'Unknown')}")
        print(f"Owner: {main.get('owner', 'Unknown')}")
        print(f"Organization: {main.get('organization', 'Unknown')}")
        
        allocation = self.configs.get('allocation', {})
        print(f"\nTotal Agents: {allocation.get('total_agents', 'Unknown')}")
        
        persona_config = self.configs.get('persona', {})
        persona = persona_config.get('persona', {})
        print(f"Voice Authority: {persona.get('voice', 'Unknown')}")
        
        protocol = self.configs.get('cfo_protocol', {})
        print(f"\nCFO Diamond Protocol: {'Enabled' if protocol.get('default_mode') else 'Disabled'}")
        
        print("="*70 + "\n")


def main():
    """Main execution function."""
    print("Agent X5.0 Configuration Loader\n")
    
    # Determine config directory
    script_dir = Path(__file__).parent
    config_dir = script_dir.parent / "config"
    
    if not config_dir.exists():
        config_dir = Path("config")
    
    # Load and validate configurations
    loader = AgentX5ConfigLoader(str(config_dir))
    
    try:
        print("Loading configuration files...\n")
        loader.load_all_configs()
        
        print("\nValidating configurations...\n")
        
        validation_results = {
            'agent_allocation': loader.validate_agent_allocation(),
            'cfo_protocol': loader.validate_cfo_protocol(),
            'persona': loader.validate_persona(),
            'cross_device_sync': loader.validate_cross_device_sync()
        }
        
        # Display summary
        loader.display_system_summary()
        
        # Final validation result
        all_valid = all(validation_results.values())
        
        if all_valid:
            print("✅ All configurations validated successfully!")
            print("\nAgent X5.0 is ready for deployment.")
            return 0
        else:
            print("❌ Configuration validation failed!")
            print("\nPlease review the errors above.")
            return 1
            
    except Exception as e:
        print(f"\n❌ Error during configuration loading: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
