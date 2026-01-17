#!/usr/bin/env python3
"""
LONG POSITION STRATEGY
Main trading strategy focused on long positions in undervalued assets

Strategy: Find undervalued, fundamentally strong assets and GO LONG

Targets:
- Undervalued stocks (P/E < 15, P/B < 2)
- Strong fundamentals (ROE > 15%, Debt/Equity < 1)
- Positive momentum (RSI 40-60, MACD bullish)
- Market dips (buying opportunities)
- Growth sectors with strong fundamentals
"""

import numpy as np
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('LongPosition')


class LongPositionStrategy:
    """
    Long Position Strategy - Professional Long Strategy

    Identifies and goes long on:
    1. Undervalued stocks (fundamentals)
    2. Technical oversold (RSI < 40, MACD bullish)
    3. Market dips (buying opportunities)
    4. Strong fundamentals (ROE, margins)
    5. Growth sectors
    """

    def __init__(self):
        self.watchlist = []
        self.active_longs = []
        self.criteria = {
            'pe_ratio_max': 15,  # P/E below this = undervalued
            'pb_ratio_max': 2,   # P/B below this = value territory
            'roe_min': 15,       # ROE above this = strong returns
            'debt_equity_max': 1, # D/E below this = manageable debt
            'rsi_oversold': 40,  # RSI below this = oversold
            'rsi_ideal_min': 40, # Ideal RSI range start
            'rsi_ideal_max': 60  # Ideal RSI range end
        }
        logger.info("=" * 70)
        logger.info("📈 LONG POSITION STRATEGY INITIALIZED")
        logger.info("   Finding undervalued assets to GO LONG...")
        logger.info("=" * 70)

    def analyze_for_long(self, symbol: str, data: Dict) -> Dict:
        """
        Analyze if symbol is a good LONG candidate

        Returns signal with confidence 0-100%
        """
        signal = {
            'symbol': symbol,
            'action': 'HOLD',
            'confidence': 0.0,
            'strategy': 'Long Position',
            'reasons': [],
            'risk_level': 'medium',
            'timestamp': datetime.now().isoformat()
        }

        score = 0
        max_score = 0

        # 1. FUNDAMENTAL UNDERVALUATION (40 points)
        pe_ratio = data.get('pe_ratio', 20)
        pb_ratio = data.get('pb_ratio', 3)
        roe = data.get('roe', 10)
        debt_equity = data.get('debt_equity', 1)

        # Handle 'N/A' or string values
        try:
            pe_ratio = float(pe_ratio) if pe_ratio not in ['N/A', None] else 999
        except (ValueError, TypeError):
            pe_ratio = 999

        try:
            pb_ratio = float(pb_ratio) if pb_ratio not in ['N/A', None] else 999
        except (ValueError, TypeError):
            pb_ratio = 999

        try:
            roe = float(roe) if roe not in ['N/A', None] else 0
        except (ValueError, TypeError):
            roe = 0

        try:
            debt_equity = float(debt_equity) if debt_equity not in ['N/A', None] else 999
        except (ValueError, TypeError):
            debt_equity = 999

        if pe_ratio < self.criteria['pe_ratio_max'] and pe_ratio > 0:
            score += 15
            signal['reasons'].append(f"Attractive P/E: {pe_ratio:.1f} (undervalued)")

        if pb_ratio < self.criteria['pb_ratio_max'] and pb_ratio > 0:
            score += 10
            signal['reasons'].append(f"Low P/B ratio: {pb_ratio:.1f} (value territory)")

        if roe > self.criteria['roe_min']:
            score += 10
            signal['reasons'].append(f"Strong ROE: {roe:.1f}% (excellent returns)")

        if debt_equity < self.criteria['debt_equity_max']:
            score += 5
            signal['reasons'].append(f"Manageable debt: {debt_equity:.1f} (healthy balance sheet)")

        max_score += 40

        # 2. TECHNICAL INDICATORS (30 points)
        rsi = data.get('rsi', 50)
        macd = data.get('macd', 0)
        macd_signal = data.get('macd_signal', 0)

        # RSI in ideal range or oversold
        if self.criteria['rsi_ideal_min'] <= rsi <= self.criteria['rsi_ideal_max']:
            score += 15
            signal['reasons'].append(f"RSI in ideal range: {rsi:.1f} (balanced momentum)")
        elif rsi < self.criteria['rsi_oversold']:
            score += 12
            signal['reasons'].append(f"RSI oversold: {rsi:.1f} (potential reversal)")

        # MACD bullish crossover
        if macd > macd_signal and macd_signal < 0:
            score += 15
            signal['reasons'].append("MACD bullish crossover (momentum building)")
        elif macd > 0:
            score += 10
            signal['reasons'].append("MACD positive (upward momentum)")

        max_score += 30

        # 3. VOLUME AND MOMENTUM (15 points)
        volume_ratio = data.get('volume_ratio', 1.0)
        momentum = data.get('momentum', 0)

        if volume_ratio > 1.2:
            score += 7
            signal['reasons'].append(f"Strong volume: {volume_ratio:.1f}x average (accumulation)")

        if momentum > 0:
            score += 8
            signal['reasons'].append(f"Positive momentum: {momentum:.2f} (uptrend)")

        max_score += 15

        # 4. MARKET CONDITIONS (15 points)
        market_sentiment = data.get('market_sentiment', 'neutral')
        sector_strength = data.get('sector_strength', 50)

        if market_sentiment in ['bullish', 'recovery']:
            score += 8
            signal['reasons'].append(f"Market sentiment: {market_sentiment} (favorable)")
        elif market_sentiment == 'dip':
            score += 10
            signal['reasons'].append("Market dip detected (buying opportunity)")

        if sector_strength > 60:
            score += 7
            signal['reasons'].append(f"Strong sector: {sector_strength}/100 (sector momentum)")

        max_score += 15

        # Calculate confidence
        if max_score > 0:
            confidence = (score / max_score) * 100
        else:
            confidence = 0

        signal['confidence'] = confidence
        signal['score'] = score
        signal['max_score'] = max_score

        # Determine action based on confidence
        if confidence >= 70:
            signal['action'] = 'BUY'
            signal['risk_level'] = 'low'
            logger.info(f"🎯 STRONG LONG: {symbol} - Confidence: {confidence:.1f}%")
        elif confidence >= 50:
            signal['action'] = 'BUY'
            signal['risk_level'] = 'medium'
            logger.info(f"📊 MODERATE LONG: {symbol} - Confidence: {confidence:.1f}%")
        elif confidence >= 30:
            signal['action'] = 'WATCH'
            signal['risk_level'] = 'medium'
            logger.info(f"👁️ WATCH: {symbol} - Confidence: {confidence:.1f}%")
        else:
            signal['action'] = 'HOLD'
            signal['risk_level'] = 'high'

        return signal

    def calculate_position_size(self, capital: float, confidence: float, risk_level: str) -> Dict:
        """
        Calculate appropriate position size based on confidence and risk

        Args:
            capital: Available trading capital
            confidence: Signal confidence (0-100)
            risk_level: Risk level (low, medium, high)

        Returns:
            Dict with position sizing details
        """
        risk_multipliers = {
            'low': 0.15,      # 15% of capital for low risk
            'medium': 0.10,   # 10% of capital for medium risk
            'high': 0.05      # 5% of capital for high risk
        }

        base_multiplier = risk_multipliers.get(risk_level, 0.10)
        
        # Adjust based on confidence
        confidence_adjustment = (confidence / 100) * 1.5
        final_multiplier = base_multiplier * confidence_adjustment

        # Cap at 20% of capital
        final_multiplier = min(final_multiplier, 0.20)

        position_size = capital * final_multiplier

        return {
            'position_size': position_size,
            'percentage_of_capital': final_multiplier * 100,
            'risk_level': risk_level,
            'confidence': confidence
        }

    def manage_position(self, position: Dict, current_price: float) -> Dict:
        """
        Manage existing long position - determine if should hold, add, or exit

        Args:
            position: Current position details
            current_price: Current market price

        Returns:
            Dict with position management recommendation
        """
        entry_price = position.get('entry_price', current_price)
        current_return = ((current_price - entry_price) / entry_price) * 100

        recommendation = {
            'action': 'HOLD',
            'reason': '',
            'current_return': current_return
        }

        # Take profit levels
        if current_return >= 20:
            recommendation['action'] = 'TAKE_PROFIT'
            recommendation['reason'] = f'Strong gain: {current_return:.1f}% (take profits)'
        elif current_return >= 10:
            recommendation['action'] = 'SCALE_OUT'
            recommendation['reason'] = f'Good gain: {current_return:.1f}% (scale out 50%)'
        # Stop loss
        elif current_return <= -10:
            recommendation['action'] = 'STOP_LOSS'
            recommendation['reason'] = f'Stop loss hit: {current_return:.1f}% (exit position)'
        elif current_return <= -5:
            recommendation['action'] = 'REDUCE'
            recommendation['reason'] = f'Moderate loss: {current_return:.1f}% (reduce position)'
        # Hold zone
        else:
            recommendation['action'] = 'HOLD'
            recommendation['reason'] = f'Within range: {current_return:.1f}% (hold position)'

        return recommendation

    def screen_candidates(self, market_data: List[Dict]) -> List[Dict]:
        """
        Screen multiple candidates and rank them

        Args:
            market_data: List of market data for different symbols

        Returns:
            List of signals sorted by confidence
        """
        signals = []

        for data in market_data:
            symbol = data.get('symbol', 'UNKNOWN')
            signal = self.analyze_for_long(symbol, data)
            
            if signal['action'] in ['BUY', 'WATCH']:
                signals.append(signal)

        # Sort by confidence (descending)
        signals.sort(key=lambda x: x['confidence'], reverse=True)

        logger.info("\n" + "=" * 70)
        logger.info(f"📊 LONG POSITION SCREENING RESULTS")
        logger.info("=" * 70)
        logger.info(f"Total candidates analyzed: {len(market_data)}")
        logger.info(f"BUY signals: {len([s for s in signals if s['action'] == 'BUY'])}")
        logger.info(f"WATCH signals: {len([s for s in signals if s['action'] == 'WATCH'])}")
        logger.info("=" * 70 + "\n")

        return signals


