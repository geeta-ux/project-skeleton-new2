-- ============================================================
--   QUESTION SEED DATA (Logical, Numerical, Verbal, Creative)
-- ============================================================

INSERT INTO questions (section, text, options, correct_answer, weight)
VALUES

-- ===========================
-- LOGICAL REASONING
-- ===========================
('logical',
 'If all Bloops are Razzies and all Razzies are Lazzies, are all Bloops definitely Lazzies?',
 '["Yes", "No", "Cannot be determined", "Only sometimes"]',
 'Yes', 1.0
),

('logical',
 'A train leaves Station A at 6 PM and reaches Station B at 10 PM. Another train leaves Station B at 8 PM and reaches Station A at 11 PM. At what time do they cross each other?',
 '["7 PM", "8:15 PM", "8:30 PM", "8:45 PM"]',
 '8:30 PM', 1.5
),

-- ===========================
-- NUMERICAL REASONING
-- ===========================
('numerical',
 'A company''s profit increased from INR2 lakh to INR2.5 lakh. What is the percentage increase?',
 '["10%", "20%", "25%", "50%"]',
 '25%', 1.0
),

('numerical',
 'If the average of 5 consecutive odd numbers is 25, what is the largest number?',
 '["27", "29", "31", "33"]',
 '29', 1.2
),

-- ===========================
-- VERBAL ABILITY
-- ===========================
('verbal',
 'Choose the correct synonym for "Ambiguous".',
 '["Clear", "Vague", "Precise", "Certain"]',
 'Vague', 1.0
),

('verbal',
 'Select the correct option: "She insisted ____ going out."',
 '["in", "on", "at", "for"]',
 'on', 1.0
),

-- ===========================
-- CREATIVE THINKING
-- ===========================
('creative',
 'You are designing a new logo for an eco-friendly brand. Which concept suits best?',
 '["Tree made of circuit lines", "Burning globe", "Skyscraper silhouette", "Car logo"]',
 'Tree made of circuit lines', 1.0
),

('creative',
 'A storytelling ad must evoke emotions while promoting a product. Which is the most creative approach?',
 '["Show specs and prices", "Highlight user success story", "Focus on brand colors", "Use only text slides"]',
 'Highlight user success story', 1.2
),

-- ===========================
-- EMPATHY
-- ===========================
('empathy',
 'Your colleague seems withdrawn and quiet during meetings. What should you do?',
 '["Ignore it", "Confront them publicly", "Ask privately if they''re okay", "Report to HR immediately"]',
 'Ask privately if they''re okay', 1.0
),

('empathy',
 'A patient is anxious before surgery. What''s the best response?',
 '["Tell them to relax", "Explain clearly what to expect", "Avoid talking", "Rush through the procedure"]',
 'Explain clearly what to expect', 1.2
);

-- DONE
