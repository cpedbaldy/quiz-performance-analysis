import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Sample functions for analyzing and generating recommendations

def performance_label(accuracy):
    """
    Classify performance into 'Good', 'Average', or 'Bad' based on accuracy.
    :param accuracy: Accuracy score (between 0 and 1).
    :return: A string label ('Good', 'Average', or 'Bad').
    """
    if accuracy >= 0.75:
        return 'Good'
    elif accuracy >= 0.5:
        return 'Average'
    else:
        return 'Bad'

def analyze_quiz_performance(current_quiz_data, historical_quiz_data):
    """
    Analyze quiz performance based on current and historical data.
    :param current_quiz_data: DataFrame containing the latest quiz submission.
    :param historical_quiz_data: DataFrame containing the last 5 quizzes.
    :return: Analysis dictionary with insights.
    """
    insights = {}

    # Topic-wise performance
    topic_performance = current_quiz_data.groupby('topic')['is_correct'].mean()
    insights['topic_performance'] = topic_performance

    # Difficulty level performance
    difficulty_performance = current_quiz_data.groupby('difficulty')['is_correct'].mean()
    insights['difficulty_performance'] = difficulty_performance

    # Historical trends
    historical_scores = historical_quiz_data.groupby('quiz_id')['score'].mean()
    insights['historical_trends'] = historical_scores

    # Weak areas
    weak_topics = topic_performance[topic_performance < 0.5].index.tolist()
    insights['weak_topics'] = weak_topics

    # Add performance labels for topics and difficulty levels
    insights['topic_labels'] = topic_performance.apply(performance_label)
    insights['difficulty_labels'] = difficulty_performance.apply(performance_label)

    return insights

def generate_recommendations(insights):
    """
    Generate personalized recommendations based on insights.
    :param insights: Dictionary containing analysis insights.
    :return: Recommendations as a list of strings.
    """
    recommendations = []

    # Weak topics
    if insights.get('weak_topics'):
        recommendations.append(f"Focus on the following weak topics: {', '.join(insights['weak_topics'])}.")

    # Difficulty level recommendations
    if 'difficulty_performance' in insights:
        if insights['difficulty_performance'].get('hard', 1) < 0.5:
            recommendations.append("Practice more hard-level questions to improve performance.")

    # Historical trends
    if 'historical_trends' in insights:
        recent_performance = insights['historical_trends'].iloc[-1]
        avg_performance = insights['historical_trends'].mean()
        if recent_performance < avg_performance:
            recommendations.append("Recent performance is below average. Review past quizzes to identify mistakes.")

    return recommendations

def overall_performance_feedback(historical_scores):
    """
    Generate feedback based on the student's overall performance.
    :param historical_scores: Series of historical quiz scores.
    :return: A feedback message string.
    """
    avg_score = historical_scores.mean()

    if avg_score >= 0.75:
        return "Great job! You're doing really well! Keep up the good work!"
    elif avg_score >= 0.5:
        return "You're doing okay, but there's room for improvement. Keep practicing!"
    else:
        return "Better luck next time! Focus on your weak areas and try again!"

# Example usage
if __name__ == "__main__":
    # Mock current quiz data
    current_quiz_data = pd.DataFrame({
        'question_id': [1, 2, 3, 4, 5],
        'topic': ['Biology', 'Chemistry', 'Physics', 'Biology', 'Physics'],
        'difficulty': ['easy', 'medium', 'hard', 'medium', 'hard'],
        'is_correct': [1, 0, 1, 0, 0]
    })

    # Mock historical quiz data
    historical_quiz_data = pd.DataFrame({
        'quiz_id': [1, 1, 2, 2, 3, 3, 4, 4, 5, 5],
        'question_id': [1, 2, 3, 4, 5, 1, 2, 3, 4, 5],
        'score': [0.8, 0.7, 0.6, 0.5, 0.9, 0.7, 0.6, 0.8, 0.5, 0.9]
    })

    # Analyze performance
    insights = analyze_quiz_performance(current_quiz_data, historical_quiz_data)

    # Generate recommendations
    recommendations = generate_recommendations(insights)

    # Get overall performance feedback
    feedback = overall_performance_feedback(historical_quiz_data.groupby('quiz_id')['score'].mean())

    # Print insights, recommendations, and feedback
    print("Insights:")
    print(insights)
    print("\nRecommendations:")
    print("\n".join(recommendations))
    print("\nFeedback: ")
    print(feedback)

    # Visualizations for the app
    
    # Topic performance bar plot
    plt.figure(figsize=(12, 7))
    sns.barplot(x=insights['topic_performance'].index, y=insights['topic_performance'].values, palette="Spectral")
    for i, v in enumerate(insights['topic_performance'].values):
        plt.text(i, v + 0.02, f"{v*100:.2f}%", color='black', ha="center", fontweight='bold')
    plt.title('Topic Performance', fontsize=18, fontweight='bold')
    plt.xlabel('Topic', fontsize=14, fontweight='bold')
    plt.ylabel('Accuracy (%)', fontsize=14, fontweight='bold')
    plt.xticks(rotation=45, fontsize=12, fontweight='bold')
    plt.yticks(fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.gca().set_facecolor('#f7f9fc')
    plt.tight_layout()
    plt.show()

    # Difficulty level performance bar plot
    plt.figure(figsize=(10, 6))
    sns.barplot(x=insights['difficulty_performance'].index, y=insights['difficulty_performance'].values, palette="coolwarm")
    for i, v in enumerate(insights['difficulty_performance'].values):
        plt.text(i, v + 0.02, f"{v*100:.2f}%", color='black', ha="center", fontweight='bold')
    plt.title('Difficulty Level Performance', fontsize=18, fontweight='bold')
    plt.xlabel('Difficulty Level', fontsize=14, fontweight='bold')
    plt.ylabel('Accuracy (%)', fontsize=14, fontweight='bold')
    plt.xticks(fontsize=12, fontweight='bold')
    plt.yticks(fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.gca().set_facecolor('#f0f8ff')
    plt.tight_layout()
    plt.show()

    # Historical trends line plot with stylish markers
    plt.figure(figsize=(12, 7))
    sns.lineplot(data=insights['historical_trends'], marker='o', markersize=10, color='crimson', linewidth=2)
    for i, v in enumerate(insights['historical_trends']):
        plt.text(i, v + 0.02, f"{v*100:.2f}%", color='black', ha="center", fontweight='bold')
    plt.title('Performance Trends Over Time', fontsize=18, fontweight='bold')
    plt.xlabel('Quiz ID', fontsize=14, fontweight='bold')
    plt.ylabel('Average Score (%)', fontsize=14, fontweight='bold')
    plt.xticks(fontsize=12, fontweight='bold')
    plt.yticks(fontsize=12)
    plt.grid(axis='both', linestyle='--', alpha=0.7)
    plt.gca().set_facecolor('#fffaf0')
    plt.tight_layout()
    plt.show()
