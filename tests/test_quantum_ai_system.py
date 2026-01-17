#!/usr/bin/env python3
"""
Test suite for Quantum AI System
Validates quantum decision-making, ML, and real-time processing
"""

import sys
from pathlib import Path
import numpy as np
import pytest

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'pillar-a-trading' / 'ai-models'))

from quantum_ai_system import (
    QuantumAISystem,
    QuantumDecisionEngine,
    QuantumMachineLearning,
    QuantumRealTimeProcessor,
    QuantumVersion,
    QuantumState
)


class TestQuantumDecisionEngine:
    """Test Quantum Decision Engine"""

    def test_initialization(self):
        """Test engine initializes correctly"""
        engine = QuantumDecisionEngine(num_qubits=8)
        assert engine.num_qubits == 8
        assert engine.state_space_size == 256

    def test_create_superposition(self):
        """Test superposition creation"""
        engine = QuantumDecisionEngine(num_qubits=8)
        decisions = [
            {'action': 'BUY', 'confidence': 0.7},
            {'action': 'SELL', 'confidence': 0.6},
            {'action': 'HOLD', 'confidence': 0.8}
        ]
        state = engine.create_superposition(decisions)

        assert isinstance(state, QuantumState)
        assert len(state.amplitudes) == 3
        assert len(state.probabilities) == 3
        assert abs(sum(state.probabilities) - 1.0) < 1e-10  # Probabilities sum to 1
        assert 0 <= state.coherence <= 1

    def test_quantum_interference(self):
        """Test quantum interference application"""
        engine = QuantumDecisionEngine(num_qubits=8)
        decisions = [
            {'action': 'BUY', 'confidence': 0.7},
            {'action': 'SELL', 'confidence': 0.6}
        ]
        state = engine.create_superposition(decisions)

        market_data = {
            'volatility': 0.2,
            'momentum': 0.5,
            'volume_ratio': 1.2
        }

        new_state = engine.quantum_interference(state, market_data)
        assert isinstance(new_state, QuantumState)
        assert len(new_state.probabilities) == 2
        assert abs(sum(new_state.probabilities) - 1.0) < 1e-10

    def test_measure(self):
        """Test quantum measurement"""
        engine = QuantumDecisionEngine(num_qubits=8)
        decisions = [
            {'action': 'BUY', 'confidence': 0.7},
            {'action': 'SELL', 'confidence': 0.6},
            {'action': 'HOLD', 'confidence': 0.8}
        ]
        state = engine.create_superposition(decisions)

        chosen_index = engine.measure(state)
        assert 0 <= chosen_index < 3

    def test_decide(self):
        """Test complete decision-making process"""
        engine = QuantumDecisionEngine(num_qubits=8)
        decisions = [
            {'action': 'BUY', 'confidence': 0.7},
            {'action': 'SELL', 'confidence': 0.6},
            {'action': 'HOLD', 'confidence': 0.8}
        ]
        market_data = {
            'volatility': 0.2,
            'momentum': 0.5,
            'volume_ratio': 1.2
        }

        result = engine.decide(decisions, market_data)
        assert 'action' in result
        assert result['action'] in ['BUY', 'SELL', 'HOLD']
        assert 'quantum_probability' in result
        assert 'quantum_coherence' in result
        assert result['quantum_enhanced'] is True


class TestQuantumMachineLearning:
    """Test Quantum Machine Learning System"""

    def test_initialization(self):
        """Test ML system initializes correctly"""
        ml = QuantumMachineLearning()
        assert isinstance(ml.entangled_features, list)
        assert isinstance(ml.learned_patterns, dict)

    def test_quantum_feature_entanglement(self):
        """Test feature entanglement"""
        ml = QuantumMachineLearning()
        features = np.random.randn(50, 10)

        entangled = ml.quantum_feature_entanglement(features)
        assert entangled.shape == features.shape

    def test_quantum_pattern_recognition(self):
        """Test pattern recognition"""
        ml = QuantumMachineLearning()
        data = np.linspace(0, 1, 100)
        patterns = ['BULLISH_MOMENTUM', 'BEARISH_MOMENTUM', 'CONSOLIDATION']

        scores = ml.quantum_pattern_recognition(data, patterns)
        assert len(scores) == 3
        for pattern in patterns:
            assert pattern in scores
            assert 0 <= scores[pattern] <= 1

    def test_quantum_train_predict(self):
        """Test training and prediction"""
        ml = QuantumMachineLearning()

        # Generate synthetic training data
        n_samples = 100
        n_features = 10
        X_train = np.random.randn(n_samples, n_features)
        y_train = np.random.choice([0, 1, 2], n_samples)

        # Train
        ml.quantum_train(X_train, y_train)
        assert len(ml.learned_patterns) > 0

        # Predict
        X_test = np.random.randn(n_features)
        label, confidence = ml.quantum_predict(X_test)
        assert label in [0, 1, 2]
        assert 0 <= confidence <= 1