def main():
    """Demo of Long Position Strategy"""
    print("""
    ╔═══════════════════════════════════════════════════════════════════╗
    ║              LONG POSITION STRATEGY                               ║
    ║          Finding Undervalued Assets                               ║
    ╚═══════════════════════════════════════════════════════════════════╝
    """)

    strategy = LongPositionStrategy()

    # Test with sample data
    test_data = {
        'symbol': 'AAPL',
        'pe_ratio': 12.5,
        'pb_ratio': 1.8,
        'roe': 25,
        'debt_equity': 0.8,
        'rsi': 45,
        'macd': 0.5,
        'macd_signal': 0.3,
        'volume_ratio': 1.5,
        'momentum': 0.02,
        'market_sentiment': 'bullish',
        'sector_strength': 70
    }

    signal = strategy.analyze_for_long('AAPL', test_data)

    print(f"\n📊 Analysis Result:")
    print(f"   Symbol: {signal['symbol']}")
    print(f"   Action: {signal['action']}")
    print(f"   Confidence: {signal['confidence']:.1f}%")
    print(f"   Risk Level: {signal['risk_level']}")
    print(f"\n📋 Reasons:")
    for reason in signal['reasons']:
        print(f"   • {reason}")

    # Test position sizing
    capital = 10000
    position_size = strategy.calculate_position_size(capital, signal['confidence'], signal['risk_level'])
    print(f"\n💰 Position Sizing (Capital: ${capital:,.2f}):")
    print(f"   Position Size: ${position_size['position_size']:,.2f}")
    print(f"   Percentage: {position_size['percentage_of_capital']:.1f}%")


if __name__ == "__main__":
    main()
