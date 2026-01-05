"""Output formatters for app ideas."""

import json
from pathlib import Path
from typing import Union

from ideas.models import AppIdea


def format_as_json(idea: AppIdea) -> str:
    """Format app idea as JSON.
    
    Args:
        idea: AppIdea to format
        
    Returns:
        JSON string
    """
    return idea.model_dump_json(indent=2)


def format_as_markdown(idea: AppIdea) -> str:
    """Format app idea as markdown.
    
    Args:
        idea: AppIdea to format
        
    Returns:
        Markdown formatted string
    """
    lines = [
        f"# {idea.name}",
        "",
        f"> {idea.tagline}",
        "",
        "## 📝 Description",
        "",
        idea.description,
        "",
        "## 👥 Target Users",
        "",
        idea.target_users,
        "",
        "## ✨ Core Features",
        "",
    ]
    
    # Group features by priority
    core_features = [f for f in idea.core_features if f.priority == "core"]
    important_features = [f for f in idea.core_features if f.priority == "important"]
    nice_to_have = [f for f in idea.core_features if f.priority == "nice-to-have"]
    
    if core_features:
        lines.append("### 🎯 Core")
        for feature in core_features:
            lines.append(f"- **{feature.name}**: {feature.description}")
        lines.append("")
    
    if important_features:
        lines.append("### 📌 Important")
        for feature in important_features:
            lines.append(f"- **{feature.name}**: {feature.description}")
        lines.append("")
    
    if nice_to_have:
        lines.append("### 💡 Nice-to-Have")
        for feature in nice_to_have:
            lines.append(f"- **{feature.name}**: {feature.description}")
        lines.append("")
    
    # Complexity justification
    lines.extend([
        "## 📊 Complexity Analysis",
        "",
        f"**Level:** {idea.complexity_justification.feature_count} features, "
        f"~{idea.complexity_justification.data_model_count} data models, "
        f"{idea.complexity_justification.integration_count} integrations",
        "",
        idea.complexity_justification.reasoning,
        "",
        f"**Estimated Build Time:** {idea.estimated_build_time}",
        "",
        "## 💎 Unique Selling Point",
        "",
        idea.unique_selling_point,
        "",
    ])
    
    return '\n'.join(lines)


def format_as_colored_text(idea: AppIdea) -> str:
    """Format app idea with ANSI colors for terminal display.
    
    Args:
        idea: AppIdea to format
        
    Returns:
        Colored text string
    """
    class Colors:
        HEADER = '\033[95m'
        BLUE = '\033[94m'
        CYAN = '\033[96m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        RED = '\033[91m'
        END = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'
    
    lines = [
        "",
        f"{Colors.BOLD}{Colors.HEADER}{'=' * 80}{Colors.END}",
        f"{Colors.BOLD}{Colors.CYAN}{idea.name}{Colors.END}",
        f"{Colors.HEADER}{'=' * 80}{Colors.END}",
        "",
        f"{Colors.BOLD}💡 {idea.tagline}{Colors.END}",
        "",
        f"{Colors.BOLD}📝 Description{Colors.END}",
        idea.description,
        "",
        f"{Colors.BOLD}👥 Target Users{Colors.END}",
        idea.target_users,
        "",
        f"{Colors.BOLD}✨ Core Features{Colors.END}",
    ]
    
    # Group features by priority with colors
    core_features = [f for f in idea.core_features if f.priority == "core"]
    important_features = [f for f in idea.core_features if f.priority == "important"]
    nice_to_have = [f for f in idea.core_features if f.priority == "nice-to-have"]
    
    if core_features:
        lines.append(f"\n{Colors.GREEN}🎯 Core:{Colors.END}")
        for feature in core_features:
            lines.append(f"  • {Colors.BOLD}{feature.name}{Colors.END}: {feature.description}")
    
    if important_features:
        lines.append(f"\n{Colors.YELLOW}📌 Important:{Colors.END}")
        for feature in important_features:
            lines.append(f"  • {Colors.BOLD}{feature.name}{Colors.END}: {feature.description}")
    
    if nice_to_have:
        lines.append(f"\n{Colors.BLUE}💡 Nice-to-Have:{Colors.END}")
        for feature in nice_to_have:
            lines.append(f"  • {Colors.BOLD}{feature.name}{Colors.END}: {feature.description}")
    
    # Complexity
    lines.extend([
        "",
        f"{Colors.BOLD}📊 Complexity{Colors.END}",
        f"  Features: {idea.complexity_justification.feature_count} | "
        f"Models: ~{idea.complexity_justification.data_model_count} | "
        f"Integrations: {idea.complexity_justification.integration_count}",
        f"  {idea.complexity_justification.reasoning}",
        "",
        f"{Colors.BOLD}⏱️  Build Time{Colors.END}",
        f"  {idea.estimated_build_time}",
        "",
        f"{Colors.BOLD}💎 Unique Selling Point{Colors.END}",
        f"  {idea.unique_selling_point}",
        "",
        f"{Colors.HEADER}{'=' * 80}{Colors.END}",
        "",
    ])
    
    return '\n'.join(lines)


def save_to_file(content: str, filepath: Union[str, Path]) -> None:
    """Save content to a file.
    
    Args:
        content: Content to save
        filepath: Path to save to
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.write_text(content, encoding='utf-8')
