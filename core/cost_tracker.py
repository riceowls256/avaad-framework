"""
AVAAD AI Cost Management System

Tracks costs associated with AI agent usage across different models and providers.
Provides budgeting, alerts, and ROI analysis for AI-assisted development.
"""

import json
import time
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from pathlib import Path
import yaml


@dataclass
class CostEntry:
    """Represents a single AI interaction cost."""
    timestamp: str
    agent: str
    model: str
    input_tokens: int
    output_tokens: int
    input_cost: float
    output_cost: float
    total_cost: float
    story_id: Optional[str] = None
    task_description: str = ""
    currency: str = "USD"


@dataclass
class BudgetAlert:
    """Represents a budget alert."""
    level: str  # INFO, WARNING, CRITICAL
    message: str
    current_spend: float
    budget_limit: float
    percentage: float
    timestamp: str


class CostTracker:
    """
    Tracks AI agent costs across different models and providers.
    
    Features:
    - Real-time cost calculation per interaction
    - Budget tracking and alerts
    - Cost per story analysis
    - ROI calculations
    - Model efficiency comparisons
    """
    
    def __init__(self, project_root: str = "."):
        """Initialize cost tracker with project settings."""
        self.project_root = Path(project_root)
        self.config = self._load_config()
        self.cost_log_path = self.project_root / "logs" / "ai_costs.jsonl"
        self.cost_log_path.parent.mkdir(exist_ok=True)
        
        # Ensure log file exists
        if not self.cost_log_path.exists():
            self.cost_log_path.write_text("")
    
    def _load_config(self) -> Dict[str, Any]:
        """Load cost tracking configuration."""
        config_path = self.project_root / "config" / "cost-tracking.yaml"
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Return default cost tracking configuration."""
        return {
            'models': {
                'claude-sonnet-4': {'input_cost': 0.003, 'output_cost': 0.015},
                'claude-opus-4': {'input_cost': 0.015, 'output_cost': 0.075},
                'gpt-4o': {'input_cost': 0.005, 'output_cost': 0.015},
                'gpt-4o-mini': {'input_cost': 0.00015, 'output_cost': 0.0006},
                'gpt-4-turbo': {'input_cost': 0.01, 'output_cost': 0.03}
            },
            'budgets': {
                'daily': 50.0,
                'weekly': 200.0,
                'monthly': 800.0,
                'project_total': 5000.0
            },
            'alerts': {
                'daily_warning': 40.0,
                'daily_critical': 45.0,
                'weekly_warning': 160.0,
                'weekly_critical': 190.0
            },
            'currency': 'USD',
            'log_level': 'INFO'
        }
    
    def log_interaction(self, agent: str, model: str, input_tokens: int, 
                       output_tokens: int, story_id: Optional[str] = None,
                       task_description: str = "") -> CostEntry:
        """
        Log a single AI interaction with cost calculation.
        
        Args:
            agent: Name of the AI agent
            model: Model used (e.g., 'claude-sonnet-4')
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            story_id: Associated story ID (optional)
            task_description: Description of the task
            
        Returns:
            CostEntry with calculated costs
        """
        model_config = self.config.get('models', {}).get(model, {})
        input_cost = model_config.get('input_cost', 0.0)
        output_cost = model_config.get('output_cost', 0.0)
        
        total_cost = (input_tokens * input_cost / 1000) + \
                    (output_tokens * output_cost / 1000)
        
        entry = CostEntry(
            timestamp=datetime.now().isoformat(),
            agent=agent,
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            input_cost=input_tokens * input_cost / 1000,
            output_cost=output_tokens * output_cost / 1000,
            total_cost=total_cost,
            story_id=story_id,
            task_description=task_description
        )
        
        # Log to file
        self._append_cost_entry(entry)
        
        # Check for budget alerts
        self._check_budget_alerts(entry)
        
        return entry
    
    def _append_cost_entry(self, entry: CostEntry) -> None:
        """Append cost entry to log file."""
        with open(self.cost_log_path, 'a') as f:
            f.write(json.dumps(asdict(entry)) + '\n')
    
    def _check_budget_alerts(self, entry: CostEntry) -> List[BudgetAlert]:
        """Check if current spending triggers budget alerts."""
        alerts = []
        
        # Get current spending for different periods
        daily_spend = self.get_period_spend('daily')
        weekly_spend = self.get_period_spend('weekly')
        monthly_spend = self.get_period_spend('monthly')
        
        # Daily alerts
        daily_budget = self.config.get('budgets', {}).get('daily', 50.0)
        daily_warning = self.config.get('alerts', {}).get('daily_warning', 40.0)
        daily_critical = self.config.get('alerts', {}).get('daily_critical', 45.0)
        
        if daily_spend >= daily_critical:
            alerts.append(BudgetAlert(
                level='CRITICAL',
                message=f'Daily budget exceeded! Current: ${daily_spend:.2f}, Limit: ${daily_budget:.2f}',
                current_spend=daily_spend,
                budget_limit=daily_budget,
                percentage=(daily_spend / daily_budget) * 100,
                timestamp=datetime.now().isoformat()
            ))
        elif daily_spend >= daily_warning:
            alerts.append(BudgetAlert(
                level='WARNING',
                message=f'Daily budget warning: ${daily_spend:.2f} of ${daily_budget:.2f}',
                current_spend=daily_spend,
                budget_limit=daily_budget,
                percentage=(daily_spend / daily_budget) * 100,
                timestamp=datetime.now().isoformat()
            ))
        
        # Similar checks for weekly/monthly
        weekly_budget = self.config.get('budgets', {}).get('weekly', 200.0)
        weekly_warning = self.config.get('alerts', {}).get('weekly_warning', 160.0)
        
        if weekly_spend >= weekly_warning:
            alerts.append(BudgetAlert(
                level='WARNING',
                message=f'Weekly budget warning: ${weekly_spend:.2f} of ${weekly_budget:.2f}',
                current_spend=weekly_spend,
                budget_limit=weekly_budget,
                percentage=(weekly_spend / weekly_budget) * 100,
                timestamp=datetime.now().isoformat()
            ))
        
        return alerts
    
    def get_period_spend(self, period: str) -> float:
        """Get total spend for a given period."""
        now = datetime.now()
        
        if period == 'daily':
            start_time = now.replace(hour=0, minute=0, second=0, microsecond=0)
        elif period == 'weekly':
            start_time = now - timedelta(days=now.weekday())
            start_time = start_time.replace(hour=0, minute=0, second=0, microsecond=0)
        elif period == 'monthly':
            start_time = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        else:
            start_time = now - timedelta(days=30)  # Default to 30 days
        
        entries = self._load_cost_entries()
        period_entries = [
            e for e in entries
            if datetime.fromisoformat(e.timestamp) >= start_time
        ]
        
        return sum(e.total_cost for e in period_entries)
    
    def get_cost_summary(self, days: int = 7) -> Dict[str, Any]:
        """Get comprehensive cost summary for a period."""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        entries = self._load_cost_entries()
        period_entries = [
            e for e in entries
            if datetime.fromisoformat(e.timestamp) >= start_date
        ]
        
        if not period_entries:
            return {
                'total_cost': 0.0,
                'entries': 0,
                'by_agent': {},
                'by_model': {},
                'by_story': {},
                'daily_breakdown': {}
            }
        
        total_cost = sum(e.total_cost for e in period_entries)
        
        # Group by agent
        by_agent = {}
        for entry in period_entries:
            by_agent[entry.agent] = by_agent.get(entry.agent, 0.0) + entry.total_cost
        
        # Group by model
        by_model = {}
        for entry in period_entries:
            by_model[entry.model] = by_model.get(entry.model, 0.0) + entry.total_cost
        
        # Group by story
        by_story = {}
        for entry in period_entries:
            if entry.story_id:
                by_story[entry.story_id] = by_story.get(entry.story_id, 0.0) + entry.total_cost
        
        # Daily breakdown
        daily_breakdown = {}
        for entry in period_entries:
            date_key = datetime.fromisoformat(entry.timestamp).strftime('%Y-%m-%d')
            daily_breakdown[date_key] = daily_breakdown.get(date_key, 0.0) + entry.total_cost
        
        return {
            'total_cost': total_cost,
            'entries': len(period_entries),
            'by_agent': by_agent,
            'by_model': by_model,
            'by_story': by_story,
            'daily_breakdown': daily_breakdown,
            'average_per_entry': total_cost / len(period_entries) if period_entries else 0.0
        }
    
    def get_model_efficiency(self) -> Dict[str, Dict[str, float]]:
        """Compare model efficiency (cost per task)."""
        entries = self._load_cost_entries()
        
        model_stats = {}
        for entry in entries:
            model = entry.model
            if model not in model_stats:
                model_stats[model] = {'total_cost': 0.0, 'tasks': 0, 'total_tokens': 0}
            
            model_stats[model]['total_cost'] += entry.total_cost
            model_stats[model]['tasks'] += 1
            model_stats[model]['total_tokens'] += entry.input_tokens + entry.output_tokens
        
        efficiency = {}
        for model, stats in model_stats.items():
            efficiency[model] = {
                'total_spend': stats['total_cost'],
                'tasks_completed': stats['tasks'],
                'cost_per_task': stats['total_cost'] / stats['tasks'] if stats['tasks'] > 0 else 0.0,
                'tokens_per_task': stats['total_tokens'] / stats['tasks'] if stats['tasks'] > 0 else 0.0,
                'cost_per_1000_tokens': (stats['total_cost'] / stats['total_tokens'] * 1000) if stats['total_tokens'] > 0 else 0.0
            }
        
        return efficiency
    
    def calculate_roi(self, story_id: str) -> Dict[str, float]:
        """Calculate ROI for a specific story."""
        entries = self._load_cost_entries()
        story_entries = [e for e in entries if e.story_id == story_id]
        
        if not story_entries:
            return {'total_cost': 0.0, 'estimated_hours': 0.0, 'roi_score': 0.0}
        
        total_cost = sum(e.total_cost for e in story_entries)
        
        # Estimate hours saved (rough calculation)
        # Assume 1 hour of developer time = $50
        # Complex stories might save more time
        estimated_hours = min(total_cost * 10, 8.0)  # Cap at 8 hours
        estimated_value = estimated_hours * 50.0  # $50/hour developer cost
        
        roi_score = (estimated_value - total_cost) / total_cost * 100 if total_cost > 0 else 0.0
        
        return {
            'total_cost': total_cost,
            'estimated_hours_saved': estimated_hours,
            'estimated_value': estimated_value,
            'roi_score': roi_score,
            'cost_per_hour': total_cost / estimated_hours if estimated_hours > 0 else 0.0
        }
    
    def _load_cost_entries(self) -> List[CostEntry]:
        """Load all cost entries from log file."""
        if not self.cost_log_path.exists():
            return []
        
        entries = []
        with open(self.cost_log_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        data = json.loads(line)
                        entries.append(CostEntry(**data))
                    except json.JSONDecodeError:
                        continue
        
        return entries
    
    def generate_cost_report(self, days: int = 7) -> str:
        """Generate a user-friendly cost report."""
        summary = self.get_cost_summary(days)
        efficiency = self.get_model_efficiency()
        
        report = []
        report.append("💰 AVAAD AI Cost Report")
        report.append("=" * 50)
        report.append(f"Period: Last {days} days")
        report.append(f"Total Spend: ${summary['total_cost']:.2f}")
        report.append(f"Interactions: {summary['entries']}")
        report.append(f"Average per interaction: ${summary['average_per_entry']:.3f}")
        
        if summary['by_agent']:
            report.append("\n📊 By Agent:")
            for agent, cost in sorted(summary['by_agent'].items(), key=lambda x: x[1], reverse=True):
                report.append(f"  {agent}: ${cost:.2f}")
        
        if summary['by_model']:
            report.append("\n🤖 By Model:")
            for model, cost in sorted(summary['by_model'].items(), key=lambda x: x[1], reverse=True):
                report.append(f"  {model}: ${cost:.2f}")
        
        if summary['by_story']:
            report.append("\n📋 By Story:")
            for story, cost in sorted(summary['by_story'].items(), key=lambda x: x[1], reverse=True)[:5]:
                report.append(f"  {story}: ${cost:.2f}")
        
        if efficiency:
            report.append("\n⚡ Model Efficiency:")
            for model, stats in efficiency.items():
                report.append(f"  {model}: ${stats['cost_per_task']:.3f}/task")
        
        return "\n".join(report)


def main():
    """CLI interface for cost tracking."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python cost_tracker.py <command>")
        print("  Commands: report, efficiency, roi <story_id>")
        sys.exit(1)
    
    tracker = CostTracker()
    command = sys.argv[1]
    
    if command == "report":
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 7
        print(tracker.generate_cost_report(days))
    elif command == "efficiency":
        efficiency = tracker.get_model_efficiency()
        for model, stats in efficiency.items():
            print(f"{model}: ${stats['cost_per_task']:.3f}/task ({stats['tasks_completed']} tasks)")
    elif command == "roi" and len(sys.argv) > 2:
        story_id = sys.argv[2]
        roi = tracker.calculate_roi(story_id)
        print(f"Story {story_id}:")
        print(f"  Cost: ${roi['total_cost']:.2f}")
        print(f"  Estimated Hours Saved: {roi['estimated_hours_saved']:.1f}")
        print(f"  ROI: {roi['roi_score']:.1f}%")


if __name__ == "__main__":
    main()