class TestQuantumRealTimeProcessor:
    """Test Quantum Real-Time Processor"""

    def test_initialization(self):
        """Test processor initializes correctly"""
        processor = QuantumRealTimeProcessor()
        assert isinstance(processor.processing_pipeline, list)

    def test_quantum_parallel_analysis(self):
        """Test parallel analysis of data streams"""
        processor = QuantumRealTimeProcessor()

        data_streams = [
            {'source': 'Technical', 'data': np.random.randn(50).tolist()},
            {'source': 'Fundamental', 'data': np.random.randn(50).tolist()},
            {'source': 'Sentiment', 'data': np.random.randn(50).tolist()}
        ]

        results = processor.quantum_parallel_analysis(data_streams)
        assert 'timestamp' in results
        assert 'streams_processed' in results
        assert results['streams_processed'] == 3
        assert results['quantum_parallel'] is True
        assert 'analyses' in results
        assert len(results['analyses']) == 3
        assert 'aggregated_signal' in results
        assert results['aggregated_signal'] in ['BUY', 'SELL', 'HOLD']


class TestQuantumAISystem:
    """Test Complete Quantum AI System"""

    def test_initialization_v3_0(self):
        """Test system initialization v3.0"""
        system = QuantumAISystem(QuantumVersion.V3_0)
        assert system.version == QuantumVersion.V3_0
        assert system.capabilities['max_qubits'] == 8
        assert system.capabilities['parallel_streams'] == 5

    def test_initialization_v3_4(self):
        """Test system initialization v3.4"""
        system = QuantumAISystem(QuantumVersion.V3_4)
        assert system.version == QuantumVersion.V3_4
        assert system.capabilities['max_qubits'] == 12
        assert system.capabilities['parallel_streams'] == 10

    def test_initialization_v4_0(self):
        """Test system initialization v4.0"""
        system = QuantumAISystem(QuantumVersion.V4_0)
        assert system.version == QuantumVersion.V4_0
        assert system.capabilities['max_qubits'] == 16
        assert system.capabilities['parallel_streams'] == 20

    def test_analyze_market(self):
        """Test complete market analysis"""
        system = QuantumAISystem(QuantumVersion.V4_0)

        market_data = {
            'volatility': 0.25,
            'momentum': 0.6,
            'volume_ratio': 1.3,
            'price_data': np.random.randn(100).cumsum().tolist(),
            'streams': [
                {'source': 'Technical', 'data': np.random.randn(50).tolist()},
                {'source': 'Fundamental', 'data': np.random.randn(50).tolist()},
                {'source': 'Sentiment', 'data': np.random.randn(50).tolist()}
            ]
        }

        result = system.analyze_market(market_data)

        # Verify result structure
        assert 'version' in result
        assert result['version'] == '4.0'
        assert 'timestamp' in result
        assert 'decision' in result
        assert 'realtime_analysis' in result
        assert result['quantum_enhanced'] is True
        assert 'confidence_level' in result
        assert 'coherence' in result
        assert 'recommendation' in result
        assert result['recommendation'] in ['BUY', 'SELL', 'HOLD']
        assert 'phd_algorithms_used' in result

        # Verify decision structure
        decision = result['decision']
        assert 'action' in decision
        assert 'quantum_probability' in decision
        assert 'quantum_coherence' in decision
        assert 'recognized_patterns' in decision

    def test_train_predict(self):
        """Test training and prediction workflow"""
        system = QuantumAISystem(QuantumVersion.V4_0)

        # Generate synthetic training data
        n_samples = 100
        n_features = 10
        X_train = np.random.randn(n_samples, n_features)
        y_train = np.random.choice([0, 1, 2], n_samples)

        # Train
        system.train(X_train, y_train)

        # Predict
        X_test = np.random.randn(n_features)
        label, confidence = system.predict(X_test)
        assert label in [0, 1, 2]
        assert 0 <= confidence <= 1


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
