#!/usr/bin/env python3
"""
AVAAD AI Cost Reporter CLI Tool

Command-line interface for AI cost tracking, reporting, and budget management.
"""

import sys
import argparse
from pathlib import Path
import json

# Add core modules to path
sys.path.append(str(Path(__file__).parent / ".." / "core"))

from cost_tracker import CostTracker


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="AVAAD AI Cost Reporter - Track AI Agent Costs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s report --last-week
  %(prog)s report --days 30
  %(prog)s efficiency
  %(prog)s roi story-6.2
  %(prog)s budget --daily
  %(prog)s add-cost claude-sonnet-4 1000 200 --story 6.2
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Report command
    report_parser = subparsers.add_parser('report', help='Generate cost report')
    report_parser.add_argument('--days', type=int, default=7, help='Number of days to report (default: 7)')
    report_parser.add_argument('--last-week', action='store_true', help='Report for last 7 days')
    report_parser.add_argument('--last-month', action='store_true', help='Report for last 30 days')
    
    # Efficiency command
    efficiency_parser = subparsers.add_parser('efficiency', help='Show model efficiency')
    
    # ROI command
    roi_parser = subparsers.add_parser('roi', help='Calculate ROI for a story')
    roi_parser.add_argument('story_id', help='Story ID to analyze')
    
    # Budget command
    budget_parser = subparsers.add_parser('budget', help='Check budget status')
    budget_parser.add_argument('--daily', action='store_true', help='Check daily budget')
    budget_parser.add_argument('--weekly', action='store_true', help='Check weekly budget')
    budget_parser.add_argument('--monthly', action='store_true', help='Check monthly budget')
    
    # Add cost command (for manual entry)
    add_parser = subparsers.add_parser('add-cost', help='Manually add cost entry')
    add_parser.add_argument('model', help='Model name (e.g., claude-sonnet-4)')
    add_parser.add_argument('input_tokens', type=int, help='Number of input tokens')
    add_parser.add_argument('output_tokens', type=int, help='Number of output tokens')
    add_parser.add_argument('--agent', default='manual', help='Agent name')
    add_parser.add_argument('--story', help='Associated story ID')
    add_parser.add_argument('--description', default='', help='Task description')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    tracker = CostTracker()
    
    try:
        if args.command == 'report':
            return handle_report(tracker, args)
        elif args.command == 'efficiency':
            return handle_efficiency(tracker, args)
        elif args.command == 'roi':
            return handle_roi(tracker, args)
        elif args.command == 'budget':
            return handle_budget(tracker, args)
        elif args.command == 'add-cost':
            return handle_add_cost(tracker, args)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    
    return 0


def handle_report(tracker: CostTracker, args) -> int:
    """Handle cost reporting."""
    days = 30 if args.last_month else (7 if args.last_week else args.days)
    
    print("💰 AVAAD AI Cost Report")
    print("=" * 50)
    print(f"Period: Last {days} days")
    
    summary = tracker.get_cost_summary(days)
    
    if summary['total_cost'] == 0:
        print("No AI costs recorded for this period.")
        return 0
    
    print(f"Total Spend: ${summary['total_cost']:.2f}")
    print(f"Interactions: {summary['entries']}")
    print(f"Average per interaction: ${summary['average_per_entry']:.3f}")
    
    if summary['by_agent']:
        print("\n📊 By Agent:")
        for agent, cost in sorted(summary['by_agent'].items(), key=lambda x: x[1], reverse=True):
            print(f"  {agent}: ${cost:.2f}")
    
    if summary['by_model']:
        print("\n🤖 By Model:")
        for model, cost in sorted(summary['by_model'].items(), key=lambda x: x[1], reverse=True):
            print(f"  {model}: ${cost:.2f}")
    
    if summary['by_story']:
        print("\n📋 Top Stories by Cost:")
        for story, cost in sorted(summary['by_story'].items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"  {story}: ${cost:.2f}")
    
    if summary['daily_breakdown']:
        print("\n📅 Daily Breakdown:")
        for date, cost in sorted(summary['daily_breakdown'].items()):
            print(f"  {date}: ${cost:.2f}")
    
    return 0


def handle_efficiency(tracker: CostTracker, args) -> int:
    """Handle efficiency analysis."""
    print("⚡ Model Efficiency Analysis")
    print("=" * 50)
    
    efficiency = tracker.get_model_efficiency()
    
    if not efficiency:
        print("No AI usage data available.")
        return 0
    
    print("Cost per task by model:")
    for model, stats in sorted(efficiency.items(), key=lambda x: x[1]['cost_per_task']):
        print(f"\n{model}:")
        print(f"  Cost per task: ${stats['cost_per_task']:.3f}")
        print(f"  Tasks completed: {stats['tasks_completed']}")
        print(f"  Total spend: ${stats['total_spend']:.2f}")
        print(f"  Cost per 1000 tokens: ${stats['cost_per_1000_tokens']:.3f}")
    
    return 0


