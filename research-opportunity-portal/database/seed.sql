-- ============================================================
-- Seed Data — 3 Sample Research Opportunities
-- ============================================================
-- Run after schema.sql:
--   mysql -u root -p research_portal < seed.sql
-- ============================================================

USE research_portal;

INSERT INTO opportunities (title, description, research_area, faculty_name, department, required_skills, positions_available, application_deadline, status)
VALUES
(
    'AI Research Assistant — Urdu NLP',
    'Join our lab to work on Natural Language Processing models for Urdu text classification and sentiment analysis. You will help build datasets, train transformer models, and evaluate results on real-world social media data.',
    'Artificial Intelligence',
    'Dr. Ahmed Khan',
    'Computer Science',
    'Python, PyTorch, NLP basics, Linguistics',
    3,
    '2026-12-15',
    'Open'
),
(
    'Cybersecurity Vulnerability Analysis',
    'Assist in identifying and documenting security vulnerabilities in IoT devices used in smart campus infrastructure. Hands-on penetration testing and report writing.',
    'Cybersecurity',
    'Dr. Fatima Noor',
    'Information Technology',
    'Networking, Linux, Wireshark, Ethical Hacking basics',
    2,
    '2026-11-30',
    'Open'
),
(
    'Data Visualization for Climate Research',
    'Help build interactive dashboards to visualize 10 years of climate data from weather stations across Pakistan. The project involves data cleaning, statistical analysis, and D3.js visualization.',
    'Data Science',
    'Prof. Bilal Hussain',
    'Software Engineering',
    'JavaScript, D3.js, Python, Pandas, SQL',
    4,
    '2026-11-01',
    'Closed'
);
