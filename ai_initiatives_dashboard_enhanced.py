# Enhanced AI Initiatives Dashboard - Complete Implementation with All 23 Requirements
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')
from data_manager import DataManager
import os
from datetime import datetime
# Removed unused imports: seaborn and matplotlib

# Page configuration
st.set_page_config(
    page_title="AI Initiatives Dashboard - SP Jain",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.18);
    }
    .insight-box {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    .filter-container {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 4px solid #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

def load_data():
    """Load all data using DataManager"""
    try:
        data_manager = DataManager()
        
        # Load all data types
        ai_tutor_data = data_manager.load_data('AI Tutor')
        ai_mentor_data = data_manager.load_data('AI Mentor')
        ai_impact_data = data_manager.load_data('AI Impact')
        ai_tkt_data = data_manager.load_data('AI TKT')
        unit_performance_data = data_manager.load_data('Unit Performance')
        cr_data = data_manager.load_data('CR (Corporate Relations)')
        prp_data = data_manager.load_data('PRP (Placement Readiness Program)')
        
        return {
            'ai_tutor': ai_tutor_data,
            'ai_mentor': ai_mentor_data,
            'ai_impact': ai_impact_data,
            'ai_tkt': ai_tkt_data,
            'unit_performance': unit_performance_data,
            'cr': cr_data,
            'prp': prp_data
        }
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

def enhanced_ai_tutor_analysis(data, program_filter=None, cohort_filter=None):
    """Enhanced AI Tutor Analysis with all 12 requirements"""
    st.header("🤖 Enhanced AI Tutor Analysis")
    
    # Apply filters
    filtered_data = data.copy()
    if program_filter and program_filter != 'All':
        filtered_data = filtered_data[filtered_data['Course(GCGM/MGM/GMBA)'] == program_filter]
    if cohort_filter and cohort_filter != 'All':
        filtered_data = filtered_data[filtered_data['Cohort'] == cohort_filter]
    
    if filtered_data.empty:
        st.warning("No data available for the selected filters.")
        return
    
    # Key Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_sessions = filtered_data['No_of_Session_IDs_created'].sum()
        st.markdown(f"""
        <div class="metric-card">
            <h3>📊 Total Sessions</h3>
            <h2>{total_sessions:,}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_participants = filtered_data['Total_Students_Participated_watched videos'].sum()
        st.markdown(f"""
        <div class="metric-card">
            <h3>👥 Total Participants</h3>
            <h2>{total_participants:,}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # Enhanced adoption rate calculation (Requirement 1)
        if total_sessions > 0:
            adoption_rate = (total_participants / total_sessions) * 100
        else:
            adoption_rate = 0
        st.markdown(f"""
        <div class="metric-card">
            <h3>📈 Adoption Rate</h3>
            <h2>{adoption_rate:.1f}%</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        avg_quiz_score = filtered_data['Average Score of AI Tutor Platform Quiz'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <h3>🎯 Avg Quiz Score</h3>
            <h2>{avg_quiz_score:.1f}/10</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # Requirement 2: Faculty Rating out of 10 with Faculty Names
    st.subheader("👨‍🏫 Faculty Performance Analysis")
    
    # Faculty-wise analysis
    faculty_analysis = filtered_data.groupby(['Faculty Name', 'Course(GCGM/MGM/GMBA)', 'Cohort']).agg({
        'Faculty_Rating_provide by students': 'mean',
        'Average Score of AI Tutor Platform Quiz': 'mean',
        'No. of Quizzes_conducted': 'sum'
    }).round(2)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Top 5 Faculty by Rating
        top_faculty = faculty_analysis.nlargest(5, 'Faculty_Rating_provide by students')
        fig_top = px.bar(
            x=top_faculty['Faculty_Rating_provide by students'],
            y=top_faculty.index.get_level_values(0),
            orientation='h',
            title="🏆 Top 5 Faculty by Student Rating (out of 10)",
            color=top_faculty['Faculty_Rating_provide by students'],
            color_continuous_scale='Viridis'
        )
        fig_top.update_layout(height=400)
        st.plotly_chart(fig_top, use_container_width=True)
    
    with col2:
        # Bottom 5 Faculty by Rating
        bottom_faculty = faculty_analysis.nsmallest(5, 'Faculty_Rating_provide by students')
        fig_bottom = px.bar(
            x=bottom_faculty['Faculty_Rating_provide by students'],
            y=bottom_faculty.index.get_level_values(0),
            orientation='h',
            title="⚠️ Bottom 5 Faculty by Student Rating",
            color=bottom_faculty['Faculty_Rating_provide by students'],
            color_continuous_scale='Reds'
        )
        fig_bottom.update_layout(height=400)
        st.plotly_chart(fig_bottom, use_container_width=True)
    
    # Requirement 3: Total Units in which AI Tutor is Implemented (Program-wise)
    st.subheader("📚 AI Tutor Implementation by Program")
    
    program_implementation = filtered_data.groupby('Course(GCGM/MGM/GMBA)')['Unit_Name'].nunique().reset_index()
    program_implementation.columns = ['Program', 'Total_Subjects_Implemented']
    
    fig_implementation = px.pie(
        program_implementation,
        values='Total_Subjects_Implemented',
        names='Program',
        title="📊 AI Tutor Implementation Distribution by Program"
    )
    st.plotly_chart(fig_implementation, use_container_width=True)
    
    # Display implementation details
    st.write("**Implementation Details:**")
    for _, row in program_implementation.iterrows():
        st.write(f"• **{row['Program']}**: {row['Total_Subjects_Implemented']} subjects implemented")
    
    # Requirement 4: Key Insights - Highest and Lowest Average Quiz Scores
    st.subheader("🎯 Key Performance Insights")
    
    subject_performance = filtered_data.groupby(['Unit_Name', 'Course(GCGM/MGM/GMBA)', 'Cohort', 'Faculty Name']).agg({
        'Average Score of AI Tutor Platform Quiz': 'mean'
    }).reset_index()
    
    # Highest performing subject
    highest_performer = subject_performance.loc[subject_performance['Average Score of AI Tutor Platform Quiz'].idxmax()]
    
    # Lowest performing subject
    lowest_performer = subject_performance.loc[subject_performance['Average Score of AI Tutor Platform Quiz'].idxmin()]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="insight-box">
            <h4>🏆 HIGHEST PERFORMANCE</h4>
            <p><strong>Subject:</strong> {highest_performer['Unit_Name']}</p>
            <p><strong>Program:</strong> {highest_performer['Course(GCGM/MGM/GMBA)']}</p>
            <p><strong>Cohort:</strong> {highest_performer['Cohort']}</p>
            <p><strong>Faculty:</strong> {highest_performer['Faculty Name']}</p>
            <p><strong>Avg Quiz Score:</strong> {highest_performer['Average Score of AI Tutor Platform Quiz']:.1f}/10</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="insight-box" style="background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);">
            <h4>⚠️ NEEDS IMPROVEMENT</h4>
            <p><strong>Subject:</strong> {lowest_performer['Unit_Name']}</p>
            <p><strong>Program:</strong> {lowest_performer['Course(GCGM/MGM/GMBA)']}</p>
            <p><strong>Cohort:</strong> {lowest_performer['Cohort']}</p>
            <p><strong>Faculty:</strong> {lowest_performer['Faculty Name']}</p>
            <p><strong>Avg Quiz Score:</strong> {lowest_performer['Average Score of AI Tutor Platform Quiz']:.1f}/10</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Requirement 5: Top 5 and Bottom 5 Subjects by Avg Quiz Score (Per Program)
    st.subheader("📊 Subject Performance Rankings")
    
    # Program filter for this section (moved above chart as requested)
    st.markdown('<div class="filter-container">', unsafe_allow_html=True)
    program_for_ranking = st.selectbox(
        "Select Program for Subject Rankings:",
        ['All'] + list(filtered_data['Course(GCGM/MGM/GMBA)'].unique()),
        key="program_ranking"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    ranking_data = filtered_data.copy()
    if program_for_ranking != 'All':
        ranking_data = ranking_data[ranking_data['Course(GCGM/MGM/GMBA)'] == program_for_ranking]
    
    subject_scores = ranking_data.groupby(['Unit_Name', 'Course(GCGM/MGM/GMBA)', 'Cohort']).agg({
        'Average Score of AI Tutor Platform Quiz': 'mean'
    }).reset_index()
    
    subject_scores['Display_Name'] = subject_scores['Unit_Name'] + ' (' + subject_scores['Course(GCGM/MGM/GMBA)'] + '_' + subject_scores['Cohort'] + ')'
    subject_scores = subject_scores.sort_values('Average Score of AI Tutor Platform Quiz', ascending=False)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Top 5 subjects
        top_5_subjects = subject_scores.head(5)
        fig_top_subjects = px.bar(
            top_5_subjects,
            x='Average Score of AI Tutor Platform Quiz',
            y='Display_Name',
            orientation='h',
            title=f"🏆 Top 5 Subjects by Quiz Score - {program_for_ranking}",
            color='Average Score of AI Tutor Platform Quiz',
            color_continuous_scale='Viridis'
        )
        fig_top_subjects.update_layout(height=400)
        st.plotly_chart(fig_top_subjects, use_container_width=True)
    
    with col2:
        # Bottom 5 subjects
        bottom_5_subjects = subject_scores.tail(5)
        fig_bottom_subjects = px.bar(
            bottom_5_subjects,
            x='Average Score of AI Tutor Platform Quiz',
            y='Display_Name',
            orientation='h',
            title=f"⚠️ Bottom 5 Subjects by Quiz Score - {program_for_ranking}",
            color='Average Score of AI Tutor Platform Quiz',
            color_continuous_scale='Reds'
        )
        fig_bottom_subjects.update_layout(height=400)
        st.plotly_chart(fig_bottom_subjects, use_container_width=True)
    
    # Requirement 6: Quiz Score Distribution (Box & Whiskers) with filters on page
    st.subheader("📈 Quiz Score Distribution Analysis")
    
    # Filters on page as requested
    st.markdown('<div class="filter-container">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        program_box = st.selectbox(
            "Select Program for Distribution:",
            ['All'] + list(filtered_data['Course(GCGM/MGM/GMBA)'].unique()),
            key="program_box"
        )
    with col2:
        cohort_box = st.selectbox(
            "Select Cohort for Distribution:",
            ['All'] + list(filtered_data['Cohort'].unique()),
            key="cohort_box"
        )
    st.markdown('</div>', unsafe_allow_html=True)
    
    box_data = filtered_data.copy()
    if program_box != 'All':
        box_data = box_data[box_data['Course(GCGM/MGM/GMBA)'] == program_box]
    if cohort_box != 'All':
        box_data = box_data[box_data['Cohort'] == cohort_box]
    
    fig_box = px.box(
        box_data,
        x='Unit_Name',
        y='Average Score of AI Tutor Platform Quiz',
        color='Course(GCGM/MGM/GMBA)',
        title=f"📊 Quiz Score Distribution Across Subjects - {program_box} - {cohort_box}"
    )
    fig_box.update_xaxes(tickangle=45)
    fig_box.update_layout(height=500)
    st.plotly_chart(fig_box, use_container_width=True)
    
    # Requirement 7: Faculty Wise Records
    st.subheader("👨‍🏫 Faculty-wise Performance Analysis")
    
    # Faculty filter on page
    st.markdown('<div class="filter-container">', unsafe_allow_html=True)
    selected_faculty = st.selectbox(
        "Select Faculty for Detailed Analysis:",
        filtered_data['Faculty Name'].unique(),
        key="faculty_analysis"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    faculty_data = filtered_data[filtered_data['Faculty Name'] == selected_faculty]
    
    # Faculty performance across subjects and cohorts
    faculty_performance = faculty_data.groupby(['Unit_Name', 'Cohort']).agg({
        'Average Score of AI Tutor Platform Quiz': 'mean'
    }).reset_index()
    
    fig_faculty = px.bar(
        faculty_performance,
        x='Unit_Name',
        y='Average Score of AI Tutor Platform Quiz',
        color='Cohort',
        title=f"📊 {selected_faculty} - Performance Across Subjects and Cohorts",
        barmode='group'
    )
    fig_faculty.update_xaxes(tickangle=45)
    fig_faculty.update_layout(height=500)
    st.plotly_chart(fig_faculty, use_container_width=True)
    
    # Requirement 8: Faculty Feedback Analysis
    st.subheader("💬 Faculty Feedback Analysis")
    
    feedback_summary = filtered_data.groupby('Faculty_Feedback').size().reset_index(name='Count')
    
    fig_feedback = px.pie(
        feedback_summary,
        values='Count',
        names='Faculty_Feedback',
        title="📊 Faculty Feedback Distribution"
    )
    st.plotly_chart(fig_feedback, use_container_width=True)
    
    # Requirement 9: Faculty Rating Analysis (already covered above)
    
    # Requirement 10: AI Tutor Student Adoption Rate vs Year
    st.subheader("📈 AI Tutor Adoption Trends")
    
    # Extract year from cohort for trend analysis
    filtered_data['Year'] = filtered_data['Cohort'].str.extract('(\d{2})').astype(int) + 2000
    
    yearly_adoption = filtered_data.groupby('Year').agg({
        'Total_Students_Participated_watched videos': 'sum',
        'No_of_Session_IDs_created': 'sum'
    }).reset_index()
    
    yearly_adoption['Adoption_Rate'] = (yearly_adoption['Total_Students_Participated_watched videos'] / yearly_adoption['No_of_Session_IDs_created']) * 100
    
    fig_trend = px.line(
        yearly_adoption,
        x='Year',
        y='Adoption_Rate',
        title="📈 AI Tutor Student Adoption Rate Trend",
        markers=True
    )
    fig_trend.update_layout(height=400)
    st.plotly_chart(fig_trend, use_container_width=True)
    
    # Requirement 11: Quiz Analysis (By Faculty, By Cohort)
    st.subheader("🎯 Comprehensive Quiz Analysis")
    
    quiz_analysis = filtered_data.groupby(['Faculty Name', 'Cohort']).agg({
        'No. of Quizzes_conducted': 'sum',
        'AI_Quizzes_used_for_grading': lambda x: (x == 'Yes').sum(),
        'Average Score of AI Tutor Platform Quiz': 'mean'
    }).round(2).reset_index()
    
    # Display quiz analysis table
    st.write("**Quiz Analysis Summary:**")
    st.dataframe(quiz_analysis, use_container_width=True)
    
    # Requirement 12: Faculty Adoption Criteria based on Quizzes Conducted
    st.subheader("📊 Faculty Adoption Analysis")
    
    faculty_adoption = filtered_data.groupby('Faculty Name').agg({
        'No. of Quizzes_conducted': 'sum',
        'Faculty_Rating_provide by students': 'mean'
    }).reset_index()
    
    # Define adoption criteria
    faculty_adoption['Adoption_Status'] = faculty_adoption['No. of Quizzes_conducted'].apply(
        lambda x: 'High Adopter' if x >= 10 else 'Medium Adopter' if x >= 5 else 'Low Adopter'
    )
    
    fig_adoption = px.scatter(
        faculty_adoption,
        x='No. of Quizzes_conducted',
        y='Faculty_Rating_provide by students',
        color='Adoption_Status',
        size='No. of Quizzes_conducted',
        hover_data=['Faculty Name'],
        title="📊 Faculty Adoption vs Performance Analysis"
    )
    fig_adoption.update_layout(height=500)
    st.plotly_chart(fig_adoption, use_container_width=True)

def enhanced_ai_mentor_analysis(data):
    """Enhanced AI Mentor Analysis with all requirements (13-16)"""
    st.header("🎓 Enhanced AI Mentor Analysis")
    
    if data.empty:
        st.warning("No AI Mentor data available.")
        return
    
    # Requirement 13: Academic Managers (AM) analysis on all possible aspects
    st.subheader("👥 Academic Managers Comprehensive Analysis")
    
    # AM Performance Overview
    am_overview = data.groupby('Academic_Manager_Name').agg({
        'Total Number of students/teams  mentoring/mentored': 'sum',
        'Approx. percentage of students under your guidance who levelled up using AI Mentor.': 'mean',
        'Q1_Are Students_motivated to use AI Mentor? (Yes/No, as they don\'t find it useful)': lambda x: (x == 'Yes').sum() / len(x) * 100,
        'Q2_Are students using AI Mentor effectively ? (Yes/No)': lambda x: (x == 'Yes').sum() / len(x) * 100,
        'Q3_Have you mandated students to meet you only after obtaining suggestions from AI Mentor? (Yes/No)': lambda x: (x == 'Yes').sum() / len(x) * 100,
        'Q4_Improvement_observed in student\'s logical thinking, Presentation & Report Structure with the use of AI Mentor (Yes/No)': lambda x: (x == 'Yes').sum() / len(x) * 100
    }).round(2).reset_index()
    
    am_overview.columns = [
        'Academic_Manager', 'Total_Students_Mentored', 'Avg_Level_Up_Percentage',
        'Student_Motivation_%', 'Effective_Usage_%', 'Mandate_Compliance_%', 'Improvement_Observed_%'
    ]
    
    # Display comprehensive AM analysis
    st.write("**Academic Managers Performance Dashboard:**")
    st.dataframe(am_overview, use_container_width=True)
    
    # Visual analysis
    col1, col2 = st.columns(2)
    
    with col1:
        # AM Effectiveness Comparison
        fig_am_effectiveness = px.bar(
            am_overview,
            x='Academic_Manager',
            y='Avg_Level_Up_Percentage',
            title="📊 AM Effectiveness - Average Level Up Percentage",
            color='Avg_Level_Up_Percentage',
            color_continuous_scale='Viridis'
        )
        fig_am_effectiveness.update_xaxes(tickangle=45)
        st.plotly_chart(fig_am_effectiveness, use_container_width=True)
    
    with col2:
        # Students Mentored Distribution
        fig_students = px.pie(
            am_overview,
            values='Total_Students_Mentored',
            names='Academic_Manager',
            title="📊 Students Distribution Among AMs"
        )
        st.plotly_chart(fig_students, use_container_width=True)
    
    # Requirement 14: Project Type Analysis for AM
    st.subheader("📋 Project Type Analysis")
    
    project_analysis = data.groupby(['Project Type (ARP, IBR 1, IBR 2, Industry Project)', 'Academic_Manager_Name']).agg({
        'Total Number of students/teams  mentoring/mentored': 'sum',
        'Approx. percentage of students under your guidance who levelled up using AI Mentor.': 'mean'
    }).reset_index()
    
    project_summary = data.groupby('Project Type (ARP, IBR 1, IBR 2, Industry Project)').agg({
        'Total Number of students/teams  mentoring/mentored': 'sum',
        'Approx. percentage of students under your guidance who levelled up using AI Mentor.': 'mean'
    }).round(2).reset_index()
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_project_volume = px.bar(
            project_summary,
            x='Project Type (ARP, IBR 1, IBR 2, Industry Project)',
            y='Total Number of students/teams  mentoring/mentored',
            title="📊 Project Volume by Type"
        )
        st.plotly_chart(fig_project_volume, use_container_width=True)
    
    with col2:
        fig_project_success = px.bar(
            project_summary,
            x='Project Type (ARP, IBR 1, IBR 2, Industry Project)',
            y='Approx. percentage of students under your guidance who levelled up using AI Mentor.',
            title="📈 Success Rate by Project Type",
            color='Approx. percentage of students under your guidance who levelled up using AI Mentor.',
            color_continuous_scale='RdYlGn'
        )
        st.plotly_chart(fig_project_success, use_container_width=True)
    
    # Requirement 15: AM adoption rate for AI Mentor
    st.subheader("📈 AM Adoption Rate Analysis")
    
    # Calculate adoption metrics
    total_ams = data['Academic_Manager_Name'].nunique()
    active_ams = data[data['Q2_Are students using AI Mentor effectively ? (Yes/No)'] == 'Yes']['Academic_Manager_Name'].nunique()
    adoption_rate = (active_ams / total_ams) * 100 if total_ams > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>👥 Total AMs</h3>
            <h2>{total_ams}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>✅ Active AMs</h3>
            <h2>{active_ams}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>📊 Adoption Rate</h3>
            <h2>{adoption_rate:.1f}%</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # Requirement 16: Top AM based on average level up percentage
    st.subheader("🏆 Top Performing Academic Managers")
    
    # Top AMs by level up percentage
    top_ams = am_overview.nlargest(5, 'Avg_Level_Up_Percentage')
    
    fig_top_ams = px.bar(
        top_ams,
        x='Avg_Level_Up_Percentage',
        y='Academic_Manager',
        orientation='h',
        title="🏆 Top 5 Academic Managers by Student Level Up Rate",
        color='Avg_Level_Up_Percentage',
        color_continuous_scale='Viridis'
    )
    fig_top_ams.update_layout(height=400)
    st.plotly_chart(fig_top_ams, use_container_width=True)
    
    # Detailed performance metrics
    st.write("**Top Performers Detailed Analysis:**")
    for _, am in top_ams.iterrows():
        st.markdown(f"""
        <div class="insight-box">
            <h4>🏆 {am['Academic_Manager']}</h4>
            <p><strong>Students Mentored:</strong> {am['Total_Students_Mentored']}</p>
            <p><strong>Level Up Rate:</strong> {am['Avg_Level_Up_Percentage']:.1f}%</p>
            <p><strong>Student Motivation:</strong> {am['Student_Motivation_%']:.1f}%</p>
            <p><strong>Effective Usage:</strong> {am['Effective_Usage_%']:.1f}%</p>
        </div>
        """, unsafe_allow_html=True)

def ai_tkt_analysis(data):
    """AI TKT (Technical Knowledge Test) Analysis"""
    st.header("🧠 AI for Technical Knowledge Test Analysis")
    
    if data.empty:
        st.warning("No AI TKT data available.")
        return
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_before = data['Average Grades Before AI for TKT'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <h3>📉 Before AI TKT</h3>
            <h2>{avg_before:.1f}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        avg_after = data['Avergae Grades After AI for TKT'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <h3>📈 After AI TKT</h3>
            <h2>{avg_after:.1f}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        avg_improvement = data['Improvement%'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <h3>🚀 Avg Improvement</h3>
            <h2>{avg_improvement:.1f}%</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        total_subjects = data['Unit'].nunique()
        st.markdown(f"""
        <div class="metric-card">
            <h3>📚 Subjects Covered</h3>
            <h2>{total_subjects}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # Before vs After Analysis
    col1, col2 = st.columns(2)
    
    with col1:
        # Subject-wise improvement
        subject_improvement = data.groupby('Unit').agg({
            'Average Grades Before AI for TKT': 'mean',
            'Avergae Grades After AI for TKT': 'mean',
            'Improvement%': 'mean'
        }).reset_index()
        
        fig_improvement = px.bar(
            subject_improvement,
            x='Unit',
            y='Improvement%',
            title="📊 Improvement by Subject",
            color='Improvement%',
            color_continuous_scale='RdYlGn'
        )
        fig_improvement.update_xaxes(tickangle=45)
        st.plotly_chart(fig_improvement, use_container_width=True)
    
    with col2:
        # Before vs After comparison
        comparison_data = []
        for _, row in data.iterrows():
            comparison_data.append({
                'Subject': row['Unit'],
                'Period': 'Before AI TKT',
                'Score': row['Average Grades Before AI for TKT']
            })
            comparison_data.append({
                'Subject': row['Unit'],
                'Period': 'After AI TKT',
                'Score': row['Avergae Grades After AI for TKT']
            })
        
        comparison_df = pd.DataFrame(comparison_data)
        
        fig_comparison = px.box(
            comparison_df,
            x='Period',
            y='Score',
            title="📊 Score Distribution: Before vs After AI TKT"
        )
        st.plotly_chart(fig_comparison, use_container_width=True)

def cr_analysis(data):
    """Corporate Relations Analysis"""
    st.header("🏢 Corporate Relations Analysis")
    
    if data.empty:
        st.warning("No Corporate Relations data available.")
        return
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_companies = data['Company Name'].nunique()
        st.markdown(f"""
        <div class="metric-card">
            <h3>🏢 Companies</h3>
            <h2>{total_companies}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_vacancies = data['No. of Vacancies_Offered'].sum()
        st.markdown(f"""
        <div class="metric-card">
            <h3>💼 Total Vacancies</h3>
            <h2>{total_vacancies:,}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        total_selected = data['Students_Selected'].sum()
        placement_rate = (total_selected / data['No. of students applied'].sum()) * 100
        st.markdown(f"""
        <div class="metric-card">
            <h3>✅ Placement Rate</h3>
            <h2>{placement_rate:.1f}%</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        avg_ctc = data['Avg_CTC(in USD)'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <h3>💰 Avg CTC (USD)</h3>
            <h2>{avg_ctc:.0f}K</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # Industry Analysis
    col1, col2 = st.columns(2)
    
    with col1:
        industry_analysis = data.groupby('Industry_Sector').agg({
            'Students_Selected': 'sum',
            'Avg_CTC(in USD)': 'mean'
        }).reset_index()
        
        fig_industry = px.bar(
            industry_analysis,
            x='Industry_Sector',
            y='Students_Selected',
            title="📊 Placements by Industry",
            color='Avg_CTC(in USD)',
            color_continuous_scale='Viridis'
        )
        fig_industry.update_xaxes(tickangle=45)
        st.plotly_chart(fig_industry, use_container_width=True)
    
    with col2:
        # Company Tier Analysis
        tier_analysis = data.groupby('Company_Tier').agg({
            'Students_Selected': 'sum',
            'Avg_CTC(in USD)': 'mean'
        }).reset_index()
        
        fig_tier = px.pie(
            tier_analysis,
            values='Students_Selected',
            names='Company_Tier',
            title="📊 Placements by Company Tier"
        )
        st.plotly_chart(fig_tier, use_container_width=True)

def prp_analysis(data):
    """Placement Readiness Program Analysis"""
    st.header("🎯 Placement Readiness Program Analysis")
    
    if data.empty:
        st.warning("No PRP data available.")
        return
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_students = len(data)
        st.markdown(f"""
        <div class="metric-card">
            <h3>👥 Total Students</h3>
            <h2>{total_students:,}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        placed_students = len(data[data['Placed/Not Placed'] == 'Placed'])
        placement_rate = (placed_students / total_students) * 100
        st.markdown(f"""
        <div class="metric-card">
            <h3>✅ Placement Rate</h3>
            <h2>{placement_rate:.1f}%</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        avg_jpt_score = data['No. of JPT Mock Interviews attempted and scored equal or above 80%'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <h3>🎯 Avg JPT Score</h3>
            <h2>{avg_jpt_score:.1f}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        avg_area_head_score = data['Area Head Mock Interview Score'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <h3>👨‍💼 Avg Area Head Score</h3>
            <h2>{avg_area_head_score:.1f}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # Performance Analysis
    col1, col2 = st.columns(2)
    
    with col1:
        # Category Analysis
        category_analysis = data.groupby('Categorise student overall (Outstanding, Good, Average, Needs Handholding)').size().reset_index(name='Count')
        
        fig_category = px.pie(
            category_analysis,
            values='Count',
            names='Categorise student overall (Outstanding, Good, Average, Needs Handholding)',
            title="📊 Student Category Distribution"
        )
        st.plotly_chart(fig_category, use_container_width=True)
    
    with col2:
        # Term Performance
        term_cols = ['Term-1', 'Term-2', 'Term-3']
        term_averages = data[term_cols].mean()
        
        fig_terms = px.bar(
            x=term_cols,
            y=term_averages.values,
            title="📊 Average Performance by Term",
            color=term_averages.values,
            color_continuous_scale='Viridis'
        )
        st.plotly_chart(fig_terms, use_container_width=True)

def main():
    """Main dashboard function"""
    # Header
    st.markdown('<h1 class="main-header">🤖 AI Initiatives Dashboard - SP Jain</h1>', unsafe_allow_html=True)
    
    # Load data
    with st.spinner("Loading data..."):
        all_data = load_data()
    
    if not all_data:
        st.error("Failed to load data. Please check your data files.")
        return
    
    # Sidebar filters
    st.sidebar.header("🔍 Filters")
    
    # Program filter (including GCGM as requested)
    programs = ['All', 'GCGM', 'MGB', 'GMBA']
    selected_program = st.sidebar.selectbox("Select Program:", programs)
    
    # Campus filter (including SYD as requested)
    campuses = ['All', 'SG', 'MUM', 'SYD', 'DXB']
    selected_campus = st.sidebar.selectbox("Select Campus:", campuses)
    
    # Cohort filter
    if not all_data['ai_tutor'].empty:
        cohorts = ['All'] + list(all_data['ai_tutor']['Cohort'].unique())
        selected_cohort = st.sidebar.selectbox("Select Cohort:", cohorts)
    else:
        selected_cohort = 'All'
    
    # Navigation
    st.sidebar.header("📊 Navigation")
    analysis_type = st.sidebar.radio(
        "Select Analysis:",
        [
            "🤖 Enhanced AI Tutor Analysis",
            "🎓 AI Mentor Analysis", 
            "🧠 AI TKT Analysis",
            "🏢 Corporate Relations",
            "🎯 Placement Readiness Program",
            "📊 AI Impact Analysis"
        ]
    )
    
    # Apply filters to AI Tutor data if campus filter is selected
    ai_tutor_filtered = all_data['ai_tutor'].copy()
    if selected_campus != 'All' and not ai_tutor_filtered.empty:
        ai_tutor_filtered = ai_tutor_filtered[ai_tutor_filtered['Campus (SG/MUM/SYD/DXB)'] == selected_campus]
    
    # Display selected analysis
    if analysis_type == "🤖 Enhanced AI Tutor Analysis":
        enhanced_ai_tutor_analysis(ai_tutor_filtered, selected_program, selected_cohort)
    
    elif analysis_type == "🎓 AI Mentor Analysis":
        enhanced_ai_mentor_analysis(all_data['ai_mentor'])
    
    elif analysis_type == "🧠 AI TKT Analysis":
        ai_tkt_analysis(all_data['ai_tkt'])
    
    elif analysis_type == "🏢 Corporate Relations":
        cr_analysis(all_data['cr'])
    
    elif analysis_type == "🎯 Placement Readiness Program":
        prp_analysis(all_data['prp'])
    
    elif analysis_type == "📊 AI Impact Analysis":
        st.header("📊 AI Impact Analysis")
        if not all_data['ai_impact'].empty:
            # Impact analysis visualization
            impact_data = all_data['ai_impact']
            
            # CGPA vs Placement analysis
            fig_impact = px.scatter(
                impact_data,
                x='CGPA',
                y='Placed/Not Placed',
                color='AI Tutor Usage',
                size='CGPA',
                title="📊 CGPA vs Placement Status by AI Tool Usage"
            )
            st.plotly_chart(fig_impact, use_container_width=True)
            
            # Usage analysis
            usage_cols = ['AI Tutor Usage', 'AI Mentor Usage', 'JPT Usage', 'Yoodli Usage']
            for col in usage_cols:
                usage_dist = impact_data[col].value_counts()
                fig = px.pie(values=usage_dist.values, names=usage_dist.index, 
                           title=f"{col} Distribution")
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No AI Impact data available.")
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666; padding: 2rem;'>"
        "🤖 AI Initiatives Dashboard - SP Jain School of Global Management<br>"
        f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
