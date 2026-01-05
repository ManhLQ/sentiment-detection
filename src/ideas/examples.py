"""Training examples for the app idea generator.

These examples demonstrate the expected quality and structure for generated ideas.
They cover different complexity levels and domains to guide the LLM.
"""

from ideas.models import (
    AppIdea,
    ComplexityJustification,
    ComplexityLevel,
    Feature,
    IdeaRequest,
)

# Example 1: Low Complexity - Productivity
EXAMPLE_1_REQUEST = IdeaRequest(
    domain="productivity",
    complexity=ComplexityLevel.LOW,
)

EXAMPLE_1_IDEA = AppIdea(
    name="FocusBlocks",
    tagline="A minimalist Pomodoro timer with task tracking",
    description="FocusBlocks helps users stay productive by combining Pomodoro technique with simple task management. Users can create tasks, start focus sessions, and track their daily productivity streaks.",
    target_users="Students, remote workers, and anyone looking to improve focus and time management",
    core_features=[
        Feature(
            name="Pomodoro Timer",
            description="25-minute focus sessions with 5-minute breaks",
            priority="core",
        ),
        Feature(
            name="Task List",
            description="Simple CRUD operations for tasks with completion tracking",
            priority="core",
        ),
        Feature(
            name="Daily Statistics",
            description="View completed sessions and tasks for the current day",
            priority="important",
        ),
        Feature(
            name="Streak Tracking",
            description="Track consecutive days of productivity",
            priority="nice-to-have",
        ),
    ],
    complexity_justification=ComplexityJustification(
        feature_count=4,
        data_model_count=3,
        integration_count=0,
        reasoning="Low complexity with 4 simple features, minimal data models (User, Task, Session), no external integrations, and straightforward CRUD operations. Perfect for a 1-2 week build.",
    ),
    estimated_build_time="1-2 weeks",
    unique_selling_point="Unlike comprehensive productivity apps that can feel overwhelming, FocusBlocks strips away the noise. Its unique selling point is its strict focus on the visual psychology of streak-building, making habit formation the primary and only user interface.",
)

# Example 2: Medium Complexity - Project Management
EXAMPLE_2_REQUEST = IdeaRequest(
    domain="project management",
    complexity=ComplexityLevel.MEDIUM,
)

EXAMPLE_2_IDEA = AppIdea(
    name="RequireFlow",
    tagline="Collaborative requirements gathering and prioritization for product teams",
    description="RequireFlow streamlines the requirements gathering process by providing a structured workflow for collecting, organizing, and prioritizing feature requests from stakeholders. Teams can vote on requirements, add comments, and track the evolution of ideas from initial concept to implementation.",
    target_users="Product managers, development teams, and stakeholders in software projects",
    core_features=[
        Feature(
            name="Requirement Cards",
            description="Create and organize requirements with rich text descriptions, attachments, and metadata",
            priority="core",
        ),
        Feature(
            name="Voting System",
            description="Stakeholders can vote on requirements to indicate priority and interest",
            priority="core",
        ),
        Feature(
            name="Comment Threads",
            description="Threaded discussions on each requirement for clarification and feedback",
            priority="core",
        ),
        Feature(
            name="Workflow States",
            description="Move requirements through states: Proposed → Under Review → Approved → In Development",
            priority="important",
        ),
        Feature(
            name="Team Collaboration",
            description="Invite team members with different roles (Admin, Contributor, Viewer)",
            priority="important",
        ),
        Feature(
            name="Export Reports",
            description="Generate PDF/CSV reports of requirements and voting results",
            priority="nice-to-have",
        ),
    ],
    complexity_justification=ComplexityJustification(
        feature_count=6,
        data_model_count=7,
        integration_count=0,
        reasoning="Medium complexity with 6 features requiring user authentication, role-based permissions, voting mechanics, and state management. Approximately 7 data models (User, Team, Requirement, Vote, Comment, Attachment, WorkflowState). Suitable for 3-6 weeks of development.",
    ),
    estimated_build_time="4-6 weeks",
    unique_selling_point="Most requirement tools are either too simple (spreadsheets) or too complex (enterprise tools). RequireFlow hits the sweet spot by focusing specifically on the early-stage requirement gathering process with built-in collaboration and prioritization, making it perfect for agile teams.",
)

# Example 3: High Complexity - Education
EXAMPLE_3_REQUEST = IdeaRequest(
    domain="education",
    complexity=ComplexityLevel.HIGH,
)