def handle_roi(tracker: CostTracker, args) -> int:
    """Handle ROI calculation."""
    print(f"💡 ROI Analysis for Story: {args.story_id}")
    print("=" * 50)
    
    roi = tracker.calculate_roi(args.story_id)
    
    if roi['total_cost'] == 0:
        print(f"No AI costs recorded for story {args.story_id}")
        return 1
    
    print(f"AI Cost: ${roi['total_cost']:.2f}")
    print(f"Estimated Hours Saved: {roi['estimated_hours_saved']:.1f}")
    print(f"Estimated Developer Value: ${roi['estimated_value']:.2f}")
    print(f"ROI Score: {roi['roi_score']:.1f}%")
    print(f"Cost per Hour Saved: ${roi['cost_per_hour']:.2f}")
    
    if roi['roi_score'] > 100:
        print("🎉 Excellent ROI! AI usage is highly cost-effective.")
    elif roi['roi_score'] > 50:
        print("✅ Good ROI. AI usage is cost-effective.")
    elif roi['roi_score'] > 0:
        print("⚠️  Moderate ROI. Consider optimizing AI usage.")
    else:
        print("❌ Negative ROI. Review AI usage strategy.")
    
    return 0


def handle_budget(tracker: CostTracker, args) -> int:
    """Handle budget checking."""
    print("💰 Budget Status")
    print("=" * 50)
    
    config = tracker.config
    
    if args.daily:
        spend = tracker.get_period_spend('daily')
        budget = config.get('budgets', {}).get('daily', 50.0)
        print(f"Daily Budget: ${budget:.2f}")
        print(f"Current Daily Spend: ${spend:.2f}")
        print(f"Remaining: ${budget - spend:.2f}")
        
        if spend >= budget:
            print("❌ DAILY BUDGET EXCEEDED!")
        elif spend >= budget * 0.9:
            print("⚠️  Daily budget almost exhausted!")
        else:
            print("✅ Daily budget OK")
    
    elif args.weekly:
        spend = tracker.get_period_spend('weekly')
        budget = config.get('budgets', {}).get('weekly', 200.0)
        print(f"Weekly Budget: ${budget:.2f}")
        print(f"Current Weekly Spend: ${spend:.2f}")
        print(f"Remaining: ${budget - spend:.2f}")
        
        if spend >= budget:
            print("❌ WEEKLY BUDGET EXCEEDED!")
        elif spend >= budget * 0.9:
            print("⚠️  Weekly budget almost exhausted!")
        else:
            print("✅ Weekly budget OK")
    
    elif args.monthly:
        spend = tracker.get_period_spend('monthly')
        budget = config.get('budgets', {}).get('monthly', 800.0)
        print(f"Monthly Budget: ${budget:.2f}")
        print(f"Current Monthly Spend: ${spend:.2f}")
        print(f"Remaining: ${budget - spend:.2f}")
        
        if spend >= budget:
            print("❌ MONTHLY BUDGET EXCEEDED!")
        elif spend >= budget * 0.9:
            print("⚠️  Monthly budget almost exhausted!")
        else:
            print("✅ Monthly budget OK")
    
    else:
        # Show all budgets
        daily = tracker.get_period_spend('daily')
        weekly = tracker.get_period_spend('weekly')
        monthly = tracker.get_period_spend('monthly')
        
        daily_budget = config.get('budgets', {}).get('daily', 50.0)
        weekly_budget = config.get('budgets', {}).get('weekly', 200.0)
        monthly_budget = config.get('budgets', {}).get('monthly', 800.0)
        
        print(f"Daily: ${daily:.2f} / ${daily_budget:.2f} ({daily/daily_budget*100:.1f}%)")
        print(f"Weekly: ${weekly:.2f} / ${weekly_budget:.2f} ({weekly/weekly_budget*100:.1f}%)")
        print(f"Monthly: ${monthly:.2f} / ${monthly_budget:.2f} ({monthly/monthly_budget*100:.1f}%)")
    
    return 0


def handle_add_cost(tracker: CostTracker, args) -> int:
    """Handle manual cost entry."""
    entry = tracker.log_interaction(
        agent=args.agent,
        model=args.model,
        input_tokens=args.input_tokens,
        output_tokens=args.output_tokens,
        story_id=args.story,
        task_description=args.description
    )
    
    print("✅ Cost entry added:")
    print(f"  Model: {entry.model}")
    print(f"  Tokens: {entry.input_tokens} in, {entry.output_tokens} out")
    print(f"  Cost: ${entry.total_cost:.3f}")
    print(f"  Story: {entry.story_id or 'N/A'}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())