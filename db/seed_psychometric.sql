-- ============================================================
--   PSYCHOMETRIC QUESTION SEED DATA
--   (Personality, Cognitive Style, Work Preference)
-- ============================================================

INSERT INTO psychometric_questions (section, text, options, weight, is_active)
VALUES
-- ANALYTICAL vs CREATIVE
(
 'psychometric',
 'I enjoy breaking down complex problems into logical steps.',
 '{
   "Strongly Agree": {"Analytical": 5},
   "Agree": {"Analytical": 4},
   "Neutral": {"Analytical": 3},
   "Disagree": {"Analytical": 2},
   "Strongly Disagree": {"Analytical": 1}
 }',
 1.0,
 TRUE
),
(
 'psychometric',
 'I prefer coming up with original ideas rather than following existing methods.',
 '{
   "Strongly Agree": {"Creativity": 5},
   "Agree": {"Creativity": 4},
   "Neutral": {"Creativity": 3},
   "Disagree": {"Creativity": 2},
   "Strongly Disagree": {"Creativity": 1}
 }',
 1.0,
 TRUE
),

-- WORK STYLE
(
 'psychometric',
 'I am comfortable working independently without constant supervision.',
 '{
   "Strongly Agree": {"Independence": 5},
   "Agree": {"Independence": 4},
   "Neutral": {"Independence": 3},
   "Disagree": {"Independence": 2},
   "Strongly Disagree": {"Independence": 1}
 }',
 1.0,
 TRUE
),
(
 'psychometric',
 'I perform better when collaborating with others in a team.',
 '{
   "Strongly Agree": {"Teamwork": 5},
   "Agree": {"Teamwork": 4},
   "Neutral": {"Teamwork": 3},
   "Disagree": {"Teamwork": 2},
   "Strongly Disagree": {"Teamwork": 1}
 }',
 1.0,
 TRUE
),
(
 'psychometric',
 'I prefer having clear rules and structured processes while working.',
 '{
   "Strongly Agree": {"Structure": 5},
   "Agree": {"Structure": 4},
   "Neutral": {"Structure": 3},
   "Disagree": {"Structure": 2},
   "Strongly Disagree": {"Structure": 1}
 }',
 1.0,
 TRUE
),

-- PERSONALITY (BIG-5 LITE)
(
 'psychometric',
 'I enjoy learning new things and exploring unfamiliar topics.',
 '{
   "Strongly Agree": {"Openness": 5},
   "Agree": {"Openness": 4},
   "Neutral": {"Openness": 3},
   "Disagree": {"Openness": 2},
   "Strongly Disagree": {"Openness": 1}
 }',
 1.0,
 TRUE
),
(
 'psychometric',
 'I plan my tasks carefully and complete them on time.',
 '{
   "Strongly Agree": {"Conscientiousness": 5},
   "Agree": {"Conscientiousness": 4},
   "Neutral": {"Conscientiousness": 3},
   "Disagree": {"Conscientiousness": 2},
   "Strongly Disagree": {"Conscientiousness": 1}
 }',
 1.0,
 TRUE
),
(
 'psychometric',
 'I feel energized when interacting with many people.',
 '{
   "Strongly Agree": {"Extraversion": 5},
   "Agree": {"Extraversion": 4},
   "Neutral": {"Extraversion": 3},
   "Disagree": {"Extraversion": 2},
   "Strongly Disagree": {"Extraversion": 1}
 }',
 1.0,
 TRUE
),
(
 'psychometric',
 'I stay calm and focused even under pressure.',
 '{
   "Strongly Agree": {"Emotional Stability": 5},
   "Agree": {"Emotional Stability": 4},
   "Neutral": {"Emotional Stability": 3},
   "Disagree": {"Emotional Stability": 2},
   "Strongly Disagree": {"Emotional Stability": 1}
 }',
 1.0,
 TRUE
),

-- LEADERSHIP & RISK
(
 'psychometric',
 'I naturally take the lead when working in a group.',
 '{
   "Strongly Agree": {"Leadership": 5},
   "Agree": {"Leadership": 4},
   "Neutral": {"Leadership": 3},
   "Disagree": {"Leadership": 2},
   "Strongly Disagree": {"Leadership": 1}
 }',
 1.0,
 TRUE
),
(
 'psychometric',
 'I am comfortable making decisions even when outcomes are uncertain.',
 '{
   "Strongly Agree": {"Risk Taking": 5},
   "Agree": {"Risk Taking": 4},
   "Neutral": {"Risk Taking": 3},
   "Disagree": {"Risk Taking": 2},
   "Strongly Disagree": {"Risk Taking": 1}
 }',
 1.0,
 TRUE
);