EXAMPLE_3_IDEA = AppIdea(
    name="CodePath",
    tagline="Personalized learning paths for developers with adaptive difficulty",
    description="CodePath creates customized learning journeys for developers by analyzing their skill level, learning pace, and goals. The platform adapts content difficulty in real-time based on performance, provides hands-on coding challenges, and connects learners with mentors for guidance.",
    target_users="Self-taught developers, bootcamp students, and professionals looking to upskill in new technologies",
    core_features=[
        Feature(
            name="Skill Assessment",
            description="Initial and periodic assessments to gauge current skill level across multiple domains",
            priority="core",
        ),
        Feature(
            name="Adaptive Learning Paths",
            description="AI-generated personalized curriculum that adjusts based on learner performance and pace",
            priority="core",
        ),
        Feature(
            name="Interactive Coding Challenges",
            description="In-browser code editor with automated testing and instant feedback",
            priority="core",
        ),
        Feature(
            name="Progress Analytics",
            description="Detailed dashboards showing learning velocity, strengths, and areas for improvement",
            priority="important",
        ),
        Feature(
            name="Mentor Matching",
            description="Connect learners with experienced developers for 1-on-1 guidance",
            priority="important",
        ),
        Feature(
            name="Peer Code Review",
            description="Submit solutions for review by other learners and mentors",
            priority="important",
        ),
        Feature(
            name="Achievement System",
            description="Badges, certificates, and portfolio generation for completed learning paths",
            priority="nice-to-have",
        ),
        Feature(
            name="Community Forum",
            description="Discussion boards for asking questions and sharing knowledge",
            priority="nice-to-have",
        ),
    ],
    complexity_justification=ComplexityJustification(
        feature_count=8,
        data_model_count=15,
        integration_count=2,
        reasoning="High complexity with 8 features including AI-driven personalization, real-time code execution, mentor matching algorithms, and analytics. Requires approximately 15 data models (User, LearningPath, Module, Challenge, Submission, Assessment, Mentor, Review, Achievement, etc.) and integrations with code execution sandbox and possibly LLM for content generation. Estimated 2-3 months of development.",
    ),
    estimated_build_time="2-3 months",
    unique_selling_point="Unlike static course platforms, CodePath continuously adapts to each learner's unique journey. The combination of AI-driven personalization, hands-on practice, and human mentorship creates a learning experience that's both scalable and deeply personal.",
)

# Example 4: Medium Complexity - Developer Tools
EXAMPLE_4_REQUEST = IdeaRequest(
    domain="developer tools",
    complexity=ComplexityLevel.MEDIUM,
)

EXAMPLE_4_IDEA = AppIdea(
    name="APIVault",
    tagline="Smart API response caching and cost optimization for developers",
    description="APIVault helps developers reduce API costs and improve application performance by intelligently caching API responses. It provides a simple proxy layer that automatically caches responses based on configurable rules, tracks cost savings, and offers analytics on API usage patterns.",
    target_users="Backend developers, DevOps engineers, and teams working with expensive third-party APIs",
    core_features=[
        Feature(
            name="Smart Proxy",
            description="Transparent proxy layer that intercepts API calls and serves cached responses when appropriate",
            priority="core",
        ),
        Feature(
            name="Caching Rules",
            description="Configure TTL, cache invalidation strategies, and selective caching based on endpoints or parameters",
            priority="core",
        ),
        Feature(
            name="Cost Tracking",
            description="Monitor API usage and calculate cost savings from cache hits",
            priority="core",
        ),
        Feature(
            name="Usage Analytics",
            description="Visualize API call patterns, cache hit rates, and response time improvements",
            priority="important",
        ),
        Feature(
            name="Multi-API Support",
            description="Manage caching for multiple different APIs from a single dashboard",
            priority="important",
        ),
        Feature(
            name="Cache Warming",
            description="Pre-populate cache with frequently accessed data during off-peak hours",
            priority="nice-to-have",
        ),
    ],
    complexity_justification=ComplexityJustification(
        feature_count=6,
        data_model_count=6,
        integration_count=0,
        reasoning="Medium complexity with 6 features requiring proxy implementation, caching strategies, analytics, and cost calculation. Approximately 6 data models (User, APIConfig, CacheRule, CachedResponse, UsageMetric, CostCalculation). No external integrations needed as it acts as a proxy. Suitable for 3-5 weeks of development.",
    ),
    estimated_build_time="3-5 weeks",
    unique_selling_point="Most caching solutions are generic and require significant configuration. APIVault is specifically designed for API cost optimization, with built-in intelligence to suggest optimal caching strategies based on actual usage patterns and automatic cost tracking that shows ROI in real-time.",
)

# Collect all examples
TRAINING_EXAMPLES = [
    {"request": EXAMPLE_1_REQUEST, "idea": EXAMPLE_1_IDEA},
    {"request": EXAMPLE_2_REQUEST, "idea": EXAMPLE_2_IDEA},
    {"request": EXAMPLE_3_REQUEST, "idea": EXAMPLE_3_IDEA},
    {"request": EXAMPLE_4_REQUEST, "idea": EXAMPLE_4_IDEA},
]


def get_examples_by_complexity(complexity: ComplexityLevel) -> list[dict]:
    """Filter examples by complexity level.
    
    Args:
        complexity: Complexity level to filter by
        
    Returns:
        List of examples matching the complexity level
    """
    return [
        ex for ex in TRAINING_EXAMPLES
        if ex["request"].complexity == complexity
    ]